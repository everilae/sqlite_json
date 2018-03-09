from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="sqlite_json",
    version="0.0.0",
    description="SQLAlchemy plugin that adds SQLite dialect JSON support",
    long_description=long_description,
    author="Ilja Everilä",
    author_email="saarni@gmail.com",
    license="MIT",
    url="https://github.com/everilae/sqlite_json",
    packages=["sqlite_json"],
    #setup_requires=[ "pytest-runner" ],
    #tests_require=[ "pytest" ],
    install_requires=[
        "sqlalchemy>=1.1"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "sqlalchemy.plugins": [
            "jsonplugin = sqlite_json:JsonPlugin"
        ]
    }
)
