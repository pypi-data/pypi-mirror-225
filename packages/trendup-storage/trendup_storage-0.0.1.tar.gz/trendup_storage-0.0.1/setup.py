from distutils.core import setup

setup(
    name="trendup_storage",
    version="0.0.1",

    author="JerryLin",
    author_email="jerry.lin@keeptossinglab.com",
    packages=["src"],
    include_package_data=True,
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    description="Useful towel-related stuff.",
    install_requires=[
        "attrs",
    ],
)
