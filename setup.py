import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tac1",
    version="0.7.0",
    author="Gianluca Romanin",
    author_email="romaninz@gmail.com",
    description="Simple note taking app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayZar21/tac1_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points=
    {
        "console_scripts": ["tac1 = tac1.tac1:main"],
    },
)