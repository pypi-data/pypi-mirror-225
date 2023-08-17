from setuptools import setup, find_packages
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
# Read the contents of your README file
with open(os.path.join(current_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PermCCA",
    version="0.0.1",
    description="A permutation-based CCA analysis toolbox",
    author="Neil Jianzhang Ni",
    author_email="jzni132134@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wetiqe/PermCCA",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "pingouin",
        "seaborn",
        "sklearn",
        "tqdm",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
