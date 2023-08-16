import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yesno.wtf",
    version="0.0.1",
    author="Nemupy",
    author_email="nemu.otoyume@gmail.com",
    description="Wrapper for yesno.wtf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nemupy/yesno.wtf",
    packages=setuptools.find_packages()
)