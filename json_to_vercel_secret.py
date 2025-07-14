import json

def json_to_vercel_secret(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.replace('\n', '\\n')
    compact_json = json.dumps(data, separators=(',', ':'))

    print(compact_json)

json_to_vercel_secret('./yaari-dba-firebase-adminsdk-fbsvc-e9275c444b.json')
