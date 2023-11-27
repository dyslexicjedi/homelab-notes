# DNS Update Script

Caveat
- DigitalOcean DNS
- Ubuntu LXC (or VM)

## Setup

Basics
```
apt update && apt upgrade -y && python3-requests python3-dotenv
```

## Script

Linked [here](update_vpn_ip.py)

Example .env file:
```
DIGITALOCEAN_TOKEN=<your token>
DIGITALOCEAN_DOMAIN=<your domain>
DIGITALOCEAN_RECORDID=<domain id>
```

## Crontab

I'm doing every 30 minutes...

```
*/30 * * * * cd /path && python3 /path/update_vpn_ip.py
```

Success!