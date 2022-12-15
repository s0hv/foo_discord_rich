import requests
import sys

url = "https://api.imgur.com/3/image"

sys.stdin.reconfigure(encoding='utf-8')
filename = sys.stdin.read().strip()
client_id = 'Insert imgur api client id here'

headers = {
    'Authorization': f'Client-ID {client_id}'
}

with open(filename, 'rb') as f:
    r = requests.post(url, headers=headers, files={
        'image': f
    })

if not r.ok:
    print(r.text[:1000])
    exit(1)

print(r.json()['data']['link'], end='')
