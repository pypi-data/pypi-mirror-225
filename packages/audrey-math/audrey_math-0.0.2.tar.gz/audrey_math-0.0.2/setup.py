from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "first python package!"

setup (
    # name should match the name of module (second folder)
    name = "audrey_math",
    version = VERSION,
    author = "Audrey Lin",
    description = DESCRIPTION,
    packages = find_packages(),
    # add any additional packages that need to be installed w/ my package
    # install_requires = []
    keywords = ["python", "first package"]
    #provide more information about my package
    # classifiers = []
)
