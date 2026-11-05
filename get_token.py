"""Run once on your own computer: logs in to Garmin Connect and prints the token to paste
into the GARMIN_TOKENS secret of your GitHub repository. Your password is not stored anywhere."""
import getpass

from garminconnect import Garmin

email = input("Garmin Connect email: ").strip()
password = getpass.getpass("Garmin Connect password (hidden): ")
g = Garmin(email, password, prompt_mfa=lambda: input("Code received by email or SMS: ").strip())
g.login()
print("\nCopy everything on the next line into the GARMIN_TOKENS secret:\n")
print(g.client.dumps())
