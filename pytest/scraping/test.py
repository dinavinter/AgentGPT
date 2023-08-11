import json, jsonpath_ng

with open("test.json", "r") as json_file:
  json_data = json.load(json_file)

jsonpath_expr = jsonpath_ng.parse("$..country")
extracted_data = jsonpath_expr.find(json_data)

for match in extracted_data:
  print(f"The country data is {match.value}")
