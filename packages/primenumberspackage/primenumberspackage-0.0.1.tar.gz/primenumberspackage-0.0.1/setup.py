from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
    
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="primenumberspackage",
    version="0.0.1",
    author="Lucas Venicius Alves Santos",
    author_email="lucas.alves.santos19@gmail.com",
    description="This code shows a range of prime numbers based on the minimum and maximum numbers the user prompts",
    long_description=page_description,
    long_description_content_type='text/markdown',
    url="https://github.com/lucasvenicius19/primenumberspackage.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
)