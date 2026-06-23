import os

from playwright.sync_api import sync_playwright

from file_utils import (
    get_company_folder,
    safe_name
)


def download_krs_pdf(
    nip: str,
    company_name: str
):

    company_dir = get_company_folder(
        nip,
        company_name
    )

    pdf_path = (
        company_dir
        / f"{safe_name(company_name)}_KRS.pdf"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            accept_downloads=True
        )

        try:

            page = context.new_page()

            print("Otwieram KRS...")

            page.goto(
                "https://wyszukiwarka-krs.ms.gov.pl",
                wait_until="networkidle"
            )

            print("Wpisuję NIP...")

            page.locator("input").nth(4).fill(
                nip
            )

            print("Klikam Wyszukaj...")

            page.get_by_role(
                "button",
                name="Wyszukaj"
            ).click()

            page.wait_for_timeout(3000)

            print("Otwieram szczegóły...")

            page.get_by_text(
                "Wyświetl szczegóły"
            ).click()

            page.wait_for_timeout(3000)

            print("Pobieram PDF...")

            with page.expect_download(
                timeout=60000
            ) as download_info:

                page.locator(
                    "button"
                ).nth(19).click()

            download = download_info.value

            download.save_as(
                str(pdf_path)
            )

            try:

                temp_file = download.path()

                if (
                    temp_file
                    and os.path.exists(temp_file)
                ):

                    os.remove(
                        temp_file
                    )

            except Exception as e:

                print(
                    "Nie udało się usunąć pliku tymczasowego:",
                    e
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