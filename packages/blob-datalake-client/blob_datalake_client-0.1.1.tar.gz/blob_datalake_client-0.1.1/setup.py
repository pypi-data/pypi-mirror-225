from setuptools import setup, find_packages

setup(
    name='blob_datalake_client',
    version='0.1.1',
    license='Apache License 2.0',
    author="Lucas Barbosa Oliveira",
    author_email='lucas.barbosa@nutes.uepb.edu.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/nutes-uepb/blob_datalake_client',
    keywords='blob datalake storage azure',
    install_requires=[
          'azure-storage-file-datalake==12.10.1',
      ],
)
