from setuptools import setup, find_packages

setup(
    name='faiss-imputer',
    version='0.1.1',
    url='https://github.com/ScionKim/FaissImputer',
    license='MIT',
    description='Impute missing values using faiss',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hakkil Kim',
    author_email='scionkim@gmail.com',
    packages=find_packages(),
    install_requires=['numpy', 'faiss-cpu', 'scikit-learn']
)