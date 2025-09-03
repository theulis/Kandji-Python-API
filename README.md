# Kandji-Python-API


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
   - Example: `b5d21f9e-9d41-4463-b2b5-c292b3c2ccad`  
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
     Kandji-Export-Library-Status-b5d21f9e-9d41-4463-b2b5-c292b3c2ccad-20250903-132045.csv
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

## 📂 Example CSV Output

```
computer_name,result
MacBook-Pro,The device was rebooted 12 days ago
iMac-Office,The device was rebooted 3 days ago
```
## ✅ Example Run
```
Please specify the Kandji Library Item ID:
b5d21f9e-9d41-4463-b2b5-c292b3c2ccad

Type Downloads, Desktop, or Documents to save CSV in your user folder, or press Enter to skip if you do not want to export this report to a CSV file:
Downloads

MacBook-Pro,The device was rebooted 12 days ago
iMac-Office,The device was rebooted 3 days ago
✅ Saved CSV to: /Users/you/Downloads/Kandji-Export-Library-Status-b5d21f9e-9d41-4463-b2b5-c292b3c2ccad-20250903-132045.csv 💾📄
```

