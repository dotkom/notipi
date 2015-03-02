Notipi
======

For students at NTNU or HiST, Trondheim, Norway.

If your student union ("linjeforening") wants to purchase a Notipi, contact Omega Verksted. Notipi allows your student union to get even more out of [Online Notifier](https://github.com/appKom/notifier/): Coffee status, office status (open/closed), meeting status and more.

This software is made my the Application Committee in Online. The software is made for the Notipis that are built by Omega Verksted for each student organization in Trondheim, Norway.

The software delivers data to a server running [Online Notiwire](https://github.com/appKom/notiwire/), which in turn delivers data to [Online Notifier](https://github.com/appKom/notifier/). Online Notifier is a free + ad-free browser extension that may be added from here:
* http://bit.ly/NotifierForChrome
* http://bit.ly/NotifierForOpera

Both Online and OmegaV are student unions at NTNU in Trondheim, Norway. Feel free to contact us.
* appkom@online.ntnu.no (Notipi software)
* omegav@omegav.no (Notipi hardware)

Which student unions have a Notipi?
-----------------------------------

In chronological order:

1. Online (home made, with a big red button)
2. Delta (home made, with a screen and a "kriteliste"-function)
3. Abakus (home made, with automatic coffee notifications, but without light sensor)
4. Solan
5. Nabla
6. Høiskolens Chemikerforening

Installation of this software on a Notipi
-----------------------------------------

1. Format the SD-card to the lastest version of Raspbian
2. Boot up the Raspberry Pi and choose:
  * Expand filesystem
  * Change User Password (use one you'll truly remember)
  * Finish -> Reboot
3. Log in
4. `wget http://gg.gg/notipi -O - | sh`

Alt:

4. `wget http://gg.gg/notipi`
5. `mv notipi setup.sh`
6. `chmod +x setup.sh`
7. `./setup.sh`

The Notipi setup is now complete, but it must be configured for your student organization.

8. `cd notipi`
9. `cp settings-example.py local.py`
10. Edit `local.py` with the information you get by emailing appkom@online.ntnu.no (tell us which student organization you're from)
11. `sudo reboot now`
