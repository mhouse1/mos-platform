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


