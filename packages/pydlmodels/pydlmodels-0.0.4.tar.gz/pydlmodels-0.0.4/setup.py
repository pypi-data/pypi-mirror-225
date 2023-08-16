from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pydlmodels',
    version='0.0.4',
    description='A package for deep learning models and data preprocessing',
    author= 'Ateendra Jha',
    author_email="ateendrajha@live.com",
    url = 'https://www.drateendrajha.com/projects/pydlmodels',
    long_description_content_type="text/markdown",
    long_description = long_description,
    packages=setuptools.find_packages(),
    keywords=['python', 'pandas', 'numpy', 'basic libraries', "models", "deep learning", 'resnet', 'nlp' ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pydlmodels'],
    package_dir={'':'src'},
    install_requires = [
        'pybaseanal',
        'torch',
        'termcolor',
        'datetime',
        'torchvision',
        'tqdm',
        'nltk'
    ]
)