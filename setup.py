from setuptools import setup, find_packages


setup(
    name='edp_redy_py',
    version='0.1.6',
    license='Apache 2.0',
    author="Fábio Ferreira",
    author_email='fabiorcferreira@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/skyborgff/edp_redy',
    keywords='EDP',
    install_requires=[],

)