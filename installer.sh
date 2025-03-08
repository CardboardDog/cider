#!/bin/bash

clear

echo "Cider v1"
read -p "[press any key to start install]"
clear

lsblk
read -p "Where to install? " drive

echo "All data on drive [$drive] will be overwriten."
read -p "Continue [y/n]: " cont
if [ "$cont" != "y" ]; then
	exit 1
fi
clear

connect_wifi () {
	wlo="$(ip link | grep -o 'wlo.')"
	wlan="$(ip link | grep -o 'wlan.')"
	wifi=""
	if [ -z "$wlo" ]; then
		wifi="$wlan"
	else
		wifi="$wlo"
	fi;
	echo $wifi
	rfkill unblock wlan
	iwctl device $wifi set-property Powered on
	iwctl adapter $wifi set-property Powered on
	iwctl station $wifi scan
	iwctl station $wifi get-networks
	read -p "Wifi to connect to? " conn
	iwctl station $wifi connect $conn
}

if [[ `ping -c1 google.com` ]]; then
	echo "Ethernet detected"
else
	while ! [[ `ping -c1 google.com` ]]; do
		connect_wifi
	done
fi;
timedatectl
clear

echo "VIDEO DRIVERS:"
echo "--------------"
echo "0: Intel"
echo "1: AMD"
echo "2: nVidia"
echo "3 or anything else for none."
echo "-------------"
read -p "Driver [0/1/2/3]:" GPU
declare -a drivers
drivers=("intel" "amd" "nvidia" "none")
clear

echo "FINAL"
echo "-------------"
echo "install drive: $drive"
echo "video drivers: ${drivers[$GPU]}"
echo "-------------"
read -p "Install [y/n]?" cont
if [ "$cont" != "y" ]; then
	exit 1
fi

echo "wiping ${drive}"
dd if=/dev/zero of=/dev/${drive}
parted --script /dev/${drive} mklabel gpt
parted --script /dev/${drive} mkpart primary fat32 1MiB 300MiB
parted --script /dev/${drive} mkpart primary ext4 300MiB 100%
parted --script /dev/${drive} set 1 esp on
mkfs.ext4 /dev/${drive}1
mkfs.fat -F 32 /dev/${drive}2

mount /dev/${drive}1 /mnt
mount --mkdir /dev/${drive}2 /mnt/boot

pacstrap -K /mnt base linux linux-firmware vim nano man-db man-pages texinfo NetworkManager parted python3

genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt

# clock stuff here later ln -sf
# hwclock --systohc

locale-gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
echo "ciderbooted.local" >> /etc/hostname

mkinitcpio -P
yes cider | passwd
grub-install --target=x86_64-efi --efi-directory=esp --bootloader-id=GRUB #only supports efi right now

reboot
