import os
import time
import random
from playwright.sync_api import sync_playwright

d_companies = {
    "Tesla": {"ticker": "TSLA", "exchange": "NASDAQ", "country": "US"},
    "BMW": {"ticker": "BMW.DE", "exchange": "Xetra", "country": "EU"},
    "Volkswagen": {"ticker": "VOW3.DE", "exchange": "Xetra", "country": "EU"},
    "Benz": {"ticker": "MBG.DE", "exchange": "Xetra", "country": "EU"},
    "Toyota": {"ticker": "7203.T", "exchange": "Tokyo", "country": "JP"},
    "Stellantis": {"ticker": "STLA", "exchange": "NYSE", "country": "EU"},
    # "Bosch": {"ticker": "BOS.IN", "exchange": "IN", "country": "IN"},
    "Apple": {"ticker": "AAPL", "exchange": "NASDAQ", "country": "US"},
    # "Microsoft": {"ticker": "MSFT", "exchange": "NASDAQ", "country": "US"},
    "Intel": {"ticker": "INTC", "exchange": "NASDAQ", "country": "US"},
    "Qualcomm": {"ticker": "QCOM", "exchange": "NASDAQ", "country": "US"},
    # "Nvdia": {"ticker": "NVDA", "exchange": "NASDAQ", "country": "US"},
    # "SAP": {"ticker": "SAP", "exchange": "NYSE / Xetra", "country": "EU"},
    "IBM": {"ticker": "IBM", "exchange": "NYSE", "country": "US"},
    # "Jpmorgan": {"ticker": "JPM", "exchange": "NYSE", "country": "US"},
    # "Goldman": {"ticker": "GS", "exchange": "NYSE", "country": "US"},
    # "HSBC": {"ticker": "HSBC", "exchange": "NYSE", "country": "EU"},
    # "Blackrock": {"ticker": "BLK", "exchange": "NYSE", "country": "US"},
    # "Citigroup": {"ticker": "C", "exchange": "NYSE", "country": "US"},
    # "Pfizer": {"ticker": "PFE", "exchange": "NYSE", "country": "US"},
    "J&J": {"ticker": "JNJ", "exchange": "NYSE", "country": "US"},
    # "Nestle": {"ticker": "NESN.SW", "exchange": "Swiss", "country": "EU"},
    # "Loreal": {"ticker": "OR.PA", "exchange": "Paris", "country": "EU"},
    # "Shiseido": {"ticker": "4911.T", "exchange": "Tokyo", "country": "JP"},
    # "P&G": {"ticker": "PG", "exchange": "NYSE", "country": "US"},
    # "AstraZeneca": {"ticker": "AZN", "exchange": "LSE", "country": "EU"},
    # "Novartis": {"ticker": "NVS", "exchange": "NYSE", "country": "US"},
}

d_companies.update({
    # "General Motors Co": {"ticker": "GM", "exchange": "NYSE", "country": "US"},
    # "MONOLITHIC POWER SYSTEMS INC": {"ticker": "MPWR", "exchange": "NASDAQ", "country": "US"},
    # "Aptiv PLC": {"ticker": "APTV", "exchange": "NYSE", "country": "US"},
    # "FORD MOTOR CO": {"ticker": "F", "exchange": "NYSE", "country": "US"},
    # "Viatris Inc": {"ticker": "VTRS", "exchange": "NASDAQ", "country": "US"},
    # "METTLER TOLEDO INTERNATIONAL INC/": {"ticker": "MTD", "exchange": "NYSE", "country": "US"},
    # "INTUITIVE SURGICAL INC": {"ticker": "ISRG", "exchange": "NASDAQ", "country": "US"},
    # "Merck & Co": {"ticker": "MRK", "exchange": "NYSE", "country": "US"},
    # "MICRON TECHNOLOGY INC": {"ticker": "MU", "exchange": "NYSE", "country": "US"},
    # "CORNING INC NY": {"ticker": "GLW", "exchange": "NYSE", "country": "US"},
    # "Super Micro Computer": {"ticker": "SMCI", "exchange": "NASDAQ", "country": "US"},
    # "BIO-TECHNE Corp": {"ticker": "TECH", "exchange": "NASDAQ", "country": "US"},
    # "APPLIED MATERIALS INC": {"ticker": "AMAT", "exchange": "NASDAQ", "country": "US"},
    # "DANAHER CORP": {"ticker": "DHR", "exchange": "NYSE", "country": "US"},
    # "ADVANCED MICRO DEVICES INC": {"ticker": "AMD", "exchange": "NASDAQ", "country": "US"},
    # "KLA CORP": {"ticker": "KLAC", "exchange": "NASDAQ", "country": "US"},
    # "Zoetis": {"ticker": "ZTS", "exchange": "NYSE", "country": "US"},
    # "MICROCHIP TECHNOLOGY INC": {"ticker": "MCHP", "exchange": "NASDAQ", "country": "US"},
    # "LAM RESEARCH CORP": {"ticker": "LRCX", "exchange": "NASDAQ", "country": "US"},
    # "Arista Networks": {"ticker": "ANET", "exchange": "NYSE", "country": "US"},
    # "TELEDYNE TECHNOLOGIES INC": {"ticker": "TDY", "exchange": "NYSE", "country": "US"},
    # "CISCO SYSTEMS": {"ticker": "CSCO", "exchange": "NASDAQ", "country": "US"},
    # "ON SEMICONDUCTOR CORP": {"ticker": "ON", "exchange": "NASDAQ", "country": "US"},
    # "TERADYNE": {"ticker": "TER", "exchange": "NASDAQ", "country": "US"},
    # "WATERS CORP": {"ticker": "WAT", "exchange": "NYSE", "country": "US"},
    # "FERRARI NV": {"ticker": "RACE", "exchange": "NYSE", "country": "EUR"},
    # "NOKIA OYJ": {"ticker": "NOKIA", "exchange": "Nasdaq Helsinki", "country": "EUR"},
    # "LOGITECH INTERNATIONAL-REG": {"ticker": "LOGN", "exchange": "SIX Swiss Exchange", "country": "EUR"},
    # "MERCK": {"ticker": "MRK", "exchange": "Xetra", "country": "EUR"},
    # "STMICROELECTRONICS NV": {"ticker": "STMMI", "exchange": "Borsa Italiana", "country": "EUR"},
    # "ASML HOLDING NV": {"ticker": "ASML", "exchange": "Euronext Amsterdam", "country": "EUR"},
    # "AMGEN INC": {"ticker": "AMGN", "exchange": "NASDAQ", "country": "EUR"},
    # "ELI LILLY": {"ticker": "LLY", "exchange": "NYSE", "country": "EUR"},
    # "ERICSSON LM-B SHS": {"ticker": "ERICB", "exchange": "Nasdaq Stockholm", "country": "EUR"},
    # "MEDTRONIC PLC": {"ticker": "MDT", "exchange": "NYSE", "country": "EUR"},
    # "ABBOTT LABORATORIES": {"ticker": "ABT", "exchange": "NYSE", "country": "EUR"}
})

output_dir = "annual_reports"

def get_slug(name, data):
    """Generates the AnnualReports.com slug logic."""
    if name == "Bosch": return None
    
    # --- UPDATED MANUAL OVERRIDES ---
    if name == "BMW": return "OTC_BAMGF"
    if name == "Volkswagen": return "OTC_VWAGY"
    if name == "Benz": return "OTC_MBGAF"
    if name == "Nestle": return "OTC_NSRGY"
    
    # Other Manual Overrides
    if name == "Toyota": return "NYSE_TM"
    if name == "Loreal": return "Loreal_SA"
    if name == "Shiseido": return "Shiseido_Company_Limited"

    # Standard "EXCHANGE_TICKER" logic
    exchange = data['exchange']
    ticker = data['ticker']
    if "NYSE" in exchange: return f"NYSE_{ticker}"
    if "NASDAQ" in exchange: return f"NASDAQ_{ticker}"
    if "LSE" in exchange: return f"LSE_{ticker}"
    return None

def download_reports_sync():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with sync_playwright() as p:
        # We still launch the browser to generate valid cookies/headers
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # We don't even need 'page' for the download, we use the context's request API
        # but we create one just to hold the session alive visually if you want to watch
        page = context.new_page()

        print("--- Starting Download Loop (API Fetch Mode) ---")

        for company_name, data in d_companies.items():
            slug = get_slug(company_name, data)
            if not slug: continue

            # Clean slug logic
            clean_slug = slug.replace("NASDAQ_", "").replace("NYSE_", "").replace("OTC_", "")
            first_letter = clean_slug[0].lower()
            if slug == "LSE_AZN":
                first_letter = "a"

            if slug == "NYSE_GLW":
                first_letter = "c"

            if slug == "NASDAQ_TECH":
                first_letter = "b"

            if slug == "NYSE_RACE":
                first_letter = "f"

            company_folder = os.path.join(output_dir, company_name)
            if not os.path.exists(company_folder):
                os.makedirs(company_folder)

            print(f"\nProcessing {company_name}...")

            for year in range(2024, 2026):
                filename = f"{slug}_{year}.pdf"
                print(first_letter)
                print(filename)
                
                url = f"https://www.annualreports.com/HostedData/AnnualReports/PDF/{filename}"
                print(url)
                
                save_path = os.path.join(company_folder, filename)

                if os.path.exists(save_path):
                    continue
                
                try:
                    # Random throttle
                    time.sleep(random.uniform(10, 15))

                    # This fetches the file stream directly, bypassing the PDF Viewer
                    response = context.request.get(url)

                    if response.status == 200:
                        body = response.body()
                        
                        # Validate it is actually a PDF (Magic bytes %PDF)
                        if body.startswith(b'%PDF'):
                            with open(save_path, 'wb') as f:
                                f.write(body)
                            print(f"  [SUCCESS] {filename} ({len(body)//1024} KB)")
                        else:
                            # If it's 200 OK but not a PDF, it's likely the HTML redirect/error page
                            print(f"  [FAILED] {filename} - Content was HTML/Text, not PDF. (Size: {len(body)} bytes)")
                    
                    elif response.status == 404:
                        print(f"  [404] Not Found: {year}")
                    
                    elif response.status == 429:
                        print(f"  [429] Rate Limit. Pausing 60s...")
                        time.sleep(60)

                except Exception as e:
                    print(f"  [ERROR] {e}")

        browser.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    download_reports_sync()