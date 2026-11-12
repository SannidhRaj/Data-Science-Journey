from playwright.sync_api import sync_playwright
import csv
import re


BASE_URL = "https://www.amazon.in/s?k=iphone"

MAX_PAGES = 20


with sync_playwright() as p:

    # -----------------------------
    # 1. Open browser
    # -----------------------------
    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        viewport={"width": 1366, "height": 900}
    )

    all_products = []

    # -----------------------------
    # 2. Loop through search pages
    # -----------------------------
    for page_number in range(1, MAX_PAGES + 1):

        if page_number == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}&page={page_number}"

        print("\nOpening page:", page_number)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("Page opened")

        # -----------------------------
        # 3. Find product cards
        # -----------------------------
        products = page.locator(
            '[data-component-type="s-search-result"]'
        )

        count = products.count()

        print("Products found:", count)

        if count == 0:
            print("No more products.")
            break

        # -----------------------------
        # 4. Extract products
        # -----------------------------
        for i in range(count):

            product = products.nth(i)

            # -------------------------
            # Product title
            # -------------------------
            try:
                name = product.locator("h2").inner_text().strip()
            except:
                continue

            # Only keep iPhone products
            if "iphone" not in name.lower():
                continue

            # -------------------------
            # Price
            # -------------------------
            try:
                price = product.locator(
                    ".a-price .a-offscreen"
                ).first.inner_text().strip()
            except:
                price = ""

            # -------------------------
            # Product URL
            # -------------------------
            try:
                link = product.locator(
                    "h2 a"
                ).get_attribute("href")

                if link and link.startswith("/"):
                    link = "https://www.amazon.in" + link

            except:
                link = ""

            # -------------------------
            # ASIN
            # -------------------------
            try:
                asin = product.get_attribute(
                    "data-asin"
                )
            except:
                asin = ""

            # -------------------------
            # Storage extraction
            # -------------------------
            storage_match = re.search(
                r"\b(64GB|128GB|256GB|512GB|1TB|2TB)\b",
                name,
                re.IGNORECASE
            )

            if storage_match:
                storage = storage_match.group(1)
            else:
                storage = ""

            # -------------------------
            # Save product
            # -------------------------
            all_products.append({
                "Model / Product": name,
                "Storage": storage,
                "Price": price,
                "ASIN": asin,
                "URL": link
            })

            print(
                f"{len(all_products)}. "
                f"{name[:80]} | {price}"
            )

    # -----------------------------
    # 5. Remove duplicate products
    # -----------------------------
    unique_products = {}

    for product in all_products:

        key = product["ASIN"]

        if key:
            unique_products[key] = product
        else:
            unique_products[
                product["Model / Product"]
            ] = product

    all_products = list(unique_products.values())

    # -----------------------------
    # 6. Save CSV
    # -----------------------------
    filename = "amazon_iphone_prices.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Model / Product",
                "Storage",
                "Price",
                "ASIN",
                "URL"
            ]
        )

        writer.writeheader()

        writer.writerows(all_products)

    # -----------------------------
    # 7. Final output
    # -----------------------------
    print("\n-----------------------------")
    print("SCRAPING COMPLETED")
    print("-----------------------------")

    print(
        "Total unique iPhone listings:",
        len(all_products)
    )

    print(
        "Saved file:",
        filename
    )

    browser.close()