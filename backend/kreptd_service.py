from playwright.sync_api import sync_playwright


def test_kreptd():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto("https://kreptd.gitd.gov.pl/")

        page.wait_for_timeout(5000)

       

        page.locator("#TaxNumber").fill("7951606800")

        recaptcha = page.frame_locator(
            "iframe[src*='recaptcha/api2/anchor']"
        )

        recaptcha.locator("#recaptcha-anchor").click()

        print("Strona została otwarta.")

        input("Naciśnij Enter, aby zamknąć przeglądarkę...")

        browser.close()


if __name__ == "__main__":
    test_kreptd()