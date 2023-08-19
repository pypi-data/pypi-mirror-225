# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiwi_booster',
 'kiwi_booster.common_utils',
 'kiwi_booster.gcp_utils',
 'kiwi_booster.ml_utils']

package_data = \
{'': ['*']}

install_requires = \
['black[d]>=22.1.0,<23.0.0',
 'google-auth>=2.18.0,<3.0.0',
 'google-cloud-bigquery>=3.10.0,<4.0.0',
 'google-cloud-secret-manager>=2.16.1,<3.0.0',
 'google-cloud-storage>=2.9.0,<3.0.0',
 'google-crc32c>=1.5.0,<2.0.0',
 'slack-sdk>=3.21.3,<4.0.0',
 'structlog>=23.1.0,<24.0.0']

setup_kwargs = {
    'name': 'kiwi-booster',
    'version': '0.2.1',
    'description': 'Python utility functions and classes for KiwiBot AI&Robotics team',
    'long_description': '<div id="top"></div>\n\n<!-- PROJECT LOGO -->\n\n<br />\n<div align="center">\n  <a href="https://github.com/kiwicampus/kiwi-booster">\n    <img src="https://user-images.githubusercontent.com/26184787/227988899-7192c613-c651-4f45-ae9a-8dea254ccaca.png" alt="Logo" width="200" height="200">\n  </a>\n<h3 align="center"><font size="8">Kiwi Booster</font></h3>\n\n<p align="center">\n    Python utils and classes for KiwiBot AI&Robotics team<br>\n    <a href="https://github.com/kiwicampus/kiwi-booster/pulls">Make a Pull Request</a>\n    ·\n    <a href="https://github.com/kiwicampus/kiwi-booster/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/kiwicampus/kiwi-booster/issues">Request Feature</a>\n</p>\n\n</div>\n\n---\n\n<!-- TABLE OF CONTENTS -->\n\n### Table of contents\n\n- [About The Project](#about-the-project)\n- [Getting started](#getting-started)\n  - [Installation](#installation)\n  - [Usage](#usage)\n- [Contributing](#contributing)\n  - [License](#license)\n  - [Contact](#contact)\n\n---\n\n<!-- ABOUT THE PROJECT -->\n\n## About The Project\n\nThis library contains utility functions and classes from Python that are commonly used in the AI&Robotics team. It is divided into 5 main sections:\n\n- **common_utils**: Some common utils that are normally used in most of the projects.\n  \n  - kiwi_booster.loggers\n    This module contains GCP and local loggers with a predefined format.\n  \n  - kiwi_booster.mixed\n    This module contains miscellaneous utils from multiple objectives.\n  \n  - kiwi_booster.requests\n    This module contains utils for working with HTTP requests.\n\n- **gcp_utils**: Utils that are related to the Google Cloud Platform.\n  \n  - kiwi_booster.gcp_utils.bigquery\n    This module contains utils for working with BigQuery.\n  \n  - kiwi_booster.gcp_utils.kfp\n    This module contains utils for working with Vertex (Kubeflow) Pipelines.\n  \n  - kiwi_booster.gcp_utils.secrets\n    This module contains utils for working with Google Cloud Secrets Manager.\n  \n  - kiwi_booster.gcp_utils.storage\n    This module contains utils for working with Google Cloud Storage.\n\n- **ml_utils**: Utils that are related to Machine Learning.\n  \n  - kiwi_booster.ml_utils.benchmarks\n    This module contains utils for benchmarking machine learning models.\n  \n  - kiwi_booster.ml_utils.prediction\n    This module contains utils to handle the prediction of the semantic segmentation model.\n\n- **decorators**: Decorators that are used to improve the codebase.\n\n- **slack_utils**: Utils that are related to Slack.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n---\n\n<!-- GETTING STARTED -->\n\n## Getting started\n\n### Installation\n\nTo install the package, simply run the following command:\n\n```sh\npip install kiwi-booster\n```\n\n### Usage\n\nTo use the package, we recommend using relative imports for each function or class you want to import to improve readability. For example, if you want to use the `SlackBot` class, you can import it as follows:\n\n```python\nfrom kiwi_booster.slack_utils import SlackBot\n\nslack_bot = SlackBot(\n        SLACK_TOKEN,\n        SLACK_CHANNEL_ID,\n        SLACK_BOT_IMAGE_URL,\n        image_alt_text="Bot description",\n)\n```\n\nOr any decorator as follows:\n\n```python\nfrom kiwi_booster.decorators import try_catch_log\n\n@try_catch_log\ndef my_function():\n    # Do something\n```\n\nAs well, we recommend importing them in a separate section from the rest of the imports.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n---\n\n<!-- CONTRIBUTING -->\n\n## Contributing\n\nIf you\'d like to contribute to Kiwi Booster, please feel free to submit a pull request! We\'re always looking for ways to improve our codebase and make it more useful to a wider range of use cases. You can also request a new feature by submitting an issue.\n\n### License\n\nKiwi Booster is licensed under the GNU license. See the LICENSE file for more information.\n\n### Contact\n\nSebastian Hernández Reyes - Machine Learning Engineer - [Mail contact](mailto:juan.hernandez@kiwibot.com)\n\nCarlos Alvarez - Machine Learning Engineer Lead - [Mail contact](mailto:carlos.alvarez@kiwibot.com)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- Template developed by the ML Team :D-->\n',
    'author': 'Sebastian Hernandez',
    'author_email': 'juan.hernandez@kiwibot.con',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
