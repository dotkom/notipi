sudo apt-get update
sudo apt-get --assume-yes install htop supervisor vim python-dev python-pip git curl ntp
sudo rm /etc/localtime >> /dev/null
sudo ln -s /usr/share/zoneinfo/Europe/Oslo /etc/localtime
sudo sh -c "echo 'XKBMODEL=\"pc105\"\nXKBLAYOUT=\"no\"' > /etc/default/keyboard"
sudo service keyboard-setup restart
sudo pip install virtualenvwrapper
echo 'source virtualenvwrapper.sh' >> .bashrc
source virtualenvwrapper.sh
cd /home/pi
git clone https://github.com/appKom/notipi.git
cd notipi
git checkout production
mkvirtualenv notipi
setvirtualenvproject
pip install -r requirements.txt
sudo sh -c "echo '[program:notipi]\nuser=root\ncommand=/home/pi/.virtualenvs/notipi/bin/python /home/pi/notipi/main.py' > /etc/supervisor/conf.d/notipi.conf"
sudo sh -c "echo '\n*/10 * * * *  root  /home/pi/notipi/update_debug.sh > /home/pi/notipi/cron.log 2>&1' >> /etc/crontab"
echo '----------------------------'
echo 'Remember to edit local.py'
echo '----------------------------'
