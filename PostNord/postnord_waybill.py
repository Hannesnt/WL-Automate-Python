import time

class PostNordWaybill:
    def create_postnord_waybill(self, unifaunPage, serialNumbers, customer_info, caseNumber, default_context):

        self.edit_page_language_postnord(unifaunPage)

        self.shipping_box_postnord(unifaunPage, serialNumbers, customer_info, False)
        
        self.add_customer_data_postnord(unifaunPage, customer_info)
        
        self.shipment_reference_postnord(unifaunPage, customer_info, serialNumbers, caseNumber, False)

        self.dangerous_goods_postnord(unifaunPage, serialNumbers, customer_info, False)

        self.label_amount_postnord(unifaunPage, serialNumbers)

        unifaunPage.get_by_role("button", name="Print PDF").nth(1).click()
        if customer_info["subject"] == "ST" or customer_info["subject"] == "MMSW":
            return_label_page = default_context.new_page()
            return_label_page.goto("https://www.unifaunonline.com/jsapp/uo/start")
            time.sleep(2)
            return_label_page.get_by_role("button", name="Log in").click()
            time.sleep(1)
            return_label_page.get_by_role("button", name="Log in").click()
            time.sleep(1)
            return_label_page.get_by_role("button", name="Log in").click()
            time.sleep(2)

            self.edit_page_language_postnord(return_label_page)
            self.shipping_box_postnord(return_label_page, serialNumbers, customer_info, True)
            self.add_customer_data_postnord(return_label_page, customer_info)
            self.shipment_reference_postnord(return_label_page, customer_info, serialNumbers, caseNumber, True)
            self.dangerous_goods_postnord(return_label_page, serialNumbers, customer_info, True)
            self.label_amount_postnord(return_label_page, serialNumbers)
            return_label_page.get_by_role("button", name="Print PDF").nth(1).click()
    
    def label_amount_postnord(self, unifaunPage, serialNumbers):
        unifaunPage.locator("input[name=\"ParcelGroupCount\"]").click()
        if len(serialNumbers) > 74:
            unifaunPage.locator("input[name=\"ParcelGroupCount\"]").fill("5")
        elif len(serialNumbers) > 56:
            unifaunPage.locator("input[name=\"ParcelGroupCount\"]").fill("4")
        elif len(serialNumbers) > 36:
            unifaunPage.locator("input[name=\"ParcelGroupCount\"]").fill("3")
        elif len(serialNumbers) > 18:
            unifaunPage.locator("input[name=\"ParcelGroupCount\"]").fill("2")

    def dangerous_goods_postnord(self, unifaunPage, serialNumbers, customer_info, return_waybill):
        if len(serialNumbers) >= 3 and "move" in customer_info['model'].lower():
            if return_waybill:
                unifaunPage.locator("input[name=\"AddonsFDNG\"]").check()
            else:
                unifaunPage.locator("input[name=\"AddonsDNG\"]").check()

    def shipment_reference_postnord(self, unifaunPage, customer_info, serialNumbers, caseNumber, return_label):
        unifaunPage.locator("input[name=\"ShipmentSndReference\"]").click()
        if customer_info['subject'] == "ST" or customer_info["subject"] == "MMSW":
            if return_label == False:
                unifaunPage.locator("input[name=\"ShipmentSndReference\"]").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} {customer_info['subject']} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
                unifaunPage.locator("input[name=\"AddonsPRENOT\"]").check()
                unifaunPage.locator("input[name=\"AddonsDLVNOT\"]").check()
                unifaunPage.locator("input[name=\"AddonsPODNOT\"]").check()
            else:
                unifaunPage.locator("input[name=\"ShipmentSndReference\"]").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} R {customer_info['subject']} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
        else: 
            unifaunPage.locator("input[name=\"ShipmentSndReference\"]").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} {customer_info['subject'][0]} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
            unifaunPage.locator("input[name=\"AddonsPRENOT\"]").check()
            unifaunPage.locator("input[name=\"AddonsDLVNOT\"]").check()
            unifaunPage.locator("input[name=\"AddonsPODNOT\"]").check()
    def add_customer_data_postnord(self, unifaunPage, customer_info):
        unifaunPage.locator("input[name=\"RECEIVERName\"]").click()
        unifaunPage.locator("input[name=\"RECEIVERName\"]").fill(customer_info["name"])
        unifaunPage.locator("input[name=\"RECEIVERName\"]").press("Tab")
        unifaunPage.locator("input[name=\"RECEIVERDeliveryAddress1\"]").fill(customer_info["address"])
        if customer_info["country"] == 'SE':
            unifaunPage.locator("select[name=\"RECEIVERDeliveryCountry\"]").select_option("SE")
        elif customer_info["country"] == 'DK' or customer_info["country"] == 'da-DK':
            unifaunPage.locator("select[name=\"RECEIVERDeliveryCountry\"]").select_option("DK")
        elif customer_info["country"] == 'FI':
            unifaunPage.locator("select[name=\"RECEIVERDeliveryCountry\"]").select_option("FI")
        unifaunPage.locator("input[name=\"RECEIVERDeliveryZipcode\"]").click()
        unifaunPage.locator("input[name=\"RECEIVERDeliveryZipcode\"]").fill(customer_info["zip"])
        unifaunPage.locator("input[name=\"RECEIVERDeliveryCity\"]").click()
        unifaunPage.locator("input[name=\"RECEIVERDeliveryCity\"]").fill(customer_info['county'])
        unifaunPage.locator("div:nth-child(6) > .caption-row > .caption-row-entry").click()
        unifaunPage.locator("input[name=\"RECEIVERPhone\"]").click()
        unifaunPage.locator("input[name=\"RECEIVERPhone\"]").fill(customer_info["phone"])
        unifaunPage.locator("input[name=\"RECEIVEREmail\"]").click()
        unifaunPage.locator("input[name=\"RECEIVEREmail\"]").fill(customer_info["email"])
        unifaunPage.locator("input[name=\"RECEIVEREmail\"]").press("Tab")
        unifaunPage.locator("input[name=\"RECEIVERSms\"]").fill(customer_info["phone"])
        unifaunPage.get_by_role("button", name="Next").nth(1).click()

    def edit_page_language_postnord(self, unifaunPage):
        unifaunPage.get_by_test_id("wide-logo").click()
        time.sleep(1)
        try: 
            unifaunPage.get_by_label("en").click()
            time.sleep(1)
            unifaunPage.get_by_role("option", name="English").click()
        except:
            try:
                unifaunPage.get_by_label("sv").click()
                time.sleep(1)
                unifaunPage.get_by_role("option", name="English").click()
            except: 
                print("Failed to click both 'en' and 'sv' labels")
        time.sleep(1)
        unifaunPage.get_by_test_id("menuTopHeaderPrinting").click()
        time.sleep(1)
    def shipping_box_postnord(self, unifaunPage, serialNumbers, customer_info, return_label):
        unifaunPage.get_by_role("menuitem", name="Printing favorites").click()
        if len(serialNumbers) < 3 :
            unifaunPage.locator("button[name=\"act_ShipmentJobFavoriteSearchActions_SearchResultEdit_RowId_35093\"]").click()
            unifaunPage.locator("#RECEIVEREditRadioBtn").click()
            time.sleep(1)
            unifaunPage.get_by_role("button", name="Normal").click()
            time.sleep(1)
            unifaunPage.locator("select[name=\"SENDERList\"]").select_option("1188244")
            time.sleep(1)
            if return_label:
                if customer_info["country"] == "SE":
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P20|")
                else:
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P24|P24DPD|")
            else:
                unifaunPage.locator("select[name=\"Service\"]").select_option("|P18|P18DPD|")
            time.sleep(1)
        elif len(serialNumbers) > 2 and len(serialNumbers) < 7:
            unifaunPage.locator("button[name=\"act_ShipmentJobFavoriteSearchActions_SearchResultEdit_RowId_35095\"]").click()
            unifaunPage.locator("select[name=\"SENDERList\"]").select_option("1188244")
            time.sleep(1)
            unifaunPage.locator("span").filter(has_text="Normal").nth(1).click()
            time.sleep(1)
            if return_label:
                if customer_info["country"] == "SE":
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P20|")
                else:
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P24|P24DPD|")
            else:  
                unifaunPage.locator("select[name=\"Service\"]").select_option("|P18|P18DPD|")
            time.sleep(1)
            unifaunPage.locator("#RECEIVEREditRadioBtn").click()
        else: 
            unifaunPage.locator("button[name=\"act_ShipmentJobFavoriteSearchActions_SearchResultEdit_RowId_35096\"]").click()
            time.sleep(1)
            unifaunPage.locator("select[name=\"SENDERList\"]").select_option("1188244")
            time.sleep(1)
            if return_label:
                if customer_info["country"] == "SE":
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P20|")
                else:
                    unifaunPage.locator("select[name=\"Service\"]").select_option("|P24|P24DPD|")
            else:  
                unifaunPage.locator("select[name=\"Service\"]").select_option("|P18|P18DPD|")
            time.sleep(1)
            unifaunPage.locator("div:nth-child(13) > .block-wrapper > .block-corners > .block > .block-entry > .block-entry-toggle-buttons > span > .button-background > span:nth-child(2)").click()
            time.sleep(1)
            unifaunPage.locator("#RECEIVEREditRadioBtn").click()
            time.sleep(1)