# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skillsnetwork',
 'skillsnetwork.cvstudio',
 'skillsnetwork.cvstudio.download_all',
 'skillsnetwork.cvstudio.download_model',
 'skillsnetwork.cvstudio.ping',
 'skillsnetwork.cvstudio.report',
 'skillsnetwork.cvstudio.upload_model']

package_data = \
{'': ['*']}

install_requires = \
['ipython', 'ipywidgets>=7,<8', 'requests>=2,<3', 'tqdm>=4,<5']

extras_require = \
{'docs': ['Sphinx>=4,<5',
          'sphinx-autodoc-typehints>=1,<2',
          'pydata-sphinx-theme>=0.9,<0.10'],
 'regular': ['ibm-cos-sdk>=2,<3'],
 'regular:python_version >= "3.7.17" and python_version < "4.0.0"': ['typing-extensions']}

setup_kwargs = {
    'name': 'skillsnetwork',
    'version': '0.21.0',
    'description': 'Library for working with Skills Network',
    'long_description': '# Skills Network Python Library\n\nA library for working with [Skills Network](https://skills.network) Python labs.\n\n - [Documentation](https://ibm-skills-network.github.io/skillsnetwork-python-library/)\n\n### Environment Variables\n\n(Required environment variables for testing)\n\n- `CV_STUDIO_TOKEN`\n- `CV_STUDIO_BASE_URL`\n- `IBMCLOUD_API_KEY`\n\n## Contributing\nPlease see [CONTRIBUTING.md](https://github.com/ibm-skills-network/skillsnetwork-python-library/blob/main/CONTRIBUTING.md)\n',
    'author': 'Bradley Steinfeld',
    'author_email': 'bs@ibm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '==3.7.17',
}


setup(**setup_kwargs)
