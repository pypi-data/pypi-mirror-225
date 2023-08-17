from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent

if (this_directory / "README.md").is_file():
    long_description = (this_directory / "README.md").read_text()
else:
    long_description="#DESC"

setup(
    name='mlplatformutils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.9.5.18',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
    author='Keshav Singh',
    author_email='keshav_singh@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mlplatformutils',
    install_requires=[
          'applicationinsights','gremlinpython','azureml-core','azure-identity','azure-storage-file-datalake','azure-cosmos'
      ],

)
