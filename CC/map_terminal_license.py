import time

class CC:
    def map_terminal_license(self, serialNumbers, ccPage, customer_info):
        for sn in range(len(serialNumbers)):
            ccPage.get_by_placeholder("Search here").click()
            ccPage.get_by_placeholder("Search here").fill(serialNumbers[sn])
            ccPage.get_by_placeholder("Search here").press("Enter")
            ccPage.get_by_role("link", name=f" {serialNumbers[sn]}").click()
            ccPage.get_by_role("button", name="Logistics").click()
            ccPage.get_by_role("link", name="Deliver").click()
            ccPage.get_by_role("link", name="Deliver").click()
            ccPage.locator("#DeliverTerminal").get_by_role("textbox").click()
            ccPage.locator("#DeliverTerminal").get_by_role("textbox").fill(customer_info['licenseNumber'][sn])
            ccPage.get_by_role("button", name="Deliver").click()
            time.sleep(2)