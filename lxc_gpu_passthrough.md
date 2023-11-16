# LXC GPU Passthrough on Proxmox

Caveats
- proxmox
- lxc
- nvidia gpu installed on proxmox

## Get GPU and Groups info

Verify **nvidia-smi** works (example output):
```
Thu Nov 16 10:04:41 2023       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Quadro P2000                   Off | 00000000:3E:00.0 Off |                  N/A |
| 71%   39C    P0              17W /  75W |      0MiB /  5120MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
```

Get groups, (in this case 195 511 236 and 226):
```
root@newton:/dev# ls -lh nvidia*
crw-rw-rw- 1 root root 195,   0 Nov 16 10:04 nvidia0
crw-rw-rw- 1 root root 195, 255 Nov 16 10:04 nvidiactl
crw-rw-rw- 1 root root 511,   0 Nov 16 10:04 nvidia-uvm
crw-rw-rw- 1 root root 511,   1 Nov 16 10:04 nvidia-uvm-tools

nvidia-caps:
total 0
cr-------- 1 root root 236, 1 Nov 16 10:04 nvidia-cap1
cr--r--r-- 1 root root 236, 2 Nov 16 10:04 nvidia-cap2

```
```
root@newton:/dev# ls -lh dri
total 0
drwxr-xr-x 2 root root         80 Oct  3 17:19 by-path
crw-rw---- 1 root video  226,   0 Oct  3 17:19 card0
crw-rw---- 1 root render 226, 128 Oct  3 17:19 renderD128
```
```
root@newton:/dev# ls -lh nvidia-caps*
total 0
cr-------- 1 root root 236, 1 Nov 16 10:04 nvidia-cap1
cr--r--r-- 1 root root 236, 2 Nov 16 10:04 nvidia-cap2

```

## Edit the LXC config

Edit the config of the lxc container (example 101)
**/etc/pve/local/lxc/101.conf**

```
lxc.cgroup2.devices.allow: c 226:* rwm
lxc.cgroup2.devices.allow: c 195:* rwm
lxc.cgroup2.devices.allow: c 505:* rwm
lxc.cgroup2.devices.allow: c 508:* rwm
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/nvidia0 dev/nvidia0 none bind,optional,create=file
lxc.mount.entry: /dev/nvidiactl dev/nvidiactl none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm dev/nvidia-uvm none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm-tools dev/nvidia-uvm-tools none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-caps dev/nvidia-caps none bind,optional,create=dir
```

## In the LXC container
Match the driver version to the version on the proxmox server, in my case 535

```
apt update && apt upgrade -y
apt install nvidia-utils-535-server libnvidia-encode-535-server
```

Let's check it:

```
root@jellyfin:~# nvidia-smi
Thu Nov 16 15:26:15 2023       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Quadro P2000                   Off | 00000000:3E:00.0 Off |                  N/A |
| 69%   37C    P0              17W /  75W |      0MiB /  5120MiB |      2%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+

```

Success!!!

### Issues
- Make sure the nvidia version on the proxmox server and inside the lxc container is the same. Example 535.129.03 (full version must match, not just major version)