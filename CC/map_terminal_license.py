import time
import requests
import json
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
            ccPage.locator("#DeliverTerminal").get_by_role("textbox").fill(customer_info['license'][sn])
            ccPage.get_by_role("button", name="Deliver").click()
            time.sleep(2)
    def sr_handle_merchant(self, serialNumbers, ccPage, customer_info):
        token = ccPage.evaluate("window.sessionStorage.getItem('instore-api-token')")
        if token:
            token_value = json.loads(token)
            url = f"https://api.instore.bambora.com/api/terminals/{customer_info['serialNumber']}?embed=hostconfiguration&embed=capabilities&embed=history&embed=ecr&embed=logsettings&embed=SoftwareHistory&embed=logistics"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Authorization': f"Bearer {token_value['token']}"
            }
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    customer_info['country'] = data['merchant']['country']
                    customer_info['accountNumber'] = str(data['merchant']['id'])
                    customer_info['stockLocation'] = data['logistics']['stock']['stockLocation']['name']
            except:
                print("Couldnt fetch cc")

        self.change_terminal_stock(ccPage, customer_info, serialNumbers[0])
        time.sleep(2)

        if customer_info['keepAlive'] == False:
            ccPage.get_by_placeholder("Search here").click()
            ccPage.get_by_placeholder("Search here").fill(customer_info['serialNumber'])
            time.sleep(2)
            ccPage.get_by_placeholder("Search here").press("Enter")
            ccPage.get_by_role("button", name="Logistics").click()
            ccPage.get_by_role("link", name="Swap").click()
            ccPage.locator("#SwapTerminal").get_by_role("textbox").click()
            ccPage.locator("#SwapTerminal").get_by_role("textbox").fill(serialNumbers[0])
            ccPage.get_by_role("button", name="Swap")
        elif customer_info['keepAlive'] == True:
            ccPage.get_by_role("button", name="Logistics").click()
            ccPage.get_by_role("link", name="Deliver").click()
            ccPage.get_by_role("combobox").nth(1).select_option("Merchant")
            ccPage.get_by_label("", exact=True).click()
            ccPage.locator("input[type=\"search\"]").fill(customer_info['accountNumber'])
            time.sleep(4)
            ccPage.locator("input[type=\"search\"]").press("Enter")
            ccPage.get_by_role("button", name="Deliver").click()
            time.sleep(2)
            ccPage.get_by_role("button", name="Actions").click()
            ccPage.get_by_role("link", name="Create virtual license").click()
            ccPage.get_by_placeholder("Payment license ID").click()
            ccPage.get_by_placeholder("Payment license ID").fill(customer_info['license'])
            ccPage.get_by_role("button", name="Fetch").click()
            ccPage.get_by_role("button", name="Create").click()
            time.sleep(2)
    def change_terminal_stock(self, ccPage, customer_info, serialNumber):
        ccPage.get_by_placeholder("Search here").click()
        ccPage.get_by_placeholder("Search here").fill(serialNumber)
        time.sleep(1)
        ccPage.get_by_placeholder("Search here").press("Enter")
        ccPage.get_by_role("button", name="Logistics").click()
        ccPage.get_by_role("link", name="Move to different stock").click()
        if customer_info['stockLocation'] == 'RentalStock' or customer_info['stockLocation'] == 'RentalSwapStock':
            ccPage.get_by_role("combobox").select_option("RentalSwapStock")
        elif customer_info['stockLocation'] == 'SaleStock' or customer_info['stockLocation'] == 'SaleSwapStock':
            ccPage.get_by_role("combobox").select_option("SaleSwapStock")
        ccPage.get_by_role("button", name="Move").click()


        