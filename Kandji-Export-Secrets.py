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
kandji_domain=os.environ.get("kandji_domain")

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

#### Get Device Count
#### We will run an API call for every 300 devices (1-300,301-600,601-900 etc.)
### First we need to find how many devices we have

url_device_count = "https://"+kandji_domain+".api.kandji.io/api/v1/settings/licensing"
payload = {}
headers = {'Authorization': authorisation_value}

response_device_count = requests.request("GET", url_device_count, headers=headers, data=payload)
response_device_count_json=response_device_count.json()

total_devices=response_device_count_json['counts']['computers_count']

# Generate URLs dynamically
api_limit = 300  # devices per API call
base_url = "https://"+kandji_device_api_url+"/api/v1/devices"
urls = [f"{base_url}?offset={i+1}" if i > 0 else base_url for i in range(0, total_devices, api_limit)]


## Write to the CSV File - Start with the Header 
pathname = save_dir + "/" + filename
with open(pathname, "a") as f:
    print("Serial_Number,Device_ID,Platform,Blueprint_Name,Last_Check_In,OS_Version,FileVault_Key,User_Based_Bypass_Code,Device_Based_Bypass_Code,User_Unlock_PIN", file=f)



    for url in urls:  # keep looping until 'next' is None
        payload = {}
        headers = {'Authorization': authorisation_value}
        response = requests.request("GET", url, headers=headers, data=payload)
        dictionary_user_output= json.loads(response.text)
        for value in range(len(dictionary_user_output)):
            print(f"{GREEN}Processing Device {str(dictionary_user_output[value]['serial_number'])} "
                  f"({str(dictionary_user_output[value]['device_id'])})...{RESET}", end='\r')
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






