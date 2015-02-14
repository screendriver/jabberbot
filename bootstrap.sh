#!/usr/bin/env bash

# Setting timezone
echo "Europe/Berlin" | sudo tee /etc/timezone
sudo dpkg-reconfigure -f noninteractive tzdata

# Update package list
sudo apt-get update -y
sudo apt-get install -y build-essential git mc python3-pip pylint

echo "alias sudo='sudo env PATH=$PATH'" >> /home/vagrant/.bash_profile

cd /vagrant

# Fix pyvenv-3.4. This is a workaround because it is broken at the moment
echo "Fixing pyvenv-3.4"
pyvenv-3.4 --without-pip env
source env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
deactivate
source env/bin/activate

echo "Installing dependencies from Python Package Index"
pip3.4 install -r requirements.txt

echo "cd /vagrant" >> /home/vagrant/.bash_profile
echo "source env/bin/activate" >> ~/.bash_profile
