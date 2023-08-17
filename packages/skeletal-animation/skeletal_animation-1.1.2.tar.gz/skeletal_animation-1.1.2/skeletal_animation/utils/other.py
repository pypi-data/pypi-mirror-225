import numpy as np
import bpy

from skeletal_animation.core.math.constants import VERY_HIGH_R_TOL
from skeletal_animation.core.model import Skeleton


def are_skeletons_similar(first_skeleton: Skeleton, second_skeleton: Skeleton):
    """Checks if the skeletons are similar.

    Similarity is defined as:
    - The skeletons have the same number of joints.
    - The local bind transforms of the joints are within a tolerance of each other.
      The tolerance used in this case does not need to be tight. Since if the joints
      of the first skeleton start at similar positions to those of the second skeleton,
      the animation will look correct.
      Tolerance values are defined in skeletal_animation/core/math/constants.py. file
      Very high tolerance values are used here.

    Parameters
    ----------
    first_skeleton : Skeleton
        First skeleton.
    second_skeleton : Skeleton
        Skeleton to compare to the first.

    Returns
    -------
    bool
        True if the skeletons are similar, False otherwise.

    Warnings
    --------
    This function may return false positives.
    For two skeletons to be similar, the joint hierarchy of both must be the same.
    However, this check is not implemented yet.
    """
    first_joint_list = first_skeleton.as_joint_list()
    second_joint_list = second_skeleton.as_joint_list()

    if len(first_joint_list) != len(second_joint_list):
        return False
    for i in range(len(first_joint_list)):
        if not np.allclose(
            first_joint_list[i].local_bind_transform.as_matrix(),
            second_joint_list[i].local_bind_transform.as_matrix(),
            rtol=VERY_HIGH_R_TOL,
        ):
            return False
    return True


def fbx_to_gltf(fbx_file_path, gltf_file_path):
    # See https://docs.blender.org/api/current/bpy.ops.import_scene.html#bpy.ops.import_scene.fbx
    # and https://docs.blender.org/api/current/bpy.ops.export_scene.html#bpy.ops.export_scene.gltf
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)
    # print([obj for obj in bpy.data.objects])
    bpy.ops.object.select_all(action="DESELECT")
    # Delete the default camera, cube and light, keeping the armature
    bpy.data.objects["Camera"].select_set(True)
    bpy.data.objects["Cube"].select_set(True)
    bpy.data.objects["Light"].select_set(True)
    bpy.ops.object.delete()
    # print([obj for obj in bpy.data.objects])
    bpy.ops.export_scene.gltf(
        filepath=gltf_file_path, use_active_scene=True, export_yup=False
    )


if __name__ == "__main__":

    try:
        import fbx
    except ImportError:
        print("Could not import fbx on first try")
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
            try:
                import fbx
            except ImportError:
                print("Could not import fbx on second try")
                raise
    print(fbx)


    # fbx_to_gltf(
    #     os.path.join(FBX_ANIMATION_PATH, "bow.fbx"),
    #     os.path.join(GLTF_ANIMATION_PATH, "bow.glb"),
    # )

    pass
