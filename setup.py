import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dapt",
    packages=["dapt"],
    version="0.9.1.4",
    license='BSD 3-clause "New" or "Revised" license',
    author="Ben S. Duggan",
    author_email="dugganbens@gmail.com",
    description="A library to assist with running parameter sets across multiple systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenSDuggan/DAPT",
    keywords=['paramater', 'testing', 'distributed'],
    install_requires=[
        'boxsdk>=2.0.0',
        'flask>=1.0.2',
        'gspread>=3.1.0',
        'oauth2client>=4.1.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)