sudo apt-get install htop supervisor vim python-dev python-pip
sudo ln -s /usr/share/zoneinfo/Europe/Oslo /etc/localtime
sudo echo 'XKBMODEL="pc105"\nXKBLAYOUT="no"' > /etc/default/keyboard
sudo pip install virtualenvwrapper
cd /home/pi
git clone https://github.com/appKom/notipi.git
cd notipi
mkvirtualenv notipi
setvirtualenvproject
pip install -r requirements.txt
sudo echo '[program:notipi]\nuser=root\ncommand=/home/pi/.virtualenvs/notipi/bin/python /home/pi/notipi/main.py' > /etc/supervisor/conf.d/notipi.conf
echo 'Remember to edit settings.py'

