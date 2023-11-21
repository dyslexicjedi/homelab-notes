# Setting up a local github runner

## github runner

Note: Local runners are supported by individual repo or by org, you can't have a runner for all your repos. Weird. So I created a org and put a repo in there, this will allow me to use the same runner for other projects in the future. 

I basically started by following the github guide found [here](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners). 

```
apt update && apt upgrade -y && apt install curl
```
Create a user account, can be called anything. I used "gh" (since lxc's start as root)

```
#Create User
useradd -m gh
#Set password
passwd gh
#add to sudoers
usermod -aG sudo gh
#Change to User
su gh -
```


```
mkdir actions-runner && cd actions-runner

#Get package
curl -o actions-runner-linux-x64-2.309.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-x64-2.309.0.tar.gz

#Verify install
echo "2974243bab2a282349ac833475d241d5273605d3628f0685bd07fb5530f9bb1a  actions-runner-linux-x64-2.309.0.tar.gz" | shasum -a 256 -c

#Extract it
tar xzf ./actions-runner-linux-x64-2.309.0.tar.gz

#Configure it
./config.sh --url https://github.com/jedihomelab --token <redacted>

```
Run it

```
./run.sh
```
Success!!

Now let's make it a service

```
sudo ./svc.sh install
sudo systemctl enable actions.runner.jedihomelab.lxc
sudo systemctl start actions.runner.jedihomelab.lxc
sudo systemctl status actions.runner.jedihomelab.lxc
```

Done!
