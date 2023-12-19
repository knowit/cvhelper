"""A simple python script that can be run in the terminal to invoke the cvhelper API.

The script should be run with two arguments:
1. the email to select the CV
2. the prompt
"""

from langserve import RemoteRunnable
from settings import settings
import sys

email = sys.argv[1]
prompt = sys.argv[2]

host = "localhost"
cv_ai = RemoteRunnable(
    f"http://{settings.cvhelper_host}:{settings.cvhelper_port}/cv-helper"
)

res = cv_ai.invoke(
    {
        "query": prompt,
        "email": email,
    }
)
print(res["result"])
