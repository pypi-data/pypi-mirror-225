from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dl_matrix",
    version="3.2",
    packages=find_packages(),
    description="A Divergent Language Matrix package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohamed Diomande",
    author_email="gdiomande7907@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="divergent language matrix",
    url="http://github.com/diomandeee/dl_matrix",
    install_requires=requirements,
    python_requires=">=3.6",
)

# 