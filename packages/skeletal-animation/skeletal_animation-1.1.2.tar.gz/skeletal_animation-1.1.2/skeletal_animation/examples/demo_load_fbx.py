import os
from pathlib import Path

from skeletal_animation.utils.loader import load_fbx, serialize, RAW_ANIMATION_PATH, SERIALIZED_ANIMATION_PATH


# Load the fbx file
fbx_file = "death.fbx"
# Replace default path with the path of the fbx file
walk_animator = load_fbx(
    # "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/fbx/walk.fbx"
    os.path.join(RAW_ANIMATION_PATH, fbx_file)
)

serialized_file = "".join(fbx_file.split(".")[:-1])
# Replace default path with the path where you want to save the serialized animation
serialize(
    walk_animator,
    serialized_file,
    SERIALIZED_ANIMATION_PATH,
)
