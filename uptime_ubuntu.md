# Install Uptime on ubuntu LXC Container

Caveat:
- ubuntu 22.04
- lxc proxmox

## Install Node

Obviously
```
apt update && apt upgrade -y && apt install curl
```

Get Node 18
```
curl -sL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh
bash /tmp/nodesource_setup.sh
```

Install nodejs git-all
```
 apt install nodejs git-all -y
```

Install deps
```
npm install npm -g
npm install pm2 -g
pm2 install pm2-logrotate
```

Get Uptime code and run setup
```
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma/
npm run setup
```

Test (test on port 3001)
```
node server/server.js
```

Run at startup
```
pm2 start server/server.js --name uptime-kuma
pm2 save && pm2 startup
```

Success!!!