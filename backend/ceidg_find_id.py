from playwright.sync_api import sync_playwright
import re

NIP = "8171891458"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://aplikacja.ceidg.gov.pl/ceidg/ceidg.public.ui/search.aspx"
    )

    page.wait_for_timeout(3000)

    page.click("#MainContentForm_txtNip")
    page.keyboard.type(NIP, delay=100)

    page.wait_for_timeout(1000)

    page.locator("#MainContentForm_btnInputSearch").click()

    page.wait_for_timeout(3000)

    page.locator(
        "#MainContentForm_DataListEntities_hrefDetails_0"
    ).click()

    page.wait_for_timeout(3000)

    print(page.url)

    match = re.search(
        r"Id=([a-f0-9\-]+)",
        page.url,
        re.IGNORECASE
    )

    if match:
        print("CEIDG ID:")
        print(match.group(1))

    input("ENTER...")

    browser.close()