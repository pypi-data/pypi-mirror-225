# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d8analysis',
 'd8analysis.data',
 'd8analysis.qualitative',
 'd8analysis.quantitative',
 'd8analysis.quantitative.descriptive',
 'd8analysis.quantitative.inferential',
 'd8analysis.quantitative.inferential.centrality',
 'd8analysis.quantitative.inferential.distribution',
 'd8analysis.quantitative.inferential.relational',
 'd8analysis.service',
 'd8analysis.visual',
 'd8analysis.visual.seaborn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'd8analysis',
    'version': '0.1.5',
    'description': 'Exploratory Data Analysis Framework',
    'long_description': "# d8analysis - An Exploratory Data Analysis Framework\n\n[![PyPI](https://img.shields.io/pypi/v/d8analysis?style=flat-square)](https://pypi.python.org/pypi/d8analysis/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/d8analysis?style=flat-square)](https://pypi.python.org/pypi/d8analysis/)\n[![PyPI - License](https://img.shields.io/pypi/l/d8analysis?style=flat-square)](https://pypi.python.org/pypi/d8analysis/)\n\n---\n\n**Documentation**: [https://john-james-ai.github.io/d8analysis](https://john-james-ai.github.io/d8analysis)\n\n**Source Code**: [https://github.com/john-james-ai/d8analysis](https://github.com/john-james-ai/d8analysis)\n\n**PyPI**: [https://pypi.org/project/d8analysis/](https://pypi.org/project/d8analysis/)\n\n---\n\nExploratory Data Analysis Framework\n\n## Installation\n\n```sh\npip install d8analysis\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/john-james-ai/d8analysis/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/john-james-ai/d8analysis/releases) and publish it. When\n a release is published, it'll trigger [release](https://github.com/john-james-ai/d8analysis/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n",
    'author': 'John James',
    'author_email': 'john.james.ai.studio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://john-james-ai.github.io/d8analysis',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
