from setuptools import setup, find_packages

VERSION = "2.1.6"
DESCRIPTION = "Utilities for FastAPI"

# Setting up
setup(
    name="py-ke-utils-fastapi",
    version=VERSION,
    author="KE",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["redis>=4.5.0", "deepdiff>=6.2.1", "fastapi>=0.90", "SQLAlchemy>=2.0.1", "alembic>=1.10"],
    keywords=["python", "FastAPI", "PyJWT", "decorator", "token"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
