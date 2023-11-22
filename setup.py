from distutils.core import setup

setup(
    name='web3_balancer',
    packages=['web3_balancer'],
    version='0.1b',
    license='GNU GPL-3.0 license',
    description='A balancer for web3 connections',
    author='Lars Lundin',
    author_email='lars.y.lundin@gmail.com',
    url='https://github.com/larsyngvelundin/web3_balancer',
    download_url='https://github.com/larsyngvelundin/web3_balancer/archive/refs/tags/v.011.tar.gz',
    keywords=['web3'],
    install_requires=[
        'web3',
        'loguru',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
