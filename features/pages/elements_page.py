# features/pages/elements_page.py
from .base_page import BasePage


class ElementsPage(BasePage):
    # Locators
    textBox_button = "text=Text Box"
    checkBox_button = "text=Radio Button"
    radioButton_button = "text=Web Tables"
    webTables_button = "text=Web Tables"
    buttons_button = "text=Buttons"
    links_button = "text=Links"
    brokenLinksImages_button = "text=Broken Links - Images"
    uploadAndDownload_button = "text=Upload and Download"
    dynamicProperties_button = "text=Dynamic Properties"

    async def open_section_form(self, section):
        await self.click_element(f"text={section}")
