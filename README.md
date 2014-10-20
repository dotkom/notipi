Notipi
======

This software is made my the Application Committee in Online. The software is made for the Notipis that are built by Omega Verksted for each student organization in Trondheim, Norway.

The software delivers data to a server running [Online Notiwire](https://github.com/appKom/notiwire/), which in turn delivers data to [Online Notifier](https://github.com/appKom/notifier/). Online Notifier is a free + ad-free browser extension that may be added from here:
* http://bit.ly/NotifierForChrome
* http://bit.ly/NotifierForOpera

Both Online and OmegaV are student unions at NTNU in Trondheim, Norway. Feel free to contact us.
* appkom@online.ntnu.no (Notipi software)
* omegav@omegav.no (Notipi hardware)

If your student union wants to purchase a Notipi, contact Omega Verksted.

Installation
------------

1. Format the SD-card to the lastest version of Raspbian
2. Boot up the Raspberry Pi and choose:
  * Expand filesystem
  * Change User Password (use one you'll truly remember)
  * Finish -> Reboot
3. Log in
4. `wget http://gg.gg/notipi`
5. `mv notipi setup.sh`
6. `chmod +x setup.sh`
7. `./setup.sh`

The Notipi setup is now complete, but it must be configured for your student organization.

8. `cd notipi`
9. `cp settings-example.py local.py`
10. Edit `local.py` with the information you get by emailing appkom@online.ntnu.no (tell us which student organization you're from)
11. `sudo reboot now`
