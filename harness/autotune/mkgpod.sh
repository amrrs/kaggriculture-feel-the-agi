#!/bin/bash
# usage: mkgpod.sh <name> <minVcpu> <cloud> "<gpuTypeId>" ...  (GPU pod used for its CPUs; tries each until created)
KEY=$(tr -d '[:space:]' < ~/runpod.env); PUB=$(cat ~/.ssh/id_ed25519.pub); NAME=$1; V=$2; CL=$3; shift 3
for g in "$@"; do
  body=$(python3 -c "
import json,sys;print(json.dumps({'name':sys.argv[2],'imageName':'runpod/base:1.3.3-ubuntu2404','computeType':'GPU','gpuTypeIds':[sys.argv[3]],'gpuCount':1,'minVCPUPerGPU':int(sys.argv[4]),'containerDiskInGb':30,'ports':['22/tcp'],'env':{'PUBLIC_KEY':sys.argv[1]},'cloudType':sys.argv[5]}))" "$PUB" $NAME "$g" $V $CL)
  r=$(curl -s -m 60 -X POST https://rest.runpod.io/v1/pods -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" -d "$body" | python3 -c "import sys,json;d=json.load(sys.stdin);print({k:d.get(k) for k in ['id','costPerHr','vcpuCount','error']} if isinstance(d,dict) else d)")
  echo "$g -> $r"; case "$r" in *"'id': '"*) exit 0;; esac
done
exit 1
