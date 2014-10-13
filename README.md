Notipi
======

This is the software for the Notipis made by Omega Verksted for each affiliation (student organization in Trondheim).

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
10. Edit local.py with the information you get by emailing appkom@online.ntnu.no (tell us which student organization you're from)
11. Reboot
