import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()
setuptools.setup(
    name='AndN',
    version='0.1.4',
    url='https://github.com/grayrail000/AndroidQQ',
    packages=setuptools.find_packages(),
    license='',
    author='1a',
    author_email='',
    description='',
    install_requires=required
)
