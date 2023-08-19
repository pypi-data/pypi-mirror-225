import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutil-cfg",
    version='0.0.5',
    author="chhsiao",
    author_email="hsiao.chuanheng@gmail.com",
    description="python util for cfg (configurations)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chhsiao1981/pyutil_cfg",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
