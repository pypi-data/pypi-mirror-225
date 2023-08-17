# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whereabouts']

package_data = \
{'': ['*']}

install_requires = \
['duckdb==0.7.1',
 'fastparquet>=2023.7.0,<2024.0.0',
 'lxml>=4.9.2,<5.0.0',
 'openpyxl>=3.1.1,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyarrow>=12.0.1,<13.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.11.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'whereabouts',
    'version': '0.2.0',
    'description': '',
    'long_description': "# Whereabouts\nFast, scalable geocoding for Python using DuckDB\n\n## Description\nGeocode addresses and reverse geocode coordinates directly from Python in your own environment. \n- No additional database setup required. Uses DuckDB to run all queries\n- No need to send data to an external geocoding API\n- Fast (Geocode 1000s / sec and reverse geocode 200,000s / sec)\n- Robust to typographical errors\n\n**Currently only working for Australian data.**\n\n## Requirements\n- Python 3.8+\n- Poetry (for package management)\n\n## Installation\nOnce Poetry is installed and you are in the project directory:\n\n```\npoetry shell\npoetry install\n```\n\n1) Download the latest version of GNAF core from https://geoscape.com.au/data/g-naf-core/\n2) Update the `setup.yml` file to point to the location of the GNAF core file\n3) Finally, setup the geocoder. This creates the required reference tables\n\n```\npython setup_geocoder.py\n```\n\n## Examples\n\nGeocode a list of addresses \n```\nfrom whereabouts.Matcher import Matcher\n\nmatcher = Matcher(db_name='gnaf_au')\nmatcher.geocode(addresslist, how='standard')\n```\n\nFor more accurate geocoding you can use trigram phrases rather than token phrases\n```\nmatcher.geocode(addresslist, how='trigram')\n```",
    'author': 'alex2718',
    'author_email': 'ajlee3141@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
