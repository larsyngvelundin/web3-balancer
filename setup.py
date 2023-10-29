from setuptools import setup


setup(
    name='web3_balancer',
    version='0.1',
    description='A connection balancer for web3',
    author='Lars Lundin',
    author_email='lars.y.lundin@gmail.com',
    url='https://github.com/larsyngvelundin/web3-balancer/',
    packages=['src'],
    package_dir={'': 'src'},
    install_requires=[
        'web3',
        'loguru',
    ],
)
