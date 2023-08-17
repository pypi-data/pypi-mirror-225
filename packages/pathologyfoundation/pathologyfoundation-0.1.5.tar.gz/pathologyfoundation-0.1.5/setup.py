from setuptools import setup, find_packages

setup(
    name = 'pathologyfoundation',
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "clip-anytorch",
        "pillow>=9.0.1",
        "appdirs",
        "pandas",
        "numpy",
        "tqdm",
        "gdown",
        "scikit-learn",
    ],
    version = '0.1.5',  # Ideally should be same as the GitHub release tag varsion
    description="A package of pathology foundation models.",
    long_description=open("README.md").read(),
    author = 'Zhi Huang',
    author_email = 'hz9423@gmail.com',
    url = 'https://github.com/PathologyFoundation/PathologyFoundation',
    keywords = ['Pathology', 'Foundation model', "PLIP", "OpenPath"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)