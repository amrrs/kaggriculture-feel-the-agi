#!/bin/bash
# usage: podip.sh <pod_id>  -> prints "ip port" of the 22/tcp mapping (REST GET; key never printed)
KEY=$(tr -d '[:space:]' < ~/runpod.env)
curl -s -m 30 https://rest.runpod.io/v1/pods/$1 -H "Authorization: Bearer $KEY" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('publicIp'), (d.get('portMappings') or {}).get('22'), d.get('desiredStatus'))"
