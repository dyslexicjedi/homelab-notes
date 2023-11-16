# Create a Nginx Reverse Proxy w/ WildCard Cert

Caveats 
- Proxmox LXC container 
- ubuntu 22.04 image
- Digital Ocean DNS 

## Certbot

Obviously:
```
apt update && apt upgrade -y
```

Install Certbot with Digital Ocean DNS
```
apt install python3-certbot-dns-digitalocean
```

Create a file called certbot-creds.ini (or anything really), inside is your token:
```
dns_digitalocean_token = 
```

Set permissions and run it
```
chmod 600 certbot-creds.ini 
certbot certonly --dns-digitalocean --dns-digitalocean-credentials ~/certbot-creds.ini -d '*.domain.com'
```

Success!!! You should get something similar to this output:
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/domain.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/domain.com/privkey.pem
This certificate expires on 2024-02-13.
```

## Nginx

Install 
```
apt install nginx
```

Create a file in /etc/nginx/sites-available/, example sonarr. Contains (replace ip and port obviously):
```
# Sonarr
server {
  listen 0.0.0.0:443 ssl;
  server_name sonarr.domain.com;

  include ssl.conf;

  location / {
    proxy_pass http://<ip>:<port>;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

Change directory to /etc/nginx/sites-enabled and do a symlink:
```
ln -s /etc/nginx/sites-available/sonarr sonarr
```

Restart nginx
```
systemctl restart nginx.service
```

Success!!!

### Issues
- Make sure your dns record for the domain is pointing to the reverse proxy. Example sonarr.domain.com pointing to 10.0.0.X 
- Changes aren't showing up yet, did you restart nginx? Make you you restart nginx whenever you make changes to your sites.
- Uptime won't work, add the following lines to the location in the site file:
```
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection "upgrade";

```
- nzbget won't work, add the following lines to the location in the site file
```
  # To allow POST on static pages
  error_page  405     =200 $uri;

```