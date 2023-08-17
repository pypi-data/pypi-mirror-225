from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='quantum-expresso-analize',
    version='1.0.0',
    license='MIT License',
    author='Rafael Barreto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rafinhareis17@gmail.com',
    keywords='quantum expresso',
    description=u'Quantum expresso data analize',
    packages=['pyqe'],
    install_requires=['pandas','scipy','numpy','matplotlib'],)