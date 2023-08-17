import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trustplatform-ip-protection",
    version="0.0.2",
    author="Microchip Technology",
    author_email="SPG.Tools@microchip.com",
    description="Trust Platform IP Protection usecase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="#",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Closed :: Microchip",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
