from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'azure_utils',
  packages = ['azure_utils', 'azure_utils.utils'],
  version = '0.1.0',
  license='MIT',
  description = 'Azure Utilities',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Connor Makowski',
  author_email = 'conmak@mit.edu',
  url = 'https://github.com/connor-makowski/azure_utils',
  download_url = 'https://github.com/connor-makowski/azure_utils/dist/azure_utils-0.1.0.tar.gz',
  keywords = [],
  install_requires=["azure-storage-blob>=12.17.0"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
