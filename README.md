# chaz-canary-check

A tool to easily check the validity of the weekly warrant canary at https://caphillauto.zone/

## Usage

You will need an installed copy of `gpg` on your PATH.

```shell
$ pip install -r requirements.txt
$ python3 canary_check.py
```

Example output (as of 12th June, 2020):

```
[+] Fetching warrant canary...
[+] PGP signature is valid.
[+] The given date (12 June 2020) is less than eight days old.
[+] The headlines from the canary are as follows:
'A Slap in the Face': Black Veterans on Bases Named for Confederates
Top Military Official Apologizes for Role in Trump Photo Op
No Longer in Denial About Grim Outlook, Investors Drive Market Down

[+] The canary seems to check out.
```
