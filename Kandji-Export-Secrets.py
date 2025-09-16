import requests
import json
import time
import os

# ANSI colors for nicer terminal output
RED = "\033[31m"
RESET = "\033[0m"
BOLD='\033[1m'
GREEN = "\033[32m"

##### Use Environmental Variables - Example: 
#### Use echo 'export kandji_device_api_url="domain.clients.us-1.kandji.io"' >> ~/.zshrc

kandji_api_token = os.environ.get("kandji_api_token")
authorisation_value = str('Bearer ') + kandji_api_token
kandji_device_api_url=os.environ.get("kandji_device_api_url")

print(kandji_device_api_url)


timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
filename="Kandji_Device_Export_With_Secrets_"+str(timestr)+".csv"

### ==========================================================================================================================================
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

### ==========================================================================================================================================

pathname = save_dir + "/" + filename
with open(pathname, "a") as f:
    print("Serial_Number,Device_ID,Platform,Blueprint_Name,Last_Check_In,OS_Version,FileVault_Key,User_Based_Bypass_Code,Device_Based_Bypass_Code,User_Unlock_PIN", file=f)

    url = "https://"+kandji_device_api_url+"/api/v1/devices"

    payload = {}
    headers = {
    'Authorization': authorisation_value}

    while url:  # keep looping until 'next' is None
        response = requests.request("GET", url, headers=headers, data=payload)
        dictionary_user_output= json.loads(response.text)
        for value in range(len(dictionary_user_output)):

            # Print progress to terminal
            device_serial = dictionary_user_output[value]['serial_number']
            device_id = dictionary_user_output[value]['device_id']
            print(f"{GREEN}Processing Device {device_serial} ({device_id})...{RESET}")

            print(str(dictionary_user_output[value]['serial_number']),end=',', file=f)
            print(str(dictionary_user_output[value]['device_id']),end=',', file=f)
            print(str(dictionary_user_output[value]['platform']),end=',', file=f)
            print(str(dictionary_user_output[value]['blueprint_name']),end=',', file=f)
            print(str(dictionary_user_output[value]['last_check_in']),end=',', file=f)
            print(str(dictionary_user_output[value]['os_version']),end=',', file=f)

        ### API Call for Filevault for that specific Device
            url_filevault= "https://"+kandji_device_api_url+"/api/v1/devices/"+str(dictionary_user_output[value]['device_id'])+"/secrets/filevaultkey/"
            payload_filevault = {}
            headers_filevault = {
            'Authorization': authorisation_value,
            }
            response_filevault = requests.request("GET", url_filevault, headers=headers_filevault, data=payload)
            dictionary_filevault_output= json.loads(response_filevault.text)
            print(dictionary_filevault_output['key'],end=',', file=f)

        ### API Call for ByPass Codes for that specific Device

            url_bypass_code= "https://"+kandji_device_api_url+"/api/v1/devices/"+str(dictionary_user_output[value]['device_id'])+"/secrets/bypasscode/"
            payload_bypass_code = {}
            headers_bypass_code = {
            'Authorization': authorisation_value,
            }
            response_bypass_code = requests.request("GET", url_bypass_code, headers=headers_bypass_code, data=payload)
            dictionary_bypass_code_output= json.loads(response_bypass_code.text)
            print(dictionary_bypass_code_output['user_based_albc'],end=',', file=f)
            print(dictionary_bypass_code_output['device_based_albc'],end=',', file=f)

        ### API Call for Unlock Codes for that specific Device

            url_unlock_pin= "https://"+kandji_device_api_url+"/api/v1/devices/"+str(dictionary_user_output[value]['device_id'])+"/secrets/unlockpin/"
            payload_unlock_pin = {}
            headers_unlock_pin = {
            'Authorization': authorisation_value,
            }
            response_unlock_pin = requests.request("GET", url_unlock_pin, headers=headers_unlock_pin, data=payload)
            dictionary_unlock_pin_output= json.loads(response_unlock_pin.text)
            print(dictionary_unlock_pin_output['pin'], file=f)


# ✅ assign url to the next page, if any
## Typical JSON Response
# "count": 380,
# "next": "https://xxx.api.kandji.io/api/v1/devices?limit=300&offset=300",
# "previous": null,
    url = dictionary_user_output.get("next")





