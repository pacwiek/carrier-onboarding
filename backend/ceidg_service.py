from playwright.sync_api import sync_playwright

from file_utils import (
    get_company_folder,
    safe_name
)


def download_ceidg_pdf(
    nip: str,
    company_name: str
):

    company_dir = get_company_folder(
        nip,
        company_name
    )

    pdf_path = (
        company_dir
        / f"{safe_name(company_name)}_CEIDG.pdf"
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--window-position=3000,3000"
            ]
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
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            page.wait_for_selector(
                "#MainContentForm_txtNip",
                timeout=60000
            )

            print("Pole NIP znalezione")

            page.click(
                "#MainContentForm_txtNip"
            )

            page.keyboard.type(
                nip,
                delay=100
            )

            page.wait_for_timeout(1000)

            page.click(
                "#MainContentForm_btnInputSearch"
            )

            print("Kliknięto SZUKAJ")

            page.wait_for_timeout(5000)

            page.wait_for_selector(
                "#MainContentForm_DataListEntities_hrefDetails_0",
                timeout=60000
            )

            page.click(
                "#MainContentForm_DataListEntities_hrefDetails_0"
            )

            print("Otworzono szczegóły")

            page.wait_for_timeout(5000)

            page.wait_for_selector(
                "#MainContentForm_btnPrint",
                timeout=60000
            )

            page.click(
                "#MainContentForm_btnPrint"
            )

            print("Kliknięto Pobierz PDF")

            page.wait_for_timeout(5000)

            page.wait_for_selector(
                "#MainContentForm_linkDownloadG",
                timeout=60000
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