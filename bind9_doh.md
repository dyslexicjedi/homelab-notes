# Setting up DOH (DNS over HTTPS) with Bind9

Goal: To setup an internal DNS server to my network that will send DOH requests to Quad9. Comcast has been intercepting DNS traffic and rerouting it to their DNS server. This has caused at least one site not to load unlike the public internet. 

## DOH Setup
We are going to use Stubby as our forwarder. More info [here](https://dnsprivacy.org/dns_privacy_daemon_-_stubby/). 

Basics:
```
sudo apt update && sudo apt upgrade -y && apt install stubby
```

Now configure stubby */etc/stubby/stubby.yml*
```
resolution_type: GETDNS_RESOLUTION_STUB
dns_transport_list: 
  - GETDNS_TRANSPORT_TLS
tls_authentication: GETDNS_AUTHENTICATION_REQUIRED
tls_query_padding_blocksize: 256
edns_client_subnet_private : 1
idle_timeout: 10000
listen_addresses:
  - 127.0.0.1@5453
  -  0::1@5453
round_robin_upstreams: 1
upstream_recursive_servers:
  - address_data: 9.9.9.9
    tls_auth_name: "dns.quad9.net"
  - address_data: 149.112.112.112
    tls_auth_name: "dns.quad9.net"
```

This will use quad9 as our resolver and we are binding it to port 5453 (to prevent issues with bind9 running on port 53).

Make sure stubby is started and running:

```
sudo systemctl enable stubby
sudo systemctl restart stubby
```

Now let's test it:

```
dig @127.0.0.1 -p 5453 google.com
```

Success!!!


## Bind9 Setup

Basics:
```
sudo apt update && sudo apt upgrade -y && apt install bind9 bind9utils bind9-doc
```

Now setup */etc/bind/named.conf.options*
```
acl "trusted" {
        127.0.0.0/24;
        10.0.0.0/24;
        10.0.10.0/24;
};

options {
        directory "/var/cache/bind";

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0's placeholder.

        recursion yes;
        allow-query { trusted; };
        allow-transfer { none; };

        forwarders {
                127.0.0.1 port 5453;
         };

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation auto;

        listen-on-v6 { any; };

};
```

Obviously you need to change the IPs in the ACL to match your network. But you need to keep localhost (127.0.0.0/24) in the ACL or it will reject the records. Ask me how I know....

Now restart bind9

```
sudo systemctl restart bind9
```


Now test it:

```
dig @127.0.0.1  google.com
```

Success!!!