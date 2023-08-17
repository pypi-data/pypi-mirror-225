import os
from pathlib import Path

from skeletal_animation.utils.loader import load_gltf, serialize, RAW_ANIMATION_PATH, SERIALIZED_ANIMATION_PATH

# Load the gltf file
gltf_file = "walk_90.glb"
walk_animator = load_gltf(os.path.join(RAW_ANIMATION_PATH, gltf_file))

serialized_file = "".join(gltf_file.split(".")[:-1])
# Replace default path with the path where you want to save the serialized animation
serialize(
    walk_animator,
    serialized_file,
    SERIALIZED_ANIMATION_PATH,
)
