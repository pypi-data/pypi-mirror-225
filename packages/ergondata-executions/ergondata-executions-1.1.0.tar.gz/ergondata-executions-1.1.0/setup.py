from setuptools import setup

setup(
    name='ergondata-executions',
    version='1.1.0',
    description="Collection of methods to connect and interact with Ergondata's Execution API",
    author_email="daniel.vossos@ergondata.com.br",
    author='Daniel Anzanello Vossos',
    url='',
    packages=['ergondata_executions'],
    install_requires=["requests", "typing_extensions"],
    license="MIT",
    keywords="executions"
)
