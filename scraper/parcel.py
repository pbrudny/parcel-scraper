from playwright.sync_api import sync_playwright, TimeoutError


def get_parcel_number(kod: str, number: str, control_digit: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()
        page.set_default_timeout(60000)

        # Go to search page
        page.goto(
            "https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW"
        )

        # Fill form & search
        page.get_by_role("textbox", name="Lista rozwijana wybierz kod").fill(kod)
        page.get_by_role("textbox", name="Wpisz numer księgi wieczystej").fill(number)
        page.get_by_role("textbox", name="Wpisz cyfrę kontrolną").fill(control_digit)
        page.get_by_role("button", name="Wyszukaj Księgę").click()

        # Try to open KW content
        try:
            button = page.get_by_role(
                "button", name="Przeglądanie aktualnej treści KW", exact=True
            )
            if button.count() == 0:
                return None
            button.click()
        except TimeoutError:
            return None

        # Grab parcel number
        locator = page.locator(
            "xpath=//td[normalize-space()='Identyfikator działki']/following-sibling::td[1]"
        )
        try:
            locator.wait_for(state="visible", timeout=10000)
        except TimeoutError:
            return None

        parcel_number = locator.first.inner_text().strip() if locator.count() > 0 else None

        browser.close()
        return parcel_number
