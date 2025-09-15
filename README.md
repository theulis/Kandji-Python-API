# Kandji-Python-API


## Reference 

Simplify Official Kandji Scripts, which brings info extraction time from 10-15 mins to a few seconds.

[Official Kandji GitHub Account](https://github.com/kandji-inc/support/tree/main/api-tools)

## Python Scripts 
Click on the hyperlinks to go to the specific section.

✨ [Kandji Library Item Custom Script - Status / Audit](https://github.com/theulis/Kandji-Python-API?tab=readme-ov-file#kandji-library-item-custom-script---status--audit)

✨ [Kandji Library Item Auto App - Audit](https://github.com/theulis/Kandji-Python-API?tab=readme-ov-file#kandji-auto-app-library-item-audit)


## Kandji Library Item Custom Script - Status / Audit

```
Kandji-Custom-Script-Audit.py
```

This Python script queries the [Kandji API](https://api-docs.kandji.io/#478764c4-638c-416c-b44c-3685a2f7b441) for the **status of a specific Library Item** (custom script).  
It outputs results to the terminal and can optionally export them to a CSV file.

Kandji has a more complicated GitHub Script - For more info [Device Library Items](
https://github.com/kandji-inc/support/blob/main/api-tools/device-library-items/README.md)

---

## 🔎 What the Script Does

1. **Prompt for a Kandji Library Item ID**  
   - Example: `b5d21f9e-9999-4444-3333-c292b3c2ccad`  
   - The script builds the API request URL using your **Kandji domain** and **API token** (set as environment variables).

2. **Call the Kandji API**  
   - It makes authenticated requests to Kandji’s `library-items/{id}/status` endpoint.  
   - Automatically handles pagination until all results are retrieved.

3. **Process Results**  
   - Extracts the `computer_name` and the latest `"Script results:"` line from each device’s logs.  
   - Prints the results to the terminal.
   - Errors are also captured 

```
Error: Script ran but produced no output
Error: No 'Script results:' in log
Error: No log data found
```

4. **Optional CSV Export**  
   - Prompts whether to save results in `Downloads`, `Desktop`, or `Documents`.  
   - If chosen, saves results as a timestamped CSV like:  
     ```
     Kandji-Export-Library-Status-b5d21f9e-9999-4444-3333-c292b3c2ccad-20250903-132045.csv
     ```

5. **User-Friendly Output**  
   - Uses ANSI escape codes (`RED`, `GREEN`, `BOLD`) for colorized prompts, warnings, and success messages.

---

## ✨ Features

- Query Kandji for any Library Item status report.  
- Pagination support to fetch **all devices**.  
- Friendly terminal prompts with colored output.  
- Optional CSV export to user’s **Downloads**, **Desktop**, or **Documents** folder.  
- Automatically skips invalid or empty results.

---

## Environment Variables

```
export kandji_api_token="your_api_token_here"
export kandji_domain="yourtenant"
```

## ✅ Example Run
```
Please specify the Kandji Library Item ID:
b5d21f9e-9d41-4463-b2b5-c292b3c2ccad

Type Downloads, Desktop, or Documents to save CSV in your user folder, or press Enter to skip if you do not want to export this report to a CSV file:
Downloads

MacBook-Pro,Echo Command Output-1
iMac-Office,Echo Command Output-2
✅ Saved CSV to: /Users/you/Downloads/Kandji-Export-Library-Status-b5d21f9e-9d41-4463-b2b5-c292b3c2ccad-20250903-132045.csv 💾📄
```

CSV Output Sample
```
computer_name	result
H9P0GQRRRR	No compromises found
LHG1VRRRRR	No compromises found
F6Y6P7RRRR	No compromises found
V2D64QRRRR	Compromised by oxc extension | An error occurred executing the item "VSCode Extensions Check [VULN - ISD-24241]": Script exited with non-zero status.
FVFHR33MQRRR	No compromises found
```


## Kandji Library Item Auto App - Audit

```
Kandji-Auto-App-Script-Audit.py
```

This Python script queries the [Kandji API](https://api-docs.kandji.io/#478764c4-638c-416c-b44c-3685a2f7b441) for the **status of a specific Auto App Library Item**. It extracts the installed version, available newer version, and update status for each device, prints the results to the terminal, and optionally exports them to a CSV file.

Kandji has a more complicated GitHub Script – for more info see [Device Library Items](https://github.com/kandji-inc/support/blob/main/api-tools/device-library-items/README.md)

---

## 🔎 What the Script Does

1. **Prompt for a Kandji Auto App Library Item ID**

   * Example: `b5d21f9e-9999-4444-3333-c292b3c2ccad`
   * The script builds the API request URL using your **Kandji domain** and **API token** (set as environment variables).

2. **Call the Kandji API**

   * Makes authenticated requests to Kandji’s `library-items/{id}/status` endpoint.
   * Automatically handles pagination until all devices are retrieved.

3. **Process Results**

   * Extracts the `computer_name`, `status`, `installed_version`, `available_version`, and `update_status`.
   * Handles devices that have not yet reported an audit (`last_audit_log = null`).
   * Prints the results to the terminal.

4. **Optional CSV Export**

   * Prompts whether to save results in `Downloads`, `Desktop`, or `Documents`.
   * Saves a timestamped CSV like:

     ```
     Kandji-Export-Library-Status-b5d21f9e-9d41-4463-b2b5-c292b3c2ccad-20250903-132045.csv
     ```

5. **User-Friendly Output**

   * Uses ANSI escape codes (`RED`, `GREEN`, `BOLD`) for colored prompts, warnings, and success messages.

---

## ✨ Features

* Query Kandji for any Auto App Library Item audit.
* Extract installed and available app versions.
* Detects whether devices are running the latest version.
* Handles devices that haven’t reported audit logs yet.
* Pagination support to fetch **all devices**.
* Optional CSV export to user’s **Downloads**, **Desktop**, or **Documents** folder.
* Colorized terminal output for clarity.

---

## Environment Variables

```
export kandji_api_token="your_api_token_here"
export kandji_domain="yourtenant"
```

---

## ✅ Example Run

```
Please specify the Auto App Kandji Library Item ID:
b5d21f9e-9999-4444-3333-c292b3c2ccad

Type Downloads, Desktop, or Documents to save CSV in your user folder, or press Enter to skip if you do not want to export this report to a CSV file:
Downloads

computer_name	status	result	audit_log
FVFJ2BFNQ6LR	PASS	Up-to-Date	Zoom Client for Meetings 6.5.12 (63499) (6.5.12.63499) is installed and up to date. Kandji is set to automatically enforce updates for Zoom Client for Meetings a week after they are released.
✅ Saved CSV to: /Users/you/Downloads/Kandji-Export-Library-Status-b5d21f9e-9999-4444-3333-c292b3c2ccad-20250903-132045.csv 💾📄
```

CSV Output Sample
```
computer_name	status	result	audit_log
J7XLYV6RRR	AVAILABLE	App-Not-Installed	Firefox is waiting for install through Self Service.
FVFJ2BFNQR	AVAILABLE	App-Not-Installed	Firefox is waiting for install through Self Service.
L6WYGP0RRR	PASS	Up-to-Date	Firefox 142.0.1 (14225.8.27) is installed and up to date. Kandji is set to automatically enforce updates for Firefox two weeks after they are released.
C59992JRRR	AVAILABLE	App-Not-Installed	Firefox is waiting for install through Self Service.
J444Y16RRR	AVAILABLE	App-Not-Installed	Firefox is waiting for install through Self Service.
C76QX07RRR	PASS	Up-to-Date	Firefox 142.0.1 (14225.8.27) is installed and up to date. Kandji is set to automatically enforce updates for Firefox two weeks after they are released.
GJ4DXPFRRR	AVAILABLE	App-Not-Installed	Firefox is waiting for install through Self Service.
FVFJRRRRRR	PASS	Update Available	Firefox 142.0 (14225.8.11) is installed. A newer version (142.0.1 (14225.8.27)) of Firefox is available. Kandji is set to automatically enforce updates two weeks after they are released.
```
