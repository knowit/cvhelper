# CV Browsing Application with CV Partner and LLM Integration

## Overview
This application is designed to streamline the process of browsing and analyzing CVs by integrating CV Partner's services with advanced Large Language Models (LLMs). It is a Knowit experiment.

## Installation

1. **Clone the Repository**
   ```
      git clone https://github.com/knowit/cvhelper.git
   ```
2. **Set up the Environment**
   - Install [poetry](https://python-poetry.org/).
   Using Python 3.11(chromadb does [not work with 3.12](https://github.com/chroma-core/chroma/issues/1410) as we speak).
   - Install required dependencies:
     ```
     poetry env use python3.11
     poetry install --no-root
     ```

3. **Configuration**
   If you are changing the defaults, you need to set the following environment-variables. 
   Defaults are set to local instances of Ollama, ChromaDB.
   ```
   export OLLAMA_URL="http://localhost:11434"
   export OLLAMA_MODEL="mistral"
   export CHROMA_HOST="localhost"
   export CHROMA_PORT="8080"
   export CVPARTNER_URL="https://knowit.cvpartner.com/api/v1/"
   export CVPARTNER_TOKEN="XXXX"
   ``````   

4. **Fire up the servers and a local chroma instance***

   ```
   poetry run python server.py
   ```

   ```
   poetry run chroma run --path ~/chroma_db_path
   ```

   Run a local ollama-server
   ```
   ollama pull mistral
   ollama serve
   ```

5. **Run the test-client***
   ```
   poetry run python client.py nnn@knowit.no "What projects has nnn worked on?"
   ```

## Populating chromadb vectorstore from cvpartner
   Run the script to fetch all cv's and populate the vectorstore.
   ```
   cd vectorstore
   poetry run python get_cv.py ~/Downloads/cvs
   ```

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
For support or any queries, reach out!


### Links
* [cvpartner API docs](https://docs.cvpartner.com/)
* [Langchain docs](https://api.python.langchain.com/en/latest/api_reference.html)
* Langchain serving: https://github.com/langchain-ai/langchain , https://github.com/langchain-ai/langserve
