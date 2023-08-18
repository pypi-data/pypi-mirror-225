from setuptools import setup, find_packages

setup(
    name="query_strings_parser",
    version="0.1.5",
    license="Apache License 2.0",
    author="Jefferson Sampaio de Medeiros",
    author_email="jefferson.medeiros@nutes.uepb.edu.br",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/nutes-uepb/query_strings_parser",
    keywords="query query-strings sql parser"
)
