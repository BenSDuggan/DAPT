import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dapt",
    version="0.9.0",
    author="Ben S. Duggan",
    author_email="dugganbens@gmail.com",
    description="A library to assist with running parameter sets across multiple systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenSDuggan/DAPT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)