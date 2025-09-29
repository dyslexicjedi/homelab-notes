# NAS Server (einstein)

## Base
- https://www.linuxserver.io/blog/2017-06-24-the-perfect-media-server-2017
- https://bitbysystems.com/unraid-data-disks-on-linux-with-mergerfs/
- [fstab](einstein/fstab)
- [crontab](einstein/crontab)

## Node-Exporter
- https://jaanhio.me/blog/linux-node-exporter-setup/
- https://prometheus.io/docs/guides/node-exporter/

Systemd service
```
sudo useradd -m node_exporter
sudo groupadd node_exporter
sudo usermod -a -G node_exporter node_exporter
```

node_exporter.service
```
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/sbin/node_exporter

[Install]
WantedBy=multi-user.target
```

## Snapraid
- https://diymediaserver.com/post/master-the-basics-how-to-install-snapraid/#installing-snapraid
- https://github.com/ironicbadger/ansible/blob/master/roles/epsilon/files/etc/snapraid.conf
- [snapraid](einstein/snapraid.conf)
