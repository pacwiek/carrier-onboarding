from playwright.sync_api import sync_playwright

from file_utils import (
    get_company_folder,
    safe_name
)


def download_ceidg_sc_pdfs(
    nip: str,
    company_name: str
):

    company_dir = get_company_folder(
        nip,
        company_name
    )

    downloaded_files = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context(
            accept_downloads=True,
            viewport={
                "width": 350,
                "height": 120
            }
        )

        try:

            page = context.new_page()

            print("Otwieram CEIDG...")

            page.goto(
                "https://aplikacja.ceidg.gov.pl/ceidg/ceidg.public.ui/search.aspx",
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(5000)

            page.click(
                "#MainContentForm_txtPartnershipNIP"
            )

            page.keyboard.type(
                nip,
                delay=100
            )

            page.wait_for_timeout(1000)

            page.keyboard.press("Enter")

            page.wait_for_timeout(5000)

            details_buttons = page.locator(
                "text=SZCZEGÓŁY"
            )

            count = details_buttons.count()

            print(
                f"Znaleziono wspólników: {count}"
            )

            for i in range(count):

                print(
                    f"Pobieram wspólnika {i + 1}/{count}"
                )

                page.goto(
                    "https://aplikacja.ceidg.gov.pl/ceidg/ceidg.public.ui/search.aspx",
                    wait_until="domcontentloaded"
                )

                page.wait_for_timeout(3000)

                page.click(
                    "#MainContentForm_txtPartnershipNIP"
                )

                page.keyboard.type(
                    nip,
                    delay=100
                )

                page.keyboard.press("Enter")

                page.wait_for_timeout(5000)

                details_buttons = page.locator(
                    "text=SZCZEGÓŁY"
                )

                details_buttons.nth(i).click()

                page.wait_for_timeout(5000)

                entrepreneur_name = (
                    f"WSPOLNIK_{i + 1}"
                )

                print(
                    "Wspólnik:",
                    entrepreneur_name
                )

                pdf_path = (
                    company_dir
                    / (
                        f"{safe_name(entrepreneur_name)}"
                        "_CEIDG.pdf"
                    )
                )

                print(
                    "Klikam Pobierz PDF..."
                )

                page.click(
                    "#MainContentForm_btnPrint"
                )

                page.wait_for_timeout(3000)

                page.wait_for_selector(
                    "#MainContentForm_linkDownloadG",
                    timeout=60000
                )

                print(
                    "Klikam Pobierz plik..."
                )

                with page.expect_download(
                    timeout=60000
                ) as download_info:

                    page.click(
                        "#MainContentForm_linkDownloadG"
                    )

                download = download_info.value

                download.save_as(
                    str(pdf_path)
                )

                downloaded_files.append(
                    str(pdf_path)
                )

                print(
                    f"Zapisano: {pdf_path}"
                )

            return downloaded_files

        finally:

            try:
                context.close()
            except Exception:
                pass

            try:
                browser.close()
            except Exception:
                pass