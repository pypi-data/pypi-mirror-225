import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="wikimediabot",
    version="0.0.1",
    author="Sebastian Berg",
    author_email="sebastian.berg@handarel.dev",
    description="WikimediaBot",
    long_description=long_description,
    packages=setuptools.find_packages(),
    py_modules=["wikimediabot"],
    package_dir={"": "src/wikimediabot"},
)
