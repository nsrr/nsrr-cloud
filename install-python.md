---
layout: default
title: Install Python
description: on windows, mac and linux systems
---
[Back to NSRR Cloud](./index.md)

[Install Python3.8 in Windows](#install-python38-in-windows)

[Install Python3.9 in mac](#install-python398-in-mac)

[Install Python3.9 in Linux](#install-python39-in-linux)




# Install python3.8 in Windows

It is highly recommended to use Python 3.8.x version only in Windows. To install Python3.8, visit [Python for Windows download](https://www.python.org/downloads/windows/){:target="_blank"} webpage and download Windows installer (32 or 64 bit) for version Python3.8.9

Double click on the downloaded installer and begin the installation process. 

Select customize installation:

![](./images/windows-1.png)

 Choose option 'pip' in Optional Features page

 Click Next 

![](./images/windows-2.png)


In Advanced Options page, choose option 'Add Python to environment variables'. Click on Install.

![](./images/windows-3.png)

Setup progress will be indicated in the installer.

![](./images/windows-4.png)


Finally an installation success message will show on successful installation.

![](./images/windows-5.png)



After the installation is completed, Open Powershell and run the command below to verify that Python is installed and added to path:

```
python
python -m pip
```

In case there are multiple versions of Python installed, the system will allow you to run specific Python version using:

```
py 3.8
py -3.8 -m pip
```


# Install Python3.9.8 in Mac

Since Mac systems are now available with two different Chip options - Intel and Apple Silicon, Python has upgraded their installer to be universal i.e., supporting both chip options. In accordance with that, we recommend using Python version 3.9.8 or above in Mac. 

```
brew install python@3.9 
```

The command above will install the latest stable version of Python 3.9. Run the command below to check if Python is successfully installed and added to the path:

```
python3
python3 -m pip
```

To manage multiple versions of Python in Mac, we recommend using a virtual environment. To learn more about virtual environment, visit [Python Virtual Envs](https://docs.python-guide.org/dev/virtualenvs/){:target="_blank"}.



## Install Python3.9 in Linux

If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.9 with the following commands:

```
sudo apt update
sudo apt install python3.9
sudo apt install python3-pip
```

Run the command below to check if Python is successfully installed:

```
python3
python3 -m pip
```

Note: In the example workflow described in this website, we will be using Ubuntu 20.x. 
