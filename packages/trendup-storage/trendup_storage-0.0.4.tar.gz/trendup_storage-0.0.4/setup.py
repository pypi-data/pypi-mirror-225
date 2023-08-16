from setuptools import setup, find_packages

setup(
    name="trendup_storage",
    version="0.0.4",

    author="JerryLin",
    author_email="jerry.lin@keeptossinglab.com",
    packages=["trendup_storage"],
    include_package_data=True,
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    description="Useful towel-related stuff.",
    install_requires=[
        "attrs",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
