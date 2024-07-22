class DHLWaybill:
    def create_dhl_waybill(self, dhl_page, customer_info, serialNumbers, caseNumber, default_context):
        
        self.add_customer_data_dhl(dhl_page, customer_info, False)

        self.goods_description_dhl(dhl_page, serialNumbers)

        self.dhl_label_amount(dhl_page, serialNumbers)

        self.shipment_reference_dhl(dhl_page, customer_info, serialNumbers, caseNumber, False)

        self.dhl_label_amount_dangerous_goods(dhl_page, customer_info, serialNumbers)

        self.print_label_dhl(dhl_page)

        if customer_info["subject"] == "ST" or customer_info["subject"] == "MMSW":
            dhl_return_label = default_context.new_page()
            dhl_return_label.goto("https://mydhl.express.dhl/se/sv/home.html?login=successful#/createNewShipmentTab")
            self.add_customer_data_dhl(dhl_return_label, customer_info, True)

            self.goods_description_dhl(dhl_return_label, serialNumbers)

            self.dhl_label_amount(dhl_return_label, serialNumbers)

            self.shipment_reference_dhl(dhl_return_label, customer_info, serialNumbers, caseNumber, True)

            self.dhl_label_amount_dangerous_goods(dhl_return_label, customer_info, serialNumbers)

            self.print_label_dhl(dhl_return_label)


    def print_label_dhl(self, dhl_page):
        dhl_page.locator("#ewfc-submit-blocker-element").get_by_text("Nej").click()
        dhl_page.get_by_role("button", name="Godkänn och fortsätt").click()
        dhl_page.get_by_text("Skicka in", exact=True).click()
        dhl_page.get_by_text("Kvitto").click()
        dhl_page.get_by_role("button", name=" Skriv ut fraktsedel").click()

    def shipment_reference_dhl(self, dhl_page, customer_info, serialNumbers, caseNumber, return_waybill):
        dhl_page.get_by_placeholder("Referens (kommer synas på").click()
        if customer_info['subject'] == "ST" or customer_info['subject'] == "MMSW":
            if return_waybill == True:
                dhl_page.get_by_placeholder("Referens (kommer synas på").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} R {customer_info['subject']} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
            else:
                dhl_page.get_by_placeholder("Referens (kommer synas på").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} {customer_info['subject']} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
        else:
            dhl_page.get_by_placeholder("Referens (kommer synas på").fill(f"{customer_info['country'][0]}{customer_info['country'][1]} {customer_info['subject'][0]} {len(serialNumbers)} {customer_info['model'][0]} - {caseNumber}")
        dhl_page.get_by_label("Välj handelsvillkor Se").select_option("DDP")
        dhl_page.get_by_text("Välj", exact=True).nth(1).click()

    def goods_description_dhl(self, dhl_page, serialNumbers):
        dhl_page.get_by_placeholder("Fyll i godsbeskrivning (170").click()
        dhl_page.get_by_text("Payment terminals Payment").click()
        dhl_page.get_by_label("Vikt (Per artikel) Vad varje").click()
        dhl_page.get_by_label("Vikt (Per artikel) Vad varje").fill(f"{len(serialNumbers)}")

    def add_customer_data_dhl(self, dhl_page, customer_info, return_waybill):
        dhl_page.get_by_text("Skicka", exact=True).click()
        dhl_page.get_by_role("link", name="Skapa en försändelse").click()
        dhl_page.get_by_label("Namn Obligatorisk Adressbok").click()
        dhl_page.get_by_label("Namn Obligatorisk Adressbok").fill("..")
        dhl_page.get_by_label("Företag Har du inget företagsnamn - använd ett namn Företag är obligatoriskt om").click()
        dhl_page.get_by_label("Företag Har du inget företagsnamn - använd ett namn Företag är obligatoriskt om").fill(customer_info['name'])
        dhl_page.get_by_label("Land/Territorium Ogiltigt vä").click()
        dhl_page.get_by_label("Land/Territorium Afghanistan").fill("nor")
        dhl_page.get_by_role("option", name="Norway").locator("a").click()
        dhl_page.get_by_label("Adress Obligatorisk").click()
        dhl_page.get_by_label("Adress Obligatorisk").fill(customer_info["address"])
        dhl_page.get_by_label("Ogiltigt").click()
        dhl_page.get_by_label("Ogiltigt").fill(customer_info["zip"])
        dhl_page.get_by_label("Obligatorisk", exact=True).click()
        dhl_page.get_by_label("Obligatorisk", exact=True).fill(customer_info["county"])
        dhl_page.get_by_role("textbox", name="E-postadress", exact=True).click()
        dhl_page.get_by_role("textbox", name="E-postadress", exact=True).fill(customer_info["email"])
        truncatedPhoneNumber = customer_info["phone"][3:]
        dhl_page.get_by_placeholder("__ __ __ _______").click()
        dhl_page.get_by_placeholder("__ __ __ _______").fill(f"{truncatedPhoneNumber}____")
        if return_waybill:
            dhl_page.get_by_role("button", name=" Skifta").click()


    def dhl_label_amount(self, dhl_page, serialNumbers):
        if len(serialNumbers) > 74:
            dhl_page.locator("#shipment-type").get_by_label("Antal").fill("5")
        elif len(serialNumbers) > 56:
            dhl_page.locator("#shipment-type").get_by_label("Antal").fill("4")
        elif len(serialNumbers) > 36:
            dhl_page.locator("#shipment-type").get_by_label("Antal").fill("3")
        elif len(serialNumbers) > 18:
            dhl_page.locator("#shipment-type").get_by_label("Antal").fill("2")
    
    def dhl_label_amount_dangerous_goods(self, dhl_page, customer_info, serialNumbers):
        if len(serialNumbers) >= 3 and "move" in customer_info['model'].lower():
            dhl_page.get_by_text("Farligt gods").click() 
            dhl_page.get_by_text("Lithium Ion PI967 Section II").click()
        if len(serialNumbers) > 74:
            dhl_page.locator("input[name=\"numberOfPackages\"]").click()
            dhl_page.locator("input[name=\"numberOfPackages\"]").fill("5")
        elif len(serialNumbers) > 56:
            dhl_page.locator("input[name=\"numberOfPackages\"]").click()
            dhl_page.locator("input[name=\"numberOfPackages\"]").fill("4")
        elif len(serialNumbers) > 36:
            dhl_page.locator("input[name=\"numberOfPackages\"]").click()
            dhl_page.locator("input[name=\"numberOfPackages\"]").fill("3")
        elif len(serialNumbers) > 18:
            dhl_page.locator("input[name=\"numberOfPackages\"]").click()
            dhl_page.locator("input[name=\"numberOfPackages\"]").fill("2")
        elif len(serialNumbers) > 3:
            dhl_page.locator("input[name=\"numberOfPackages\"]").click()
            dhl_page.locator("input[name=\"numberOfPackages\"]").fill("1")