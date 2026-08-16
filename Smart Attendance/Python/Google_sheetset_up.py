sheet = None
try:
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = google.oauth2.service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
    print("Connected to Google Sheet.")
except Exception as e:
    print("Could not connect to Google Sheets - attendance will still be saved locally.")
    print("Reason:", e)

# ESP32 DevKit (fingerprint) - update COM port to match Device Manager
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)

# Map fingerprint IDs to names - fill this in based on what you enrolled
fingerprint_map = {
    1: "",
    2: "", 
}

FINGERPRINT_TIMEOUT = 10  # seconds to wait for a scan after a face is recognized