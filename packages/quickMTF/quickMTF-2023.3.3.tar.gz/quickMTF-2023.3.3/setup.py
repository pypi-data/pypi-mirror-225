import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickMTF", # Replace with your own username
    version="2023.3.3",
    author="lorry_rui",
    author_email="lorryruizhihua@gmail.com",
    description="quick MTF for Line_pair and SFR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lorrytoolcenter/quickMTF",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
