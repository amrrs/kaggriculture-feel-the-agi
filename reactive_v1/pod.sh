#!/bin/bash
exec ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o ServerAliveInterval=30 -i $HOME/.ssh/id_ed25519 -p 40194 root@213.192.2.122 "$@"
