from setuptools import setup

setup(
    name="lloom",
    version="0.0.1",
    packages=["lloom"],
    install_requires=[
        "tiktoken",
        "pydantic"
    ],
)
