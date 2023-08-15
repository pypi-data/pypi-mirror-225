from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="icesat2SH", 
    version='0.0.3',
    author="Sajjad Hajizade",
    author_email="sajjad73hajizade@gmail.com",
    description="A description of your library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sajjad73hajizade/icesat2SH/tree/main',
    packages=find_packages(),
    install_requires=[
        "requests",
        "jsonschema",
	"datetime",
        # Add more dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
