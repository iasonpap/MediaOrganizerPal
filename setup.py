from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="MediaOrganiserPal",
    version="0.0.1",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)