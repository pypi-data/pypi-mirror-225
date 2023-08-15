from setuptools import setup, find_packages

setup(
    name='email_verify',
    version='0.1',
    author='can gologlu',
    author_email='can@xn--glolu-jua30a.com',
    description='Django app for e-mail verification on sign up',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'itsdangerous>=2.1.2',
    ],
)