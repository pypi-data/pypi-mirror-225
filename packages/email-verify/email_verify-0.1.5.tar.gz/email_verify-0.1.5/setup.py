from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='email_verify',
    version='0.1.5',
    author='can gologlu',
    author_email='can@xn--glolu-jua30a.com',
    description='Django app for e-mail verification on sign up',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'itsdangerous>=2.1.2',
    ],
)