import requests
import os
import json
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
load_dotenv(dotenv_path)

headers = {'Authorization':'Bearer '+os.getenv("DIGITALOCEAN_TOKEN")}

ip = requests.get('https://api.ipify.org').content.decode('utf8')

url = "https://api.digitalocean.com/v2/domains/{}/records/{}".format(os.getenv("DIGITALOCEAN_DOMAIN"),os.getenv("DIGITALOCEAN_RECORDID"))

dns_info = requests.get(url,headers=headers).json()

dns_ip = dns_info['domain_record']['data']

if(ip == dns_ip):
    print("IP is correct")
else:
    print("Needs update")
    print("Current IP: {}".format(ip))
    print("DNS IP: {}".format(dns_ip))
    data = {"type":"A","data":ip}
    headers['Content-Type'] = "application/json"
    print(data)
    res = requests.put(url,data=json.dumps(data),headers=headers)
    if(res.status_code == 200):
        print("Updated")
    else:
        print("Update failed")
        print(res.content)

