# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slackblocks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slackblocks',
    'version': '0.9.10',
    'description': 'Python wrapper for the Slack Blocks API',
    'long_description': '# slackblocks <img src="https://github.com/nicklambourne/slackblocks/raw/master/docs/img/sb.png" align="right" width="250px"/>\n\n![PyPI - License](https://img.shields.io/pypi/l/slackblocks)\n![Python Versions](https://img.shields.io/pypi/pyversions/slackblocks)\n![PyPI](https://img.shields.io/pypi/v/slackblocks?color=yellow&label=PyPI&logo=python&logoColor=white)\n[![Downloads](https://pepy.tech/badge/slackblocks)](https://pepy.tech/project/slackblocks)\n[![Build Status](https://github.com/nicklambourne/slackblocks/actions/workflows/unit-tests.yml/badge.svg?branch=master)](https://github.com/nicklambourne/slackblocks/actions)\n\n## What is it?\n\n`slackblocks` is a Python API for building messages in the fancy Slack Block Kit API.\n\nIt was created by [Nicholas Lambourne](https://github.com/nicklambourne) for the [UQCS Slack Bot](https://github.com/UQComputingSociety/uqcsbot) because he hates writing JSON, naturally this project has subsequently involved writing more JSON than if he\'d done the original task by hand.\n\n## Requirements\n`slackblocks` requires Python >= 3.7.\n\nAs of version 0.1.0 it has no dependencies outside the Python standard library.\n\n## Installation\n\n```bash\npip install slackblocks\n```\n\n## Usage\n\n```python\nfrom slackblocks import Message, SectionBlock\n\n\nblock = SectionBlock("Hello, world!")\nmessage = Message(channel="#general", blocks=block)\nmessage.json()\n\n```\n\nWill produce the following JSON string:\n```json\n{\n    "channel": "#general",\n    "mrkdwn": true,\n    "blocks": [\n        {\n            "type": "section",\n            "block_id": "992ceb6b-9ad4-496b-b8e6-1bd8a632e8b3",\n            "text": {\n                "type": "mrkdwn",\n                "text": "Hello, world!"\n            }\n        }\n    ]\n}\n```\nWhich can be sent as payload to the Slack message API HTTP endpoints.\n\nOf more practical uses is the ability to unpack the objects directly into \nthe Python Slack Client in order to send messages:\n```python\nfrom os import environ\nfrom slack import WebClient\nfrom slackblocks import Message, SectionBlock\n\n\nclient = WebClient(token=environ["SLACK_API_TOKEN"])\nblock = SectionBlock("Hello, world!")\nmessage = Message(channel="#general", blocks=block)\n\nresponse = client.chat_postMessage(**message)\n```\n\nNote the `**` operator in front of the `message` object.\n\n## Can I use this in my project?\n\nYes, please do! The code is all open source and BSD-3.0 licensed.\n',
    'author': 'Nicholas Lambourne',
    'author_email': 'dev@ndl.im',
    'maintainer': 'Nicholas Lambourne',
    'maintainer_email': 'dev@ndl.im',
    'url': 'https://github.com/nicklambourne/slackblocks',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0',
}


setup(**setup_kwargs)
