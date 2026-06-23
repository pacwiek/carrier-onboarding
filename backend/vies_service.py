from playwright.async_api import async_playwright


class ViesService:

    async def download_vies_pdf(
        self,
        country: str,
        vat_number: str,
        output_file: str
    ):

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            context = await browser.new_context()

            try:

                page = await context.new_page()

                await page.goto(
                    "https://ec.europa.eu/taxation_customs/vies/#/vat-validation"
                )

                await page.select_option(
                    "#select-country",
                    country
                )

                await page.locator(
                    '[formcontrolname="vatNumber"]'
                ).fill(vat_number)

                await page.locator(
                    '[data-testid="verifyBtn"]'
                ).click()

                await page.wait_for_url(
                    "**/vat-validation-result"
                )

                await page.wait_for_timeout(2000)

                await page.emulate_media(
                    media="print"
                )

                await page.pdf(
                    path=output_file,
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "10mm",
                        "bottom": "10mm",
                        "left": "10mm",
                        "right": "10mm"
                    }
                )

            finally:

                try:
                    await context.close()
                except Exception:
                    pass

                try:
                    await browser.close()
                except Exception:
                    pass