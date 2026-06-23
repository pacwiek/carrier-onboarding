from playwright.sync_api import sync_playwright
import re
import os

NIP = "8171891458"

DOWNLOAD_DIR = r"C:\Przewoznicy\downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        accept_downloads=True
    )

    page = context.new_page()

    page.goto(
        "https://aplikacja.ceidg.gov.pl/ceidg/ceidg.public.ui/search.aspx"
    )

    page.wait_for_timeout(3000)

    # NIP
    page.click("#MainContentForm_txtNip")
    page.keyboard.type(NIP, delay=100)

    page.wait_for_timeout(1000)

    # SZUKAJ
    page.locator("#MainContentForm_btnInputSearch").click()

    page.wait_for_timeout(3000)

    # SZCZEGÓŁY
    page.locator(
        "#MainContentForm_DataListEntities_hrefDetails_0"
    ).click()

    page.wait_for_timeout(3000)

    print("\nURL:")
    print(page.url)

    match = re.search(
        r"Id=([a-f0-9\-]+)",
        page.url,
        re.IGNORECASE
    )

    if match:
        ceidg_id = match.group(1)

        print("\nCEIDG ID:")
        print(ceidg_id)

    # KLIK POBIERZ PDF
    page.locator(
        "#MainContentForm_btnPrint"
    ).click()

    page.wait_for_timeout(5000)

    # KLIK POBIERZ PLIK + PRZECHWYCENIE DOWNLOADU
    with page.expect_download(timeout=30000) as download_info:

        page.locator(
            "#MainContentForm_linkDownloadG"
        ).click()

    download = download_info.value

    print("\nPobrano plik:")
    print(download.suggested_filename)

    pdf_path = rf"{DOWNLOAD_DIR}\{NIP}.pdf"

    download.save_as(pdf_path)

    print("\nZapisano:")
    print(pdf_path)

    input("\nENTER aby zakończyć...")

    browser.close()