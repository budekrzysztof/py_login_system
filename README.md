A login/register system written in python. 

Includes features such as:
- email verification by sending activation codes
- data storing in sqlite3
- password storing in sha2 hash
- 2FA
- changing password and mail from user panel

To be added in close future:
- implement account delete
- admin panel

Empty database and settings.json file provided in /database

To run this program you have to give MailHandler a path to a settings.json file containing username and password for a google account.
You can find an empty template file for settings.json inside database folder. For testing this program you should prepare new google account,
as its adviced to not use personal/important email for it. 

To let python send email you must allow less secure apps to login. 

https://support.google.com/accounts/answer/6010255

You may also have to do this:

https://accounts.google.com/b/0/DisplayUnlockCaptcha
