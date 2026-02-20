from setuptools import setup, find_packages

hyphen_e_dot = '-e .'

def get_requirements(file_path: str) -> list:
    with open(file_path, 'r') as file:
        requirements = file.read().splitlines()

    if hyphen_e_dot in requirements:
        requirements.remove(hyphen_e_dot)

    return requirements


setup(
    name='mlproject',
    version='0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)