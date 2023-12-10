# CV Browsing Application with CV Partner and LLM Integration

## Overview
This application is designed to streamline the process of browsing and analyzing CVs by integrating CV Partner's services with advanced Large Language Models (LLMs). It is a Knowit experiment.

## Installation

1. **Clone the Repository**

2. **Set up the Environment**
   - Ensure Python 3.11 is installed (chromadb does [not work with 3.12](https://github.com/chroma-core/chroma/issues/1410) as we speak).
   - Install required dependencies:
     \```
     pip install -r requirements.txt
     \```

3. **Configuration**
   - Set up your `config.json` with necessary API keys and settings.

4. **Run the test-client***
   \```
   python app.py
   \```

## Contributing

We welcome contributions to this project. If you want to contribute, please follow these steps:
- Fork the repository.
- Create a new branch for your feature.
- Commit your changes.
- Push to the branch.
- Open a pull request.

## License

Apache 2.0

## Contact

For support or any queries, reach out to us!
"""

### Links
* [cvpartner API docs](https://docs.cvpartner.com/)
* [Langchain docs](https://api.python.langchain.com/en/latest/api_reference.html)
* Langchain serving: https://github.com/langchain-ai/langchain , https://github.com/langchain-ai/langserve
