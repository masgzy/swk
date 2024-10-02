termux-change-repo
termux-setup-storage
apt install python
cp ~/../usr/bin/python ~/../usr/bin/py
cp swk.sh ~/../usr/bin/sw
chmod 777 ~/../usr/bin/sw
cd /sdcard
mkdir tm
cd ~
echo "cd /sdcard/tm" > ~/../usr/bin/tm
chmod 777 ~/../usr/bin/tm
echo "source tm" > .bashrc
py install.py