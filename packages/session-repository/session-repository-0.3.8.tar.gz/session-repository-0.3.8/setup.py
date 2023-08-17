from setuptools import setup

version = "0.3.8"

setup(
    name="session-repository",
    version=version,
    packages=[
        "session_repository",
        "session_repository.models",
    ],
    install_requires=[
        "sqlalchemy",
    ],
    license="MIT",
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to have a base repository class to permform select/insert/update/delete with dynamtic syntaxe",
    url="https://github.com/Impro02/session-repository",
    download_url="https://github.com/Impro02/session-repository/archive/refs/tags/%s.tar.gz"
    % version,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
