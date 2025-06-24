import json

with open("kommo-monitor-leads-59a7059d575f.json", "r") as f:
    data = json.load(f)
    escaped = json.dumps(data)
    print(escaped)
