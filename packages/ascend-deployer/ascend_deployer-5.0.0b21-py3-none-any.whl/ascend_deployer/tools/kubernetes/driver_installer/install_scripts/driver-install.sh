#!/bin/bash

ping -c 1 172.17.0.1 > /dev/null

if [ $? -eq 0 ];then
  hostIp=172.17.0.1
else
  hostIp=$(ip route|awk '/default/ {print $3}')
fi


mkdir -p /root/.ssh /mnt/.ssh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
cat ~/.ssh/id_rsa.pub >> /mnt/.ssh/authorized_keys

cd /root
cp *-driver*.run /mnt
cp *firmware*.run /mnt
cp install.sh /mnt

mkdir -p /mnt/pkgs
cp *.deb /mnt/pkgs
cp *.rpm /mnt/pkgs

ssh -o "StrictHostKeyChecking=no" root@$hostIp groupadd -g 1000 HwHiAiUser
ssh root@$hostIp useradd -g HwHiAiUser -u 1000 -d /home/HwHiAiUser -m HwHiAiUser -s /bin/bash

if ssh root@$hostIp command -v dpkg >/dev/null 2>&1; then
  ssh root@$hostIp dpkg --force-all -i /root/pkgs/*.deb
elif ssh root@$hostIp command -v rpm >/dev/null 2>&1; then
  ssh root@$hostIp rpm -iUv /root/pkgs/*.rpm --nodeps --force
else
  echo "Unknown package manager"
fi

ssh root@$hostIp npu-smi info > /dev/null
if [ $? -eq 0 ];then
  ssh root@$hostIp bash /root/*-driver*.run --upgrade
  ssh root@$hostIp bash /root/*firmware*.run --upgrade
else
  ssh root@$hostIp bash /root/*-driver*.run --full
  ssh root@$hostIp bash /root/*firmware*.run --full
fi

interval=5

while (true); do
  npu-smi info > /dev/null
  if [ $? -eq 0 ];then
    sleep $interval
  else
    exit 1
  fi
done
