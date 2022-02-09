A login/register system in python. 

Including features such as:
- email verification by sending activation codes
- data storing in SQL database
- 2FA
- changing password and mail from user panel

To be added:
- implement account delete
- admin panel

You can find an empty template file for settings.json inside database folder. Same with empty database.
To run it you have to overwrite settings.json and enter credentials for email that will send server messages.

For testing this program you should prepare new google account,
as its adviced to not use personal/important email for it. 

To let python send email you must allow less secure apps to login. 

https://support.google.com/accounts/answer/6010255

You may also have to do this:

https://accounts.google.com/b/0/DisplayUnlockCaptcha
