# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcoll', 'xcoll.beam_elements', 'xcoll.scattering_routines.everest']

package_data = \
{'': ['*'],
 'xcoll': ['headers/*',
           'scattering_routines/fluka/flukaio/*',
           'scattering_routines/fluka/flukaio/doc/*',
           'scattering_routines/fluka/flukaio/include/*',
           'scattering_routines/fluka/flukaio/lib/*',
           'scattering_routines/fluka/flukaio/samples/*',
           'scattering_routines/fluka/flukaio/src/*',
           'scattering_routines/fluka/flukaio/tests/*',
           'scattering_routines/fluka/flukaio/tests/fakes/*'],
 'xcoll.beam_elements': ['collimators_src/*']}

install_requires = \
['numpy>=1.0',
 'pandas>=1.4',
 'xdeps>=0.1.1',
 'xfields>=0.12.1',
 'xobjects>=0.2.6',
 'xpart>=0.15.0',
 'xtrack>=0.36.5']

extras_require = \
{'tests': ['ruamel-yaml>=0.17.31,<0.18.0']}

setup_kwargs = {
    'name': 'xcoll',
    'version': '0.2.4',
    'description': 'Xsuite collimation package',
    'long_description': '# xcoll\n\n<!---![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xcoll?logo=PyPI?style=plastic) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/xcoll?logo=PyPI?style=plastic)-->\n\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/xsuite/xcoll?style=plastic)\n![GitHub](https://img.shields.io/github/license/xsuite/xcoll?style=plastic)\n![PyPi](https://img.shields.io/pypi/dm/xcoll?logo=PyPI&style=plastic)\n![GitHub all releases](https://img.shields.io/github/downloads/xsuite/xcoll/total?logo=GitHub&style=plastic)\n\n![GitHub pull requests](https://img.shields.io/github/issues-pr/xsuite/xcoll?logo=GitHub&style=plastic)\n![GitHub issues](https://img.shields.io/github/issues/xsuite/xcoll?logo=GitHub&style=plastic)\n![GitHub repo size](https://img.shields.io/github/repo-size/xsuite/xcoll?logo=GitHub&style=plastic)\n\nCollimation in xtrack simulations\n\n## Description\n\n## Getting Started\n\n### Dependencies\n\n* python >= 3.8\n    * numpy\n    * pandas\n    * xsuite (in particular xobjects, xdeps, xtrack, xpart)\n\n### Installing\n`xcoll` is packaged using `poetry`, and can be easily installed with `pip`:\n```bash\npip install xcoll\n```\nFor a local installation, clone and install in editable mode (need to have `pip` >22):\n```bash\ngit clone git@github.com:xsuite/xcoll.git\npip install -e xcoll\n```\n\n### Example\n\n## Features\n\n## Authors\n\n* [Frederik Van der Veken](https://github.com/freddieknets) (frederik@cern.ch)\n* [Despina Demetriadou](https://github.com/ddemetriadou)\n* [Andrey Abramov](https://github.com/anabramo)\n* [Giovanni Iadarola](https://github.com/giadarol)\n\n\n## Version History\n\n* 0.1\n    * Initial Release\n\n## License\n\nThis project is [Apache 2.0 licensed](./LICENSE).\n',
    'author': 'Frederik F. Van der Veken',
    'author_email': 'frederik@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xsuite/xcoll',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
