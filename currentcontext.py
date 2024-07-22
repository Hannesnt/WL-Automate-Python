import time
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    default_context = browser.contexts[0]
    pages = default_context.pages

    salesforcePage = ""
    ccPage = ""
    dhlPage = ""
    unifaunPage = ""
    for page in pages:
        if "bambora.lightning.force" in page.url:
            salesforcePage = page 
        if "cc.samport" in page.url:
            ccPage = page
        if "dhl" in page.url:
            dhlPage = page.url
        if "unifaun" in page.url:
            unifaunPage = page

            
    salesforcePage.get_by_role("link", name="02642509").click()
    salesforcePage.get_by_title("Share an update...").click()
    salesforcePage.get_by_label("Share an update...").fill(f"S/N: {"Rubenboy"} \n\nWAYBILL: ")
    # ---------------------
    time.sleep(10)
    #context.close()
    browser.close()

def main():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == '__main__':
    main()
