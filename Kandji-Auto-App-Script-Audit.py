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
        computer_name = json_response["results"][value]["computer"]["name"]
        status = json_response["results"][value]["status"]
        last_audit_log = json_response["results"][value].get("last_audit_log")

        # Default values
        result = "Audit Not Yet Available"
        audit_log = ""

        if last_audit_log:
            # Flatten newlines to spaces
            audit_log = " ".join(line.strip() for line in last_audit_log.splitlines() if line.strip())

            # Determine update status
            if "A newer version" in last_audit_log:
                result = "Update Available"
            else:
                result = "Up-to-Date"

        # Print to terminal with | separator
        print(f"{computer_name} | {status} | {result} | {audit_log}")

        # Store row for CSV
        results_rows.append((computer_name, status, result, audit_log))

    # Advance to next page if any
    url = json_response.get("next")


# Write CSV if requested and directory is valid
if should_write_csv and results_rows:
    safe_library_item = "".join(c for c in library_item if c.isalnum() or c in ('-', '_')) or "library_item"
    timestamp = time.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM
    csv_path = os.path.join(save_dir, f"Kandji-Export-Library-Status-{safe_library_item}-{timestamp}.csv")
    try:
        with open(csv_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Header
            writer.writerow(["computer_name", "status", "result", "audit_log"])
            writer.writerows(results_rows)
        print(f"✅ Saved CSV to: {RED}{BOLD}{csv_path}{RESET} 💾📄")
    except Exception as e:
        print(f"⚠️ Failed to write CSV to '{csv_path}': {e}")
