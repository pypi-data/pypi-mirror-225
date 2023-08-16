# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_newsapi_connector']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.5.1', 'pycountry==22.3.5', 'requests==2.31.0', 'streamlit==1.25.0']

setup_kwargs = {
    'name': 'st-newsapi-connector',
    'version': '0.1.2',
    'description': 'A Python package to query data from NewsAPI in Streamlit apps',
    'long_description': '# 📰 Streamlit-NewsAPI Data Connector\n\nConnect to [NewsAPI](https://newsapi.org/) from your Streamlit app. Powered by ```st.experimental_connection()```. Works with Streamlit >= 1.22. Read more about Streamlit Connections in the [official docs](https://blog.streamlit.io/introducing-st-experimental_connection/). \n\nContributions to this repo are welcome. If you are interested in helping to maintain it, reach out to us. \n\n[![Made_withPython](https://img.shields.io/badge/Made%20With-Python-blue?logo=Python)](https://www.steamlit.io/)\n[![Made_withNewsAPI](https://img.shields.io/badge/Made%20With-NewsAPI-lightblue)](https://newsapi.org/)\n[![Open_inStreamlit](https://img.shields.io/badge/Open%20In-Streamlit-red?logo=Streamlit)](https://st-newsapi-connector.streamlit.app/)\n\n[![CodeFactor](https://www.codefactor.io/repository/github/dcarpintero/st-newsapi-connector/badge)](https://www.codefactor.io/repository/github/dcarpintero/st-newsapi-connector)\n\n## 🚀 Quickstart\n\n1. Clone the repository:\n```\ngit clone git@github.com:dcarpintero/st-newsapi-connector.git\n```\n\n2. Create and Activate a Virtual Environment:\n\n```\nWindows:\n\npy -m venv .venv\n.venv\\scripts\\activate\n\nmacOS/Linux\n\npython3 -m venv .venv\nsource .venv/bin/activate\n```\n\n3. Install dependencies:\n\n```\npip install -r requirements.txt\n```\n\n4. Launch Web Application\n\n```\nstreamlit run ./app.py\n```\n\n## 📄 Minimal Integration\n\n```python\n# src/app.py\n\nimport streamlit as st\nfrom newsapi.connection import NewsAPIConnection\n\nconn_newsapi = st.experimental_connection("NewsAPI", type=NewsAPIConnection)\n\n# Retrieves News Articles on a specific topic from the NewsAPI\ndf = conn_newsapi.everything(topic="ChatGPT")\nst.dataframe(df)\n\n# Retrieves Top-Headlines in a country and category from the NewsAPI\ndf = conn_newsapi.top_headlines(country=\'US\', category=\'Science\')\nst.dataframe(df)\n```\n\n```toml\n# .streamlit/secrets.toml\n\nNEWSAPI_KEY = \'your-newsapi-key\'\nNEWSAPI_BASE_URL = \'https://newsapi.org/v2/\'\n```\n\n```txt\n# requirements.txt\n\npandas==1.5.1\npycountry==22.3.5\npytest==7.4.0\nrequests==2.31.0\nstreamlit==1.25.0\n```\n\n## 👩\u200d💻 Streamlit Web App\n\nDemo Web App deployed to [Streamlit Cloud](https://streamlit.io/cloud) and available at https://newsapi-connector.streamlit.app/ \n\n![WebApp](./assets/st-newsapi-connector.png)\n\n## 📚 References\n\n- [Experimental BaseConnection](https://docs.streamlit.io/library/api-reference/connections/st.connections.experimentalbaseconnection)\n- [Experimental Connection](https://blog.streamlit.io/introducing-st-experimental_connection/)\n- [Get Started with Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started)\n- [NewsAPI Dcoumentation](https://newsapi.org/docs)\n\n',
    'author': 'D. Carpintero',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://st-newsapi-connector.streamlit.app/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
