from setuptools import setup, find_packages


setup(
    name='complex_mathematics',
    version='3.5.3',
    packages=find_packages(),
    install_requires=[
        'numpy', 'scipy'
    ],
    license='MIT',
    author="Arnav Malhotra",
    author_email="emumalhotra@gmail.com",
    description="Many complex math features.",
    long_description="Many advanced math features and topics like linear algebra, geometry, calculus, algebra, and machine learning algorithms.",
    url="https://github.com/Arnav-MaIhotra/complex_mathematics",
)