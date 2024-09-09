# Get the result of the Dune query https://dune.com/queries/3674980
# and dump it to JSON
# You need to provide a Dune API key.

import json
from dune_client.client import DuneClient

dune = DuneClient("API KEY")
query_result = dune.get_latest_result(3674980)

print(query_result.state)

result = query_result.result.rows

with open('top_bytecodes.json', 'w') as f:
    json.dump(result, f)
