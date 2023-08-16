from setuptools import find_packages, setup
setup(
    name='geotran',
    packages=find_packages(include=['geotran']),
    version='0.1.3',
    description='Python Geospatial Library',
    author='Thai Tran',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)