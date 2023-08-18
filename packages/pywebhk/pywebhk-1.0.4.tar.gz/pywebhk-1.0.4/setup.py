from setuptools import setup, find_packages

setup(
    name="pywebhk",
    version="1.0.4",
    description="An ultra small Discord webhook handler",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lapis Pheonix",
    url="https://github.com/LapisPhoenix/Pywebhk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "certifi==2023.7.22",
        "charset-normalizer==3.2.0",
        "idna==3.4",
        "requests==2.31.0",
        "urllib3==2.0.4",
        "validators==0.21.2"
    ],
)
