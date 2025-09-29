import requests
import os
import json

# ANSI colors for nicer terminal output
RED = "\033[31m"
RESET = "\033[0m"
BOLD='\033[1m'
GREEN = "\033[32m"

#### Use environmental variables for Domain and API Key.
okta_staging_api_key = os.environ.get("okta_staging_api_key")
okta_main_api_key = os.environ.get("okta_main_api_key")
okta_domain = os.environ.get("okta_domain")

# Define the variable before the loop
selected_domain = None
api_key = None

### Create a basic Menu so the user can select the correct environment
while True:
    user_input = input(f"Please type {GREEN}{BOLD}staging or main{RESET} : ").strip().lower()
    if user_input == "main":
      okta_instance=okta_domain+".okta.com"
      api_key=okta_main_api_key
      print(f"You have selected the {GREEN}{BOLD}Main Okta Environment{RESET}: {okta_instance}")
      break
    elif user_input == "staging":
      okta_instance=okta_domain+".oktapreview.com"
      api_key=okta_staging_api_key
      print(f"You have selected the {GREEN}{BOLD}Staging Okta Environment{RESET}: {okta_instance}")
      break
    else:
      print(f"Invalid input. Please type {GREEN}{BOLD}staging or main{RESET}.")

### Prepare the Authentication Header and the URL

authorization_header_value = 'SSWS ' + api_key
url = "https://" + okta_instance + "/api/v1/users/00u1bwz2sccMbK77u0h8/factors"
payload = {}
headers = {
   'Authorization': authorization_header_value,
   'Accept': 'application/json'
   }

response = requests.request("GET", url, headers=headers, data=payload)
factors= json.loads(response.text)
for factor in factors:
  print(factor['factorType'],end=",")
print("\nReport Completed")
