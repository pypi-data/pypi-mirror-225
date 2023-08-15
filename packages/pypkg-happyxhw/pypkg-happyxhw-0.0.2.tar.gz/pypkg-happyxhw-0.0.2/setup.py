from setuptools import setup

setup(
    name='pypkg-happyxhw',
    version='0.0.2',
    author='happyxhw',
    author_email='happyxhw@outlook.com',
    description='python useful package',
    url='https://git.happyxhw.cn:8443/happyxhw/pypkg.git',
    packages=['pypkg_happyxhw'],
    install_requires=[
        "coloredlogs",
        "pyyaml"
    ],
)
