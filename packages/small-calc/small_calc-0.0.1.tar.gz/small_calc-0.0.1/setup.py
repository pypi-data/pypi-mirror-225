from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="small_calc",
    version="0.0.1",
    author="Orlando Nascimento",
    author_email="on_ferreira@id.uff.br",
    description="Testing the creation of packages in Pypi with a small calculator package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/on-ferreira/simple-package-test",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)