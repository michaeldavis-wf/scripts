scripts
===========

A variety of useful scripts for the WebFilings development environment.


dev_build.py
-----------
Sets your app.yaml version to '1' and appid to 'bigsky'.
Sets settings in settingslocal.py to optimal development settings.
Uses [terminal-notifier][1] to trigger a Mac OS X notification when it is finished.

[1]: https://github.com/alloy/terminal-notifier        "terminal-notifier"

prep_deploy.py
-----------
Sets app.yaml to the specified version and appid (edit script to set default appid).
Sets settings in setingslocal.py to proper deployed settings.
Uses [terminal-notifier][1] to trigger a Mac OS X notification when it is finished.

[1]: https://github.com/alloy/terminal-notifier        "terminal-notifier"

###Options
* --version    The version to deploy to.
* --appid      The applicaiton id to deploy to.
* --full       If included, it will perform a full flex build.
