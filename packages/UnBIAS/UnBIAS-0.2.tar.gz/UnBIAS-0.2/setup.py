from setuptools import setup, find_packages

setup(
    name="UnBIAS",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "transformers",
    ],
    author="Shaina Raza",
    author_email="shaina.raza@utoronto.ca",
    description="A package for detecting bias, performing named entity, and debiasing text.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VectorInstitute/NewsMediaBias/UnBIAS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
