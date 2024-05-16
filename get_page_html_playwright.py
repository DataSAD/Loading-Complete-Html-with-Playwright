from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.riaa.com/gold-platinum/')

    while True:
        try:
            load_more_button = page.get_by_text('LOAD MORE RESULTS')
            load_more_button.click()
        except:
            break

    more_details_list = page.locator('div.format_details a').all()

    for item in more_details_list:
        item.click()

    page.wait_for_timeout(10000)

    page_html = page.content()

    with open('page_html.txt', 'w') as f:
        f.write(page_html)