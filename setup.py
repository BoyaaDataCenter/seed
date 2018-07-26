from setuptools import setup, find_packages

VERSION = '0.1'


def get_requirements(env):
    with open('requirements-{}.txt'.format(env)) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


install_requires = get_requirements('base')


setup(
    name='seed',
    version=VERSION,
    install_requires=install_requires,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'send = seed.runner:main',
        ]
    }
)
