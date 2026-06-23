from playwright.sync_api import sync_playwright

from file_utils import (
    get_company_folder,
    safe_name
)


def download_regon_pdf(
    nip: str,
    company_name: str
):

    company_dir = get_company_folder(
        nip,
        company_name
    )

    pdf_path = (
        company_dir
        / f"{safe_name(company_name)}_REGON.pdf"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            viewport={
                "width": 1280,
                "height": 900
            }
        )

        try:

            page = context.new_page()

            print("Otwieram REGON...")

            page.goto(
                "https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx",
                wait_until="networkidle"
            )

            print("Wpisuję NIP...")

            page.fill(
                "#txtNip",
                nip
            )

            print("Klikam Szukaj...")

            page.click(
                "#btnSzukaj"
            )

            page.wait_for_timeout(3000)

            print("Otwieram szczegóły...")

            page.locator(
                "a[href*='danePobierzPelnyRaport']"
            ).first.click()

            page.wait_for_timeout(2000)

            print("Generuję PDF...")

            page.emulate_media(
                media="print"
            )

            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={
                    "top": "10mm",
                    "bottom": "10mm",
                    "left": "10mm",
                    "right": "10mm"
                }
            )

            print("PDF zapisany:")
            print(pdf_path)

            return str(pdf_path)

        finally:

            try:
                context.close()
            except Exception:
                pass

            try:
                browser.close()
            except Exception:
                pass