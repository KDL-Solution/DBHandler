from setuptools import setup, find_packages

# requirements.txt 파일 읽기
def parse_requirements(filename):
    """ requirements.txt 파일을 읽고 패키지 리스트 반환 """
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line and not line.startswith("#")]

setup(
    name="DBHandler",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
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
