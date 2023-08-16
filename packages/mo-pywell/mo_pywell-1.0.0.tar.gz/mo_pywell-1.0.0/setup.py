from setuptools import setup

setup(
    name='mo_pywell',
    version="1.0.0",
    author='Scott Reynen',
    packages=['pywell'],
    url='https://github.com/MoveOnOrg/pywell',
    install_requires=[
        "boto3",
        "botocore"
    ],
    license='MIT',
    description="A collection of independent Python scripts following the Unix philosphy of doing one thing well. Forked from https://github.com/sreynen/pywell.",
)
