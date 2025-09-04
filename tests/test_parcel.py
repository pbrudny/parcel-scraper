import unittest
from unittest.mock import patch, MagicMock
from scraper.parcel import get_parcel_number


class TestParcelScraper(unittest.TestCase):
    @patch("scraper.parcel.sync_playwright")
    def test_get_parcel_number_mocked(self, mock_playwright):
        """
        Test get_parcel_number using a mocked Playwright instance.
        Ensures the function returns the correct parcel number without
        hitting the real website.
        """
        # Mock browser, context, page, and locator
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_locator = MagicMock()

        # Setup the mock hierarchy
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.locator.return_value = mock_locator

        # Mock locator methods
        mock_locator.count.return_value = 1
        mock_locator.first.inner_text.return_value = "140504_5.0076.14/18"

        # Call the function (uses mocked browser)
     
        parcel_number = get_parcel_number("WA6M", "00538393", "0")

        # Assertions
        self.assertEqual(parcel_number, "140504_5.0076.14/18")
        mock_page.goto.assert_called_once()
        mock_page.get_by_role.assert_called()  # Form interactions attempted

    @patch("scraper.parcel.sync_playwright")
    def test_get_parcel_number_no_results(self, mock_playwright):
        """
        Test behavior when no parcel number is found (locator.count() == 0)
        """
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_locator = MagicMock()

        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.locator.return_value = mock_locator

        mock_locator.count.return_value = 0

        parcel_number = get_parcel_number("WA6M", "00000000", "0")
        self.assertIsNone(parcel_number)


if __name__ == "__main__":
    unittest.main()
