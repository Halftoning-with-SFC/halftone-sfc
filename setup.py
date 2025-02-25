from setuptools import setup, find_packages

setup(
    name="halftonesfc",
    version="0.1.0",
    author="halftonesfc-team",
    author_email="al.pedro.porto@impatech.org.br",
    description="A Python package for Digital Halftoning with Space Filling Curves",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "matplotlib",
        "numpy"
    ],
    dependency_links=[
        "https://pypi.org/simple/"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "halftonesfc = halftonesfc:cli",
        ],
    }
)
