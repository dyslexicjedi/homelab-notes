# Setup Nvidia GPU on Proxmox

Caveats
- Proxmox
- Nvidia GPU

## Verify you see the device via SSH

```
root@newton:~# lspci -nn | grep -i nvidia
3e:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP106GL [Quadro P2000] [10de:1c30] (rev a1)
3e:00.1 Audio device [0403]: NVIDIA Corporation GP106 High Definition Audio Controller [10de:10f1] (rev a1)
```

Downloads the appropriate drivers, I'm currently using 535 from here:
**https://www.nvidia.com/en-us/drivers/unix/**


This is me.
```
Linux x86_64/AMD64/EM64T
Latest Production Branch Version: 535.129.03
```

## Install drivers

Get Kernal version
```
root@newton:~# uname -a
Linux newton 6.2.16-12-pve #1 SMP PREEMPT_DYNAMIC PMX 6.2.16-12 (2023-09-04T13:21Z) x86_64 GNU/Linux

```

Install with the correct linux header location
```
root@newton:~# chmod +x NVIDIA-Linux-x86_64-535.129.03.run 
root@newton:~# ./NVIDIA-Linux-x86_64-535.129.03.run --kernel-source-path /usr/src/linux-headers-6.2.16-12-pve --dkms
```

Follow the onscreen prompts.

Now verify
```
root@newton:~# nvidia-smi
Thu Nov 16 10:26:09 2023       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Quadro P2000                   Off | 00000000:3E:00.0 Off |                  N/A |
| 69%   37C    P0              17W /  75W |      0MiB /  5120MiB |      1%      Default |
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

Success!!!!