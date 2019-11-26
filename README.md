# YubiKey4Linux
An easy-to-use Yubikey installation tool for Ubuntu (and other Debian Distros)  

## Project Overview
Yubikey is a portable USB based biometric authentication device developed by Yubico that provides secure login and authentication to a variety of popular services and platforms. It provides intuitive installation processes for some popular platforms such as Windows and Google Account, but installation process for Linux still remains complicated. This project aims to bring easy and convenient installation to Ubuntu, one of the most popular distribution of Debian Linux.  

## Software Execution and Build
*With Python 3.7, the tool can be executed through `dev.py`.  
*Without Python, the pre-build can be found at `dist/dev`.  

The tool can be built from python to independent packages using
```pyinstaller --add-data 'cmd:.' dev.py```
or to single file using
```pyinstaller -F dev.py```
```cp cmd ./dist/```

### Dependencies for Building
Any version of Ubuntu, Python 3.7, Pyinstall. Anaconda Python management platform in preferred.  

## Official Practices and Limitations

The current method of installing Yubikey to Ubuntu requires multiple steps involving terminal commands, testing and configuring YubiKey, and finally enabling YubiKey. The whole process will take a long time and several system files will be touched and modified along the way. If configured improperly, system and root privileges may be locked and cannot properly function without system re-imaging.  

## Proposed Approach and Advantage

The aim of this project is to streamline the complex solution in order to make the setup as easy as possible. The tool will backup necessary system configuration files and walk users through the whole installation process. In case of uninstalling YubiKey, the tool will also reverse any changes to the system, and clean up any trace it left.  

## Target Population and Benefit of the Project

This project is beneficial to all users willing to add extra security layer to their systems running Ubuntu. The streamlined process will be suitable for installation of YubiKey on large numbers of computers.  

## Projected Risk and Risk Management

There are certainly risks that come with automated system. Luckily, this project requires minimal user and outside input. In fact, one of the goals of this project is to make user input as few as possible. However, the installation process requires two outside software packages, which may be tampered by third party. In addition, the scripts of installation and guiding tool may also be modified by third party.  

## Cost of the Project

For people already own Yubikey products, this tool will be free of charge.  

