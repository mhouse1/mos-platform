# mos-platform
Custom Minimal OS (MOS) built using Yocto for the Raspberry Pi Compute Module 4

# MOS Features
* Python3
* PyQt5
* SSH
* SystemD

## Requirements
* Disk space: at least 20GB of free space is required to build OS
* Time: On a 2013 MacBook Pro the basic console image takes about 6Hours to complete first build

## Getting started
* Download and install Ubuntu 22.04.3 LTS , others OS are untested for compatibility
* A series of packages must be installed to support the Yocto build
```
sudo apt-get update
sudo apt install git python3 gawk wget diffstat unzip texinfo gcc-multilib build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping libsdl1.2-dev xterm autoconf libtool libglib2.0-dev libarchive-dev sed cvs subversion coreutils texi2html docbook-utils help2man make gcc g++ desktop-file-utils libgl1-mesa-dev libglu1-mesa-dev mercurial automake groff curl lzop asciidoc u-boot-tools dos2unix mtd-utils pv libncurses5 libncurses5-dev libncursesw5-dev libelf-dev zlib1g-dev
```

for kirkstone
```
sudo apt-get update
sudo apt-get -y install lz4
```

## Installing python3
```
sudo apt update
sudo apt install python3
python3 --version
```


### if the repo utility commands fail below due to /usr/bin/env No such file or directory
Solution 
```

If Python 3 has been installed, run these commands: whereis python3

Then we create a symlink to it: sudo ln -s /usr/bin/python3 /usr/bin/python
```

## Installing the `repo` utility

To download this repo and all the dependencies listed in the default.xml, you need to have `repo` installed 

* Note: the repo utility must be install using curl command shown below , but if you decide too use apt to install repo besure to point it to ~/bin/repo
```
mkdir ~/bin
curl http://commondatastorage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
PATH=${PATH}:~/bin
```
If you have not done so, set your git account's identity
```
git config --global user.email michaelhousera@gmail.com
git config --global user.name mhouse1
```


Download MOS platform and sources listed in the default.xml file to a new project folder:
```
mkdir mos1
cd mos1
repo init -u https://github.com/mhouse1/mos-platform -b <my_branch_name>
repo sync
```

At the end of the commands you have every metadata you need to start work with.
The source code is checked out at `mos1/sources`.
You can use any directory to host your build.
As a personal favor I'm using `mos1/build` as build folder.

To configure the build and use local.conf.sample to replace the local.conf:
```
chmod a+x .repo/manifests/setup
.repo/manifests/setup
```

Afterwards you may want to edit the build/conf/local.conf
* to set the desired machine type.
* set the IMAGE_FSTYPE


To start a simple image build:

```
source sources/poky/oe-init-build-env build
bitbake console-image
```

Other images:

* ap-image
* audio-image
* console-basic-image
* console-image
* flask-image
* gumsense-image
* iot-image
* pyqt5-image
* qt5-basic-image
* qt5-image

# Making changes
If you make changes to a layer or the default.xml file run these commands to update to new files and build again.

```
repo sync
.repo/manifests/setup
bitbake console-image
```

## Troubleshooting
you might get an error `.repo/manifests: contains uncommited changes` , this happens if you've modified the mos-platform locally. In this case you can either reset the changes 

```
cd .repo/manifets
git reset --hard
```
or you can branch and push the changes up

# clean build
If you modify the default.xml file you may want to do a clean build to pull new repo's and sources before building
```
# reboot if you are already in a bitbake environment
repo sync
.repo/manifests/setup
source sources/poky/oe-init-build-env build
bitbake -c cleanall qt5-image
bitbake qt5-image
```

# copying files from vbox to host (windows)
* in vbox Devices > Shared Folders > Shared Folders Settings > mount the folder you want from windows
* this mounts it with root permission so in ubuntu open terminal and su as root
* run cp command to copy file from vbox to windows, for example: cp /home/terrafirma/dev-tools/mos/build/tmp/deploy/images/raspberrypi4-64/console-image-raspberrypi4-64.rpi-sdimg /media/sf_Downloads/console-image-raspberrypi4-64.rpi-sdimg


# Flashing the sd image

You can flash the rpi-sdimg directly from within ubuntu:

```
# to show the drive names use command
lsblk -p
# to flash the file use dd command
dd if=<path_to\input_file_name> of=<name_of_sd_card_device>

#for example
sudo dd if=/home/username/Downloads/mhouseos.rpi-sdimg of=/dev/sdb status=progress bs=4M
```

# to use tar.xz rootfs
```
rootfs is not image. It is tar archive with content of root filesystem and you are supposed to prepare bootloader and kernel on your SD card yourself and configure them to use root partition.

```

## flash using windows
it is faster to transfer the file from ubuntu to windows host and then use etcher to perform flashing.
* set compute module to boot mode, connect to pc then run rpiboot.exe
* flash the rpi-sdimg file using etcher (portable install balenaEtcher-Portable-1.18.11.exe works too).

# building using a docker container
run the "docker build ." command in the same directory as the Dockerfile
```
michael@michael-MacBookPro:~/dev-tools/poky-container$ docker build .
[+] Building 26.9s (17/17) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 1.67kB                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:22.04            0.3s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [ 1/13] FROM docker.io/library/ubuntu:22.04@sha256:19478ce7fc2ffbce89  0.0s
 => CACHED [ 2/13] RUN apt-get update && apt-get install -y git python3 g  0.0s
 => [ 3/13] RUN apt-get update && apt-get install -y lz4 zstd              6.4s
 => [ 4/13] RUN apt update && apt install -y   curl   gpg                  4.6s 
 => [ 5/13] RUN curl -fsSL https://cli.github.com/packages/githubcli-arch  0.6s 
 => [ 6/13] RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/u  0.4s 
 => [ 7/13] RUN apt update && apt install -y gh;                           8.4s 
 => [ 8/13] RUN mkdir -p ~/bin                                             0.4s 
 => [ 9/13] RUN curl -o ~/bin/repo http://commondatastorage.googleapis.co  0.6s 
 => [10/13] RUN chmod a+x ~/bin/repo                                       0.5s 
 => [11/13] RUN groupadd -g 1000 dev             && useradd -u 1000 -g de  0.5s 
 => [12/13] RUN locale-gen en_US.UTF-8                                     2.5s 
 => [13/13] WORKDIR /home/dev                                              0.2s 
 => exporting to image                                                     1.1s 
 => => exporting layers                                                    1.1s 
 => => writing image sha256:e69cfaaab8aa0525e5833dd17fb96460335bc1449696c  0.0s
michael@michael-MacBookPro:~/dev-tools/poky-container$ docker run -it -v yocto-volume:/home/dev sha256:e69cfaaab8aa0525e5833dd17fb96460335bc1449696c 
dev@b242783491f5:~$ cd mos1
dev@b242783491f5:~/mos1$ source sources/poky/oe-init-build-env build

### Shell environment set up for builds. ###
...
...
dev@b242783491f5:~/mos1$ whoami
dev
dev@b242783491f5:~/mos1$ cat /etc/os-release 
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
dev@b242783491f5:~/mos1$ python --version
bash: python: command not found
dev@b242783491f5:~/mos1$ python3 --version
Python 3.10.12
dev@b242783491f5:~/mos1$ curl
curl: try 'curl --help' or 'curl --manual' for more information
dev@b242783491f5:~/mos1$ curl --version
curl 7.81.0 (x86_64-pc-linux-gnu) libcurl/7.81.0 OpenSSL/3.0.2 z
```
## accessing files from docker
on Ubuntu go to:
```
/var/lib/docker/volumes/[volume_name]/_data
```

# Successful build
```
dev@8655c0f70b79:~/mos1/build$ bitbake py3qt-image
Loading cache: 100% |############################################| Time: 0:00:01
Loaded 3577 entries from dependency cache.
NOTE: Resolving any missing task queue dependencies

Build Configuration:
BB_VERSION           = "1.46.0"
BUILD_SYS            = "x86_64-linux"
NATIVELSBSTRING      = "universal"
TARGET_SYS           = "aarch64-poky-linux"
MACHINE              = "raspberrypi4-64"
DISTRO               = "poky"
DISTRO_VERSION       = "3.1.33"
TUNE_FEATURES        = "aarch64 cortexa72 crc crypto"
TARGET_FPU           = ""
meta                 
meta-poky            = "HEAD:63d05fc061006bf1a88630d6d91cdc76ea33fbf2"
meta-oe              
meta-multimedia      
meta-networking      
meta-perl            
meta-python          = "HEAD:01358b6d705071cc0ac5aefa7670ab235709729a"
meta-qt5             = "HEAD:5ef3a0ffd3324937252790266e2b2e64d33ef34f"
meta-raspberrypi     = "HEAD:2081e1bb9a44025db7297bfd5d024977d42191ed"
meta-security        = "HEAD:eb631c12be585d18beddbb41f6035772b2cb17d5"
meta-jumpnow         = "HEAD:b3995636741be0d219a50035c98ded8b48590888"
meta-rpi64           = "HEAD:623e233667fcdd328b5678517340e3c3e5561f1f"

```

## Flashing wic.bz2
```
michael@michael-MacBookPro:~/dev-tools/poky-container/usbboot$ sudo ./rpiboot
RPIBOOT: build-date Jun 15 2024 version 20240422~085300 4a3d3117
Waiting for BCM2835/6/7/2711/2712...
Loading embedded: bootcode4.bin
Sending bootcode.bin
Successful read 4 bytes 
Waiting for BCM2835/6/7/2711/2712...
Loading embedded: bootcode4.bin
Second stage boot server
Cannot open file config.txt
Cannot open file pieeprom.sig
Loading embedded: start4.elf
File read: start4.elf
Cannot open file fixup4.dat
Second stage boot server done
michael@michael-MacBookPro:~/dev-tools/poky-container/usbboot$ sudo dd if='/home/michael/Downloads/console-image-raspberrypi4-64-20240615013244.rootfs.wic.bz2' of=/dev/sdb status=progress
```
