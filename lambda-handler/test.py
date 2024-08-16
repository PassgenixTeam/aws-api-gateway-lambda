import json
from index import lambda_handler

event = json.load(open("event.json"))

result = lambda_handler(event, None)
print(result)
