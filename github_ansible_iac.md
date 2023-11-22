# Ansible Config stored in Github w/actions (IaC)

## Setup

Caveats:
- Setup a local runner [example](runner.md)
- Repo connected to the local runner (configure step in previous notes)

Create a new file in *.github/workflows/* example deploy.yml

```
name: Ansible Deploy

on:
    push:
        branches:
            - main

jobs:
    deploy:
        runs-on: "self-hosted"

        steps:
            - name: Checkout
              uses: actions/checkout@v2
        
            - name: Deploy yaml
              run: |
                scp *.yaml root@10.0.10.14:/root/

            - name: Deploy hosts
              run: |
                scp hosts root@10.0.10.14:/etc/ansible/hosts

```
The **runs-on** will specify to use your local runner. Checkout will checkout your code, obviously. Then you can run standard bash commands, example copy all yaml scripts from your repo to the /root directory or copy hosts file to /etc/ansible/hosts. This will make sure that your github repo and your ansible scripts remain in sync, each commit will trigger a deployment.

Example *hosts* file
```
[docker]
10.0.10.13

[vms]
10.0.10.11
10.0.10.13

[lxc]
10.0.10.14
10.0.10.15
10.0.10.20
10.0.10.21
10.0.10.22
10.0.10.23
10.0.10.24
10.0.10.25
10.0.10.26
10.0.10.27
10.0.10.28
10.0.10.29
10.0.10.30

[proxmox]
10.0.10.4
10.0.10.6
10.0.10.7

[truenas]
10.0.10.5
```

Example *yaml* file:
```
---
- hosts: lxc,vms
  become: yes
  tasks:
    - name: apt
      apt:
        update_cache: yes
        upgrade: 'yes'
    - name: Check if reboot required
      stat:
        path: /var/run/reboot-required
      register: reboot_required_file

    - name: Reboot if required
      reboot:
      when: reboot_required_file.stat.exists == true
```

## Troubleshooting

- Make sure you have accepted the fingerprint of the destination.
- Make sure you copied the ssh keys to the authorized_keys file on the destination