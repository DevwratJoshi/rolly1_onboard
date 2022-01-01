from setuptools import setup

setup(
    name='rolly_controllers',
    version='0.0.1',
    packages=['rolly_controllers'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.8"',
    ],
)
