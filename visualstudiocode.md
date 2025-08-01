# Install VSCode from tar.gz

Download the correct tar.gz file from their website [here](https://code.visualstudio.com/Download#). 

## unpack

```
tar -xvzf code-stable-x64-1753759483.tar.gz
```

## Move it

```
sudo mv VSCode-linux-x64/ /usr/share/code
```

## Sym Link it

```
sudo ln -s /usr/share/code/bin/code /usr/bin/code
```

Done.