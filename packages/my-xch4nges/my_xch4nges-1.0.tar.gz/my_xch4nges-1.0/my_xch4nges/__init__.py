from setuptools import setup, find_packages

setup(
    name="my_exchanges",
    version="1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "gate_api",
        "pybithumb",
        "pyokx",
        "python-dotenv",
        "python_bitget",
        "pyupbit",
    ],
    author="bemodest.eth",
    description="Comprehensive list of exchange api implements to use on my projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
