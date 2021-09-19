# Kuri's XP-Pen Userland config utility (GUI)

<img src="data/Artist22RProConfig.png">

Very rudimentary GUI.
Supports:
- Artist 22R Pro
- Artist 13.3 Pro
- Artist 12 Pro (Untested)
- Artist 24 Pro (Untested)

Pressing the update button will send the SIGHUP signal to the actual driver and get it to reload the config.

Setup with:
```
git clone https://github.com/kurikaesu/xp-pen-userland-config-util.git
cd xp-pen-userland-config-util
pip install -r requirements.txt
python3 -m xp_pen_userland_config_util
```
