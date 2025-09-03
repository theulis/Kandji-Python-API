import requests
import os
import csv
import time
import re 

# ANSI colors for nicer terminal output
RED = "\033[31m"
RESET = "\033[0m"
BOLD='\033[1m'
GREEN = "\033[32m"

### API For Kandji Library Item Status: https://api-docs.kandji.io/#478764c4-638c-416c-b44c-3685a2f7b441 

#### Use environmental variables for Domain and API Key.
kandji_api_token = os.environ.get("kandji_api_token")
kandji_domain=os.environ.get("kandji_domain")
authorisation_value = str('Bearer ') + kandji_api_token

## Ask the user to specify the Library Item we would like to audit

### In this example the HomeBrew Audit Library Item ID is: b5d21f9e-9d41-4463-b2b5-c292b3c2ccad
### You can get from the full URL in Kandji : https://domain.kandji.io/library/custom-scripts/b5d21f9e-9d41-4463-b2b5-c292b3c2ccad/status


# Kandji has a more complicated GitHub Script - For more info [Device Library Items](
# https://github.com/kandji-inc/support/blob/main/api-tools/device-library-items/README.md)

print(f"Please specify the {GREEN}{BOLD}Auto App Kandji Library Item ID:{RESET}\n", end="")
while not (library_item := input().strip()):
  print("Library Item ID cannot be empty.\n", end="")

url = "https://"+kandji_domain+".api.kandji.io/api/v1/library/library-items/"+library_item+"/status"

payload = {}
headers = {
  'Authorization': authorisation_value
}

# Ask user where to save CSV in your user folder: Downloads, Desktop, or Documents. Enter to skip saving.
print(
    f"Type {RED}{BOLD}Downloads{RESET}, "
    f"{RED}{BOLD}Desktop{RESET}, or "
    f"{RED}{BOLD}Documents{RESET} to save CSV in your user folder, "
    "or press Enter to skip if you do not want to export this report to a CSV file:\n",
    end=""
)
while True:
  choice = input().strip().lower()
  if choice in ("", "downloads", "desktop", "documents"):
    break
  print("Please type 'Downloads', 'Desktop', or 'Documents', or press Enter if you do not want to export this report to a CSV file.\n", end="")

should_write_csv = choice in ("downloads", "desktop", "documents")
save_dir = ""
if should_write_csv:
  choice_map = {
    "downloads": os.path.expanduser("~/Downloads"),
    "desktop": os.path.expanduser("~/Desktop"),
    "documents": os.path.expanduser("~/Documents"),
  }
  save_dir = choice_map[choice]
  if not os.path.isdir(save_dir):
    print(f"Warning: Selected folder '{save_dir}' does not exist. Skipping CSV save.")
    should_write_csv = False

# Collect results to optionally write to CSV at the end
results_rows = []  # list of tuples: (computer_name, result_line)


while url:  # keep looping until 'next' is None
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()

    for value in range(len(json_response["results"])):
        status = json_response["results"][value]["status"]
        computer_name = json_response["results"][value]["computer"]["name"]
        last_audit_log = json_response["results"][value].get("last_audit_log")

        # Default values
        installed_version = "N/A"
        available_version = "N/A"
        up_to_date = "Unknown"

        if last_audit_log:  # only run regex if log text exists
            installed_match = re.search(r"Google Chrome ([0-9.]+)", last_audit_log)
            newer_match = re.search(r"A newer version \((.*)\)", last_audit_log)

            if installed_match:
                installed_version = installed_match.group(1)
            if newer_match:
                available_version = newer_match.group(1)

            # Decide if machine is up to date
            if available_version != "N/A":
                up_to_date = "Not Running Latest Version"
            else:
                up_to_date = "Running Latest Version"
        else:
            # No audit log yet → mark as pending
            up_to_date = "Audit Not Yet Available"

        # Print to terminal
        print(f'{computer_name},{status},{installed_version},{available_version},{up_to_date}')

        # Store row for CSV
        results_rows.append((computer_name, status, installed_version, available_version, up_to_date))


    # Advance to next page
    url = json_response.get("next")



# Write CSV if requested and directory is valid
if should_write_csv and results_rows:
  safe_library_item = "".join(c for c in library_item if c.isalnum() or c in ('-', '_')) or "library_item"
  timestamp = time.strftime("%Y%m%d-%H%M%S")
  csv_path = os.path.join(save_dir, f"Kandji-Export-Library-Status-{safe_library_item}-{timestamp}.csv")
  try:
    with open(csv_path, mode='w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      # Updated header with extra fields
      writer.writerow([
        "computer_name",
        "status",
        "installed_version",
        "newer_available_version",
        "update_status"
      ])
      writer.writerows(results_rows)
    print(f"✅ Saved CSV to: {RED}{BOLD}{csv_path}{RESET} 💾📄")
  except Exception as e:
    print(f"⚠️ Failed to write CSV to '{csv_path}': {e}")
