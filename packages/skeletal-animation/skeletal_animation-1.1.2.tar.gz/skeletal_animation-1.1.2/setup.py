from setuptools import setup, find_packages

setup(
    name="skeletal_animation",
    version="1.1.2",
    description="Standalone package for skeletal animation",
    long_description="# This is a work in progrees",
    long_description_content_type="text/markdown",
    url="https://gitlab-etu.ing.he-arc.ch/isc/general/python-skeletal-animation/tb-animation-squelettale-fork",
    author='Dimitri "Kerzoum" Kohler',
    author_email="dimitri.kohler@he-arc.ch",
    maintainer='Christophe "chrismeunier" Muller',
    maintainer_email="christophe.muller@he-arc.ch",
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages()
    + [
        "skeletal_animation.examples",
        "skeletal_animation.gui",
        "skeletal_animation.gui.assets.shaders",
    ],
    package_data={
        "skeletal_animation": [
            ".config",
            # To be removed at some point, only concerns the GUI app
            "animated_models/fbx/*.fbx",
            "gui/assets/shaders/*.glsl",
            # To be removed, need to find a way to include the fbx module in the package
            "utils/fbx_bindings/*",
        ],
    },
    install_requires=[
        "setuptools",
        "wheel",
        "numpy-quaternion>=2022.0.0",
        "numpy",
        "pygltflib>=1.15.0",  # for the utils.loader
        "bpy>=3.4.0",  # only for additional conversion tools in utils.other
    ],
    include_package_data=True,
)

