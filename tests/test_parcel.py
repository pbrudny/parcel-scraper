import unittest
from unittest.mock import patch, MagicMock
from scraper.parcel import get_parcel_data

class TestParcelMocked(unittest.TestCase):
    @patch("scraper.parcel.sync_playwright")
    def test_valid_parcel_mocked(self, mock_playwright):
        # Setup mock browser, context, page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        # Mock Playwright context
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.set_default_timeout.return_value = None
        mock_page.goto.return_value = None
        
        # Mock get_by_role (for form filling and button click)
        mock_page.get_by_role.return_value.count.return_value = 1
        mock_page.get_by_role.return_value.click.return_value = None
        mock_page.get_by_role.return_value.fill.return_value = None

        # Mock locators
        def locator_side_effect(*args, **kwargs):
            mock_locator = MagicMock()
            # If checking "KW not found", simulate found
            if "nie została odnaleziona" in args[0]:
                mock_locator.count.return_value = 0
            else:
                mock_locator.count.return_value = 1
            mock_locator.first.inner_text.return_value = "Mocked Value"
            mock_locator.wait_for.return_value = None
            return mock_locator

        mock_page.locator.side_effect = locator_side_effect

        # Call function
        result = get_parcel_data("WAW", "12345", "6")
        
        # Assert results
        self.assertIsInstance(result, dict)
        self.assertEqual(result["typ_ksiegi"], "Mocked Value")
        self.assertEqual(result["polozenie"], "Mocked Value")
        self.assertEqual(result["wlasciciel"], "Mocked Value")
        self.assertEqual(result["parcel_number"], "Mocked Value")

    @patch("scraper.parcel.sync_playwright")
    def test_parcel_not_found_mocked(self, mock_playwright):
        # Setup mock browser, context, page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Simulate KW not found
        mock_page.locator.return_value.count.return_value = 1
        mock_page.locator.return_value.first.inner_text.return_value = "nie została odnaleziona"

        # Call function
        result = get_parcel_data("XYZ", "00000", "0")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
