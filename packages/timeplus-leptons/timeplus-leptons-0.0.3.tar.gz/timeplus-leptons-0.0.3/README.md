# leptons

leptons records all openAI api calls by adding an api hook that sends request/response to Timeplus cloud.

to install leptons, run `pip install timeplus-leptons`

to use leptons, refer to following sample code 

```
import os
import openai
from leptons import agent

# start the monitor agent of leptons
api_key = os.environ.get("TIMEPLUS_API_KEY")
api_address = os.environ.get("TIMEPLUS_ADDRESS")
agent = Agent(api_address=api_address, api_key=api_key)
agent.start()

# your open ai calls here
openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input}],
        temperature=temp
    )

```