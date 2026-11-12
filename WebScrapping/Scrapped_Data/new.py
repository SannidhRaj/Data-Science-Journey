from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    print("1. Playwright started")

    browser = p.chromium.launch(headless=False)

    print("2. Browser opened")

    page = browser.new_page()

    print("3. Page created")

    page.goto(
        "https://www.amazon.in/s?k=iphone",
        wait_until="domcontentloaded",
        timeout=30000
    )

    print("4. Amazon opened")

    print("Title:", page.title())

    print("5. Done")

    browser.close()

    print("6. Browser closed")
    