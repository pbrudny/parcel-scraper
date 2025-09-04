from playwright.sync_api import sync_playwright, TimeoutError


def get_parcel_data(kod: str, number: str, control_digit: str) -> dict:
    """
    Scrape KW data:
    - Typ księgi wieczystej
    - Położenie
    - Właściciel / użytkownik wieczysty / uprawniony
    - Parcel number (after opening KW content)

    Returns dict with fields or None if not available.
    """
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
        page.set_default_timeout(20000)

        # Go to search page
        page.goto(
            "https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW"
        )

        # Fill form & search
        page.get_by_role("textbox", name="Lista rozwijana wybierz kod").fill(kod)
        page.get_by_role("textbox", name="Wpisz numer księgi wieczystej").fill(number)
        page.get_by_role("textbox", name="Wpisz cyfrę kontrolną").fill(control_digit)
        page.get_by_role("button", name="Wyszukaj Księgę").click()

        # Check if KW not found
        if page.locator("text=nie została odnaleziona").count() > 0:
            browser.close()
            return None
        
        # Extract general info before opening KW content
        def get_field(label_text: str) -> str | None:
            locator = page.locator(
                f"xpath=//label[normalize-space()='{label_text}']/../following-sibling::div//div[@class='left']"
            )
            if locator.count() > 0:
                return locator.first.inner_text().strip()
            return None

        typ_ksiegi = get_field("Typ księgi wieczystej")
        polozenie = get_field("Położenie")
        wlasciciel = get_field(
            "Właściciel / użytkownik wieczysty / uprawniony"
        )

        parcel_number = None
        # Try to open KW content
        try:
            button = page.get_by_role(
                "button", name="Przeglądanie aktualnej treści KW", exact=True
            )
            if button.count() > 0:
                button.click()

                locator = page.locator(
                    "xpath=//td[normalize-space()='Identyfikator działki']/following-sibling::td[1]"
                )
                try:
                    locator.wait_for(state="visible", timeout=10000)
                    if locator.count() > 0:
                        parcel_number = locator.first.inner_text().strip()
                except TimeoutError:
                    parcel_number = None
        except TimeoutError:
            parcel_number = None

        browser.close()

        return {
            "typ_ksiegi": typ_ksiegi,
            "polozenie": polozenie,
            "wlasciciel": wlasciciel,
            "parcel_number": parcel_number,
        }
