from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="EmployeeAttritionPrediction",
    version="0.1",
    author="Saranya",
    packages=find_packages(),
    install_requires=requirements,
)    