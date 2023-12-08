# cvhelper

## Tasks
### Implement cvhelper functionallity
* Access vectorstore as client: `client = chromadb.HttpClient(host="localhost", port=8000)`
* Access vectorstore as client
* Filter queries to single CV based on email
* Use vectorstore client as document retriever
* Create QAChain with document retriever

### Deploy cvhelper API
* Create routes and app with FastAPI
* Test: Will each query have to create a new QAChain

### Links
* [cvpartner API docs](https://docs.cvpartner.com/)
* [Langchain docs](https://api.python.langchain.com/en/latest/api_reference.html)
* Langchain serving: https://github.com/langchain-ai/langchain , https://github.com/langchain-ai/langserve
* Example of using FastAPI (Norad case): https://github.com/openearthplatforminitiative/deforestation-api