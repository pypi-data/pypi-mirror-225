from setuptools import setup, find_packages

VERSION = '0.0.13'
DESCRIPTION = 'Utility functions/wrapper for psycopg2 python package'


with open("./README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="psycopg2_utility_functions",
    version=VERSION,
    author="qxh5696",
    author_email="qxh5696@g.rit.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['psycopg2-binary'],
    keywords=['python', 'database', 'postgresql', 'psql'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
