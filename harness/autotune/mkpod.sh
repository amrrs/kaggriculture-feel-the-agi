#!/bin/bash
# usage: mkpod.sh <name> "<flavor> <vcpu>" ...   (tries each spec until one is created)
KEY=$(tr -d '[:space:]' < ~/runpod.env); PUB=$(cat ~/.ssh/id_ed25519.pub); NAME=$1; shift
for spec in "$@"; do set -- $spec
  body=$(python3 -c "
import json,sys;print(json.dumps({'name':sys.argv[4],'imageName':'runpod/base:1.3.3-ubuntu2404','computeType':'CPU','cpuFlavorIds':[sys.argv[2]],'vcpuCount':int(sys.argv[3]),'containerDiskInGb':30,'ports':['22/tcp'],'env':{'PUBLIC_KEY':sys.argv[1]},'cloudType':sys.argv[5]}))" "$PUB" $1 $2 $NAME ${CLOUD:-SECURE})
  r=$(curl -s -m 60 -X POST https://rest.runpod.io/v1/pods -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" -d "$body" | python3 -c "import sys,json;d=json.load(sys.stdin);print({k:d.get(k) for k in ['id','costPerHr','vcpuCount','error']} if isinstance(d,dict) else d)")
  echo "$spec -> $r"; case "$r" in *"'id': '"*) exit 0;; esac
done
