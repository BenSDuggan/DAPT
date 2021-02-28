import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dapt",
    packages=["dapt", "dapt.db", "dapt.storage"],
    version="0.9.2",
    license='BSD 3-clause "New" or "Revised" license',
    author="Ben S. Duggan",
    author_email="dugganbens@gmail.com",
    description="A library enabling teams to distributed parameter sets between computational resources for faster parameter testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenSDuggan/DAPT",
    keywords=['paramater', 'testing', 'distributed', 'crowdsorcing'],
    install_requires=[
        'boxsdk>=2.0.0',
        'flask>=1.0.2',
        'gspread>=3.1.0',
        'oauth2client>=4.1.3',
        'google-api-python-client>=1.10.0',
        'google-auth-httplib2>=0.0.4',
        'google-auth-oauthlib>=0.4.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)