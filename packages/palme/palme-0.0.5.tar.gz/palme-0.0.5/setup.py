# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palme', 'palme.core']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'matplotlib',
 'numpy',
 'torch',
 'transformers']

setup_kwargs = {
    'name': 'palme',
    'version': '0.0.5',
    'description': 'palme - Pytorch',
    'long_description': '# 🌴 PALM-E: A Multi-Modal AI Model \n\nThis is the open source implementation of the SOTA multi-modality foundation model "PaLM-E: An Embodied Multimodal Language Model" from Google, PALM-E is a single large embodied multimodal model, that can address a variety of embodied reasoning tasks, from a variety of observation modalities, on multiple embodiments, and further, exhibits positive transfer: the model benefits from diverse joint training across internet-scale language, vision, and visual-language domains.\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/PALM-E)](https://github.com/kyegomez/PALM-E/issues) \n[![GitHub forks](https://img.shields.io/github/forks/kyegomez/PALM-E)](https://github.com/kyegomez/PALM-E/network) \n[![GitHub stars](https://img.shields.io/github/stars/kyegomez/PALM-E)](https://github.com/kyegomez/PALM-E/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/PALM-E)](https://github.com/kyegomez/PALM-E/blob/master/LICENSE)\n[![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/PALM-E)](https://twitter.com/intent/tweet?text=Excited%20to%20introduce%20PALM-E,%20the%20all-new%20robotics%20model%20with%20the%20potential%20to%20revolutionize%20automation.%20Join%20us%20on%20this%20journey%20towards%20a%20smarter%20future.%20%23RT1%20%23Robotics&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E)\n[![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E)\n[![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E&title=Introducing%20PALM-E%2C%20the%20All-New%20Robotics%20Model&summary=PALM-E%20is%20the%20next-generation%20robotics%20model%20that%20promises%20to%20transform%20industries%20with%20its%20intelligence%20and%20efficiency.%20Join%20us%20to%20be%20a%20part%20of%20this%20revolutionary%20journey%20%23RT1%20%23Robotics&source=)\n![Discord](https://img.shields.io/discord/999382051935506503)\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E&title=Exciting%20Times%20Ahead%20with%20PALM-E%2C%20the%20All-New%20Robotics%20Model%20%23RT1%20%23Robotics) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E&t=Exciting%20Times%20Ahead%20with%20PALM-E%2C%20the%20All-New%20Robotics%20Model%20%23RT1%20%23Robotics)\n[![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=PALM-E%2C%20the%20Revolutionary%20Robotics%20Model%20that%20will%20Change%20the%20Way%20We%20Work%20%23RT1%20%23Robotics)\n[![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=I%20just%20discovered%20PALM-E,%20the%20all-new%20robotics%20model%20that%20promises%20to%20revolutionize%20automation.%20Join%20me%20on%20this%20exciting%20journey%20towards%20a%20smarter%20future.%20%23RT1%20%23Robotics%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2FPALM-E)\n\n\n\n## 🚀 Quick Start\n\n### Installation 📦\n\n```sh\npip install palme\n```\n\n### Usage 🎨\n\n```python\nimport torch\nfrom palme import PalmE\n\n#usage\nimg = torch.randn(1, 3, 256, 256)\ncaption_tokens = torch.randint(0, 4)\n\nmodel = PalmE()\noutput = model(img, caption_tokens)\n\n```\n---\n\n## Contribute || Be Part of the PALM-E Adventure 🤝\n\nYour brilliance is needed! Join us, and together, let\'s make PALM-E even more awe-inspiring:\n\n1. **Get Your Copy**: Fork the PALM-E repo.\n2. **Make It Local**: Clone your fork.\n3. **Prep Your Tools**: Install the necessities.\n4. **Discover & Innovate**: Dive into the code.\n5. **Craft Your Magic**: Branch and code away.\n6. **Show & Tell**: Push your changes and craft a pull request.\n\n🐞 Fixes, 🎨 enhancements, 📝 docs, or 💡 ideas – all are welcome! Let\'s shape the future of AI, hand in hand.\n\n## Roadmap\n\n- 🕵️ Verify decoder configurations.\n- 🚂 Recreate the training strategy detailed in the paper.\n- 🌐 Train on the datasets used in the paper.\n\n## 📘 Documentation\n* Documentation will come soon\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/palme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
