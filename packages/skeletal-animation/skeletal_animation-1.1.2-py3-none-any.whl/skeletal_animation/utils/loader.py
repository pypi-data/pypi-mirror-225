import warnings
import os
import sys
import numpy as np
import quaternion
import pickle
import struct
from pathlib import Path
from pygltflib import GLTF2

from skeletal_animation.core.math import Transform
from skeletal_animation.core.model import Joint, Skeleton
from skeletal_animation.core.animate import (
    Key,
    Curve,
    JointAnimation,
    Animation,
    Animator,
)


_ANIMATED_MODELS_PATH = ""

# Keyword to search for at the beginning of a line
keyword = "Animated_Models:"


relative_path_to_config = "..\.config"

# When run from GeeXLab
try:
    import gh_utils

    path_to_config = os.path.join(gh_utils.get_demo_dir(), relative_path_to_config)

# When run normally
except:
    path_to_config = relative_path_to_config


try:
    # Read the file line by line and find the matching line
    matching_line = None
    with open(path_to_config, "r") as f:
        for line in f:
            if line.startswith(keyword):
                matching_line = line.strip()
                matching_path = matching_line[len(keyword) :].lstrip()
                break
except FileNotFoundError:
    raise FileNotFoundError(f".config file not found at {path_to_config}")

# Print the matching line if found
if matching_path:
    _ANIMATED_MODELS_PATH = matching_path
else:
    print(f"No line starting with '{keyword}' found in {path_to_config}")
    raise ValueError

RAW_ANIMATION_PATH = Path(os.path.join(_ANIMATED_MODELS_PATH, "raw"))
SERIALIZED_ANIMATION_PATH =Path(os.path.join(_ANIMATED_MODELS_PATH, "serialized"))


def serialize(animator, file_name: str, path: Path):
    """Serialize the current animator to a file using pickle.

    Animator object is saved as a pickle file (.pkl).

    Parameters:
    -----------
    animator : Animator
        The animator to serialize
    file_name : str
        The name of the file to save. Extension .pkl is added automatically.
    path : str
        The path to where the file will be saved.
    """
    if isinstance(path, str):
        path = Path(path)

    # Create parent folder if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    with open(path / (file_name + ".pkl"), "wb") as f:
        pickle.dump(animator, f)


def load_serialized(file_name: str, path: Path):
    """Load a serialized animator from a file using pickle.

    Animator object is loaded from a pickle file (.pkl).

    Parameters:
    -----------
    file_name : str
        The name of the file to load. Extension .pkl is added automatically.
    path : str
        The path to the file to load.

    Returns:
    --------
    animator : Animator
        The loaded Animator object.

    Raises:
    -------
    FileNotFoundError
        If the file cannot be found.
    """
    if isinstance(path, str):
        path = Path(path)
    try:
        with open(path / (file_name + ".pkl"), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + path + file_name + ".pkl")


def load_fbx(fbx_file_path):
    """Creates an Animator object from a fbx file.

    This method requires the installation of the fbx sdk for python.
    The fbx sdk is available at: https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-2-1.

    Parameters:
    -----------
    fbx_file_path : str
        The path to the fbx file to load.

    Raises:
    -------
    ImportError
        If the FBX SDK is not installed.

    Returns:
    --------
    animator : Animator
        The generated Animator object.

    Warnings
    --------
    This loader does not support all fbx files.
    Fbx files must follow the following criteria:
    - Animation data contains only one animation stack with only one animation layer.
    - If a key contains a value for one axis, the values for all other axes must be specified.
    Fbx files exported from Mixamo follow these criteria.
    """
    # check if the fbx sdk is installed
    try:
        import fbx
    except ImportError:
        import platform

        # is platform Windows?
        if platform.system() == "Windows":
            # add the path to the local fbx bindings
            from pathlib import Path
            import skeletal_animation
            import sys

            utils_path = Path(skeletal_animation.utils.__file__).parent
            fbx_path = utils_path / "fbx_bindings"
            sys.path.append(str(fbx_path))
            # Second try:
            try:
                import fbx
            except ImportError:
                raise

        warnings.warn(
            "The FBX SDK is not installed.\
            To load animation files from fbx, the FBX SDK must be installed.\
            see https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0",
            stacklevel=2,
        )

    sdk_manager = fbx.FbxManager.Create()

    ios = fbx.FbxIOSettings.Create(sdk_manager, fbx.IOSROOT)
    sdk_manager.SetIOSettings(ios)

    importer = fbx.FbxImporter.Create(sdk_manager, "")

    if not importer.Initialize(fbx_file_path, -1, sdk_manager.GetIOSettings()):
        print("Call to FbxImporter::Initialize() failed.")
        raise ImportError(
            "Error importing file %s file not found or %s"
            % (
                str(fbx_file_path),
                importer.GetStatus().GetErrorString(),
            )
        )

    scene = fbx.FbxScene.Create(sdk_manager, "myScene")
    importer.Import(scene)
    importer.Destroy()

    # _____________LOADING FBX HIERARCHY_____________
    def load_skeleton_nodes(skeleton_node_list, root_node):
        for i in range(root_node.GetChildCount()):
            child_node = root_node.GetChild(i)
            for i in range(child_node.GetNodeAttributeCount()):
                attribute = child_node.GetNodeAttributeByIndex(i)
                if type(attribute) == fbx.FbxSkeleton:
                    skeleton_node_list.append(child_node)
            load_skeleton_nodes(skeleton_node_list, child_node)

    def get_anim_layer():
        nb_anim_stack = scene.GetSrcObjectCount(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId)
        )

        if nb_anim_stack == 0:
            raise ValueError("No animation stack found in fbx file.")
        elif nb_anim_stack > 1:
            warnings.warn(
                "Multiple anim stacks found in fbx file, only the first one is treated",
                stacklevel=2,
            )

        anim_stack = scene.GetSrcObject(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId), 0
        )

        nb_anim_layers = anim_stack.GetSrcObjectCount(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId)
        )

        if nb_anim_layers == 0:
            raise ValueError("No animation layer found in anim stack.")
        elif nb_anim_layers > 1:
            warnings.warn(
                "Multiple anim layers found in anim stack, only the first one is treated",
                stacklevel=2,
            )

        anim_layer = anim_stack.GetSrcObject(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId), 0
        )

        return anim_layer

    def load_curves(skeleton_node, anim_layer):
        # Assumes that when a change to the position/orientation of a joint is made,
        # the translation/rotation values for each axis are given in the keyframe.

        tX_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "X")
        tY_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "Y")
        tZ_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "Z")
        rX_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "X")
        rY_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "Y")
        rZ_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "Z")

        translation_keys = []
        rotation_keys = []

        duration = 1.0

        if tX_curve is not None and tY_curve is not None and tZ_curve is not None:
            for key_id in range(tX_curve.KeyGetCount()):
                key_time = tX_curve.KeyGetTime(key_id).GetTimeString("")

                t = [
                    tX_curve.KeyGetValue(key_id),
                    tY_curve.KeyGetValue(key_id),
                    tZ_curve.KeyGetValue(key_id),
                ]

                if "*" in key_time:
                    # Keys whose time is marked with "*" are not used in the animation.
                    # They are probably used to improve interpolation quality in between keyframes.
                    pass
                else:
                    key_time = float(key_time)
                    if key_time > duration:
                        duration = key_time

                    translation_keys.append(Key(key_time, t))

        if rX_curve is not None and rY_curve is not None and rZ_curve is not None:
            for key_id in range(rX_curve.KeyGetCount()):
                key_time = rX_curve.KeyGetTime(key_id).GetTimeString("")

                v = fbx.FbxVector4(
                    rX_curve.KeyGetValue(key_id),
                    rY_curve.KeyGetValue(key_id),
                    rZ_curve.KeyGetValue(key_id),
                )

                m = fbx.FbxAMatrix()
                m.SetR(v)
                q = m.GetQ()
                q = np.quaternion(q.GetAt(3), q.GetAt(0), q.GetAt(1), q.GetAt(2))

                if "*" in key_time:
                    # Keys whose time is marked with "*" are not used in the animation.
                    # They are probably used to improve interpolation quality in between keyframes.
                    pass
                else:
                    key_time = float(key_time)
                    if key_time > duration:
                        duration = key_time

                    rotation_keys.append(Key(key_time, q))

        for key in translation_keys:
            key.time /= duration
        for key in rotation_keys:
            key.time /= duration

        translation_curve = Curve(translation_keys)
        rotation_curve = Curve(rotation_keys)
        return translation_curve, rotation_curve, duration

    # Assumes that the animation data contains only one animation stack with only one animation layer.
    # Mixamo rigged animations have this structure.
    # Assumes the duration of the animation for each joint is the same.

    root_node = scene.GetRootNode()
    skeleton_node_list = []

    load_skeleton_nodes(skeleton_node_list, root_node)

    skeleton_root = None
    root_set = False

    anim_layer = get_anim_layer()
    joint_animations = []

    joint_hierarchy = []

    anim_duration = 1.0

    for skeleton_node in skeleton_node_list:
        # Creating joints
        joint_name = skeleton_node.GetName()

        pos = [float(val) for val in skeleton_node.LclTranslation.Get()]

        rotation = skeleton_node.PreRotation.Get()

        v = fbx.FbxVector4(rotation)

        m = fbx.FbxAMatrix()
        m.SetR(v)
        q = m.GetQ()
        orient = np.quaternion(q.GetAt(3), q.GetAt(0), q.GetAt(1), q.GetAt(2))

        joint = Joint(name=joint_name, local_bind_transform=Transform(pos, orient))

        children = []
        for i in range(skeleton_node.GetChildCount()):
            child_node = skeleton_node.GetChild(i)
            children.append(child_node.GetName())

        joint_hierarchy.append((joint, children))

        if not root_set:
            skeleton_root = joint
            root_set = True

        # Creating joint animations
        if anim_layer:
            translation_curve, rotation_curve, duration = load_curves(
                skeleton_node, anim_layer
            )
            if duration > anim_duration:
                anim_duration = duration
            joint_animation = JointAnimation(joint, translation_curve, rotation_curve)
            joint_animations.append(joint_animation)

    # Building joint hierarchy
    joint_list = [relation[0] for relation in joint_hierarchy]

    for relation in joint_hierarchy:
        children = [joint for joint in joint_list if joint.name in relation[1]]
        relation[0].add_children(children)

    # Creating skeleton
    skeleton = Skeleton(skeleton_root)

    # Creating animation
    animation = Animation(joint_animations, anim_duration)

    animator = Animator(animation=animation, skeleton=skeleton)

    return animator


def load_gltf(glb_file_path):
    """Creates an Animator object from a glTF 2.0 file.
    To create an Animator, we need the following piece of data:
        1. Skeleton Hierarchy
        2. Animator
            1. Joint Animations
                1. Animation Curves

    glTF provides us two interesting lists: skins and animations
    We'll retrieve the Armature hierarchy from the skin list
    Then, we'll get the animation curves from the animation list

    We have to be careful Because the animation data contains
    final pos/rot and not the differences

    We can directly get the local_bind_transform from the metadata
    We need the accessor-buffer chain to get the time + TRS curves
    We are only interested in the translation and rotation though

    Same assumptions: one skin, one anim. No mesh yet.
    """

    def array_from_accessor_id(accessor_i):
        accessor = gltf.accessors[accessor_i]
        buffer_view = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[buffer_view.buffer]

        data = gltf.get_data_from_buffer_uri(buffer.uri)
        struct_size = buffer_view.byteLength // accessor.count
        output = []
        for i in range(accessor.count):
            index = buffer_view.byteOffset + accessor.byteOffset + i * struct_size
            d = data[index : index + struct_size]
            v = struct.unpack("<" + (struct_size // 4) * "f", d)
            if len(v) == 1:
                v = v[0]
            output.append(v)

        return output

    gltf = GLTF2().load(glb_file_path)

    skeleton_nodes = {}
    skeleton_root = None
    skeleton_name = None
    pos_min = 0.0

    curves = {"translation": {}, "rotation": {}, "scale": {}, "weights": {}}
    joint_animations = []
    anim_duration = 1.0

    # 1. Create a list of Joints from the file.
    for joint_i in gltf.skins[0].joints:
        skeleton_node = gltf.nodes[joint_i]

        joint_name = skeleton_node.name
        pos = skeleton_node.translation
        rot = skeleton_node.rotation

        if not pos:
            pos = [0.0, 0.0, 0.0]
        if not rot:
            rot = [0.0, 0.0, 0.0, 1.0]

        if pos[1] > pos_min:
            pos_min = pos[1]

        orient = np.quaternion(rot[3], rot[0], rot[1], rot[2])
        xform = Transform(pos, orient.normalized())
        joint = Joint(name=joint_name, local_bind_transform=xform)

        skeleton_nodes[joint_i] = joint
        curves["translation"][joint_i] = None
        curves["rotation"][joint_i] = None

    # 2. Create the skeleton hierarchy
    for joint_i in skeleton_nodes:
        skeleton_node = gltf.nodes[joint_i]
        children = [skeleton_nodes[child] for child in skeleton_node.children]
        skeleton_nodes[joint_i].add_children(children)

    armature_node = gltf.nodes[gltf.scenes[gltf.scene].nodes[0]]
    skeleton_root = skeleton_nodes[armature_node.children[0]]
    skeleton_name = armature_node.name
    skeleton_root.local_bind_transform.pos[1] -= pos_min

    # 3. Create the animation curves from the file
    animation = gltf.animations[0]

    for channel in animation.channels:
        target = channel.target
        joint_i = target.node

        sampler = animation.samplers[channel.sampler]
        key_times = array_from_accessor_id(sampler.input)
        key_data = array_from_accessor_id(sampler.output)
        keys = []

        key_len = len(key_times)
        duration = 1.0
        if key_len > 0:
            duration = key_times[-1]

            if key_len - 1 > anim_duration:
                anim_duration = float(key_len - 1)

        for i in range(len(key_times)):
            t = float(int((key_times[i] / duration) * (key_len - 1)))
            v = key_data[i]
            if target.path == "translation":
                p = skeleton_nodes[joint_i].local_bind_transform.pos
                if joint_i == armature_node.children[0]:
                    p = [0.0, 0.0, 0.0]
                keys.append(Key(t, [v[0] - p[0], v[1] - p[1], v[2] - p[2]]))
            elif target.path == "rotation":
                q = skeleton_nodes[joint_i].local_bind_transform.orient
                Q1 = np.quaternion(v[3], v[0], v[1], v[2])
                Q1 = Q1.normalized()
                if joint_i == armature_node.children[0]:
                    keys.append(Key(t, Q1))
                else:
                    keys.append(Key(t, q.conjugate() * Q1))
            else:
                break

        for key in keys:
            key.time /= key_len - 1
        # for key in keys:
        #     print( key.time );
        # print( len( keys ) );

        curve = Curve(keys)
        curves[target.path][joint_i] = curve

    # 4. Link the animation with the rig
    for joint_i in skeleton_nodes:
        joint = skeleton_nodes[joint_i]
        joint_animations.append(
            JointAnimation(
                joint, curves["translation"][joint_i], curves["rotation"][joint_i]
            )
        )

    # skeleton = Skeleton( skeleton_root, skeleton_name );
    skeleton = Skeleton(skeleton_root)
    animation = Animation(joint_animations, anim_duration)
    # print( 'GLTF: ', anim_duration );

    return Animator(animation=animation, skeleton=skeleton)
