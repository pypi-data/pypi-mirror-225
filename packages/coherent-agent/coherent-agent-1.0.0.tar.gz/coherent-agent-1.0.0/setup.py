from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='coherent-agent',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
    url='https://github.com/coherent-api/coherent-agent',
    license='MIT',
    author='Can Colakoglu',
    author_email='can@coherent.xyz',
    description='Coherent-Agent makes working with LLMs a breeze.',
)