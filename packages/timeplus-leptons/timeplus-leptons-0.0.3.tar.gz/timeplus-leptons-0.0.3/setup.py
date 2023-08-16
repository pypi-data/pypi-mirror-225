from setuptools import setup, find_packages  # noqa: H301
import os

print("current dir")
print(os.getcwd())

exec(open("leptons/version.py").read())

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "urllib3 >= 1.15",
    "six >= 1.10",
    "certifi",
    "openai>=0.27.8",
    "timeplus>=1.3.0b2",
]

setup(
    name="timeplus-leptons",
    version=__version__,  # noqa: F821
    author="Timeplus",
    author_email="eng@timeplus.io",
    description="Timeplus OpenAI API monitor tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/timeplus-io/leptons",
    packages=find_packages(where=".", exclude=("tests",)),
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
    ],
)
