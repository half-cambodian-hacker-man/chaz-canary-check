from typing import List

import requests
import gnupg
import re

import dateutil.parser
from datetime import datetime, timedelta

from colorama import Fore as Colours

HTTP_USER_AGENT = \
  "chaz-canary-check (https://github.com/half-cambodian-hacker-man/chaz-canary-check)"

def print_info(color, message):
  print(color + "[+] " + Colours.RESET + message)


def get_pk_info(gpg) -> List[str]:
  with open("chaz-pubkey.txt") as f:
    return gpg.import_keys(f.read()).fingerprints


def validate_gpg_signature(warrant_text) -> bool:
  gpg = gnupg.GPG(gnupghome="keys")
  fingerprints = get_pk_info(gpg)
  v = gpg.verify(warrant_text.encode("utf-8"))

  return any(v.fingerprint == fingerprint for fingerprint in fingerprints)


def extract_date(warrant_text) -> datetime:
  months = [pair[1] for pair in dateutil.parser.parserinfo.MONTHS]
  months = "(" + "|".join(months) + ")"
  day = r"(\d+).{2},"
  year = r"(\d{4})"

  m = re.search(" ".join([months, day, year]), warrant_text)
  month = m.group(1)
  day = m.group(2)
  year = m.group(3)

  return dateutil.parser.parse(" ".join([month, day, year]))


def validate_date(warrant_text) -> bool:
  date = extract_date(warrant_text)
  return datetime.now() - date < timedelta(days=8)


def extract_headlines(warrant_text):
  lines = warrant_text.splitlines()
  message_end_idx = [idx for idx, line in enumerate(lines) if "-BEGIN PGP SIGNATURE-" in line][-1]

  for i in range(3, 0, -1):
    yield lines[message_end_idx - i]


def main():
  print_info(Colours.BLUE, "Fetching warrant canary...")
  
  warrant_text = requests.get("https://caphillauto.zone/canary.txt",
    headers={ "User-Agent": HTTP_USER_AGENT }
  ).text
  gpg_valid = validate_gpg_signature(warrant_text)
  
  if gpg_valid:
    print_info(Colours.GREEN, "PGP signature is valid.")
  else:
    print_info(Colours.RED, "PGP signature is not valid!")
  
  date_valid = validate_date(warrant_text)
  date_str = extract_date(warrant_text).strftime('%d %B %Y')
  if date_valid:
    print_info(Colours.GREEN, f"The given date ({date_str}) is less than eight days old.")
  else:
    print_info(Colours.RED, f"The canary is older than eight days old! ({date_str})")

  print_info(Colours.BLUE, "The headlines from the canary are as follows:")
  for headline in extract_headlines(warrant_text):
    print(headline)

  print()

  if gpg_valid and date_valid:
    print_info(Colours.GREEN, "The canary seems to check out.")
  else:
    print_info(Colours.RED, "Warning! The canary seems to be invalid. Take care.")

if __name__ == "__main__":
  main()
