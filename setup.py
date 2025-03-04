from setuptools import setup

setup(
    name="DBHandler",
    version="0.1.1",
    include_package_data=True,
    install_requires=[
        'h5py',
        'lmdb',
        'numpy',
        'setuptools',
        'tqdm',
        'opencv-python'],
    author="Kai",
    author_email="koreadeep19@gmail.com",
    description="A package for handling Database files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KDL-Solution/DBHandler",  # Replace with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
