from setuptools import setup

setup(
    name="lonadb-client",
    version="1.0",
    author="Collin Buchkamer",
    author_email="collin@kisara.app",
    description="A client library for interacting with LonaDB server",
    url="https://github.com/LonaDB/Python-Client",
    packages=["lonadb_client"],
    install_requires=[
        "pycryptodome"
    ],
)
