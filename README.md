A login/register system written in python. 
Includes features such as:
- email verification by sending activation codes
- data storing in sqlite3
- password storing in sha2 hash
To be added in close future:
- implement 2FA
- implete account delete
- expand settings
- admin panel

Empty database provided in /database

Its required to configure email address for sending verification codes to run program.
In order to do so you have to prepare new google account as its adviced to not use personal/important email account for this.

To let python send email you must allow less secure apps to login. 
https://support.google.com/accounts/answer/6010255

You may also have to do this:
https://accounts.google.com/b/0/DisplayUnlockCaptcha

Then in MailHandler file in 'get_mail_config' method you must locate previously created settings.json file containing email addres and its password.
