from dataclasses import dataclass
import random
from playwright.async_api import async_playwright

async def svg_to_png_bytes(response_text: str) -> bytes:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 150, "height": 50},
            device_scale_factor=4,
        )

        await page.set_content(response_text)
        png_bytes = await page.locator("svg").screenshot()

        await browser.close()
        return png_bytes

@dataclass
class Person():
    id: str
    name: str
    phone_id: str
    email: str

def get_random_phone_id():
    return "139" + str(random.randint(00000000, 99999999))

# print(get_random_phone_id())