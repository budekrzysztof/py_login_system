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

To run this program you have to give MailUtils get_mail_config() and Utilities.get_salty() a path to a settings.json,
a file containing username and password for a google account and salt for sha2.
You can find an empty template file for settings.json inside database folder. Same with empty database.

For testing this program you should prepare new google account,
as its adviced to not use personal/important email for it. 

To let python send email you must allow less secure apps to login. 

https://support.google.com/accounts/answer/6010255

You may also have to do this:

https://accounts.google.com/b/0/DisplayUnlockCaptcha
