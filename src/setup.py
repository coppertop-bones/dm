from setuptools import setup, find_namespace_packages

setup(
    name='coppertop-dm',
    version='2023.03.19',
    python_requires='>=3.9',
    license='BSD',
    packages=find_namespace_packages(),
    url='https://github.com/coppertop-bones/dm/',
    author='David Briant',
    author_email='dangermouseb@forwarding.cc',
    description="danger mouse's standard library + more for coppertop-bones",
    install_requires=['coppertop-bones >= 2023.03.19', 'numpy >= 1.17.3', 'scipy >= 1.8'],
)
