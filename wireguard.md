# Wireguard on LXC container (ubuntu)

## Setup Wireguard

Basics
```
apt update && apt upgrade -y && apt install wireguard qrencode
```

Generate Certs
```
wg genkey | tee /etc/wireguard/private.key

cat /etc/wireguard/private.key | wg pubkey | tee /etc/wireguard/public.key
```

wg0.conf (replace Address and eth0 if needed, insert your own PrivateKey)
```
[Interface]
Privatekey = <contents of private.key>
Address = 10.9.0.1/24
ListenPort = 51820
SaveConfig = true
PostUp = ufw route allow in on wg0 out on eth0
PostUp = iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
PostUp = ip6tables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
PreDown = ufw route delete allow in on wg0 out on eth0
PreDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PreDown = ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

/etc/sysctl.conf (add this at the end)
```
net.ipv4.ip_forward = 1
```

Update firewall and enable
```
ufw allow 51820/udp
ufw allow OpenSSH
ufw enable
ufw status
```

Start the Service
```
systemctl enable wg-quick@wg0.service
systemctl start wg-quick@wg0.service
systemctl status wg-quick@wg0.service
```
Success!!!!

## Setup Peer

Generate a new keypair for the peer device
```
wg genkey > laptop-private.key
wg pubkey < laptop-private.key > laptop-public.key
```

Update wg0.conf
```
[Peer]
# phone
PublicKey = <contents of laptop-public.key>
AllowedIPs = 10.9.0.2
```

Setup laptop.conf
```
[Interface]
PrivateKey = <contents of laptop-private.key>
Address = 10.9.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = <contents of public.key>
AllowedIPs = 0.0.0.0/0
Endpoint = <server ip>:51820
PersistentKeepalive = 15
```

Generate QR Code
```
qrencode -t png -o laptop.png -r laptop.conf
```

Success!!!