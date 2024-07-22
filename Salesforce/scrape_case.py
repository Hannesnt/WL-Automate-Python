from bs4 import BeautifulSoup
import time
import re
from datetime import date, timedelta
class ScrapeCaseData:
    def scrape_case_data(self, salesforcePage, caseNumber, serial_numbers_str, rental, mm_swap):
        self.get_case(salesforcePage, caseNumber, rental, mm_swap)

        web_component = None
        soup = None
        customer_info = {}
        
        if rental: 
            web_component = salesforcePage.locator('emailui-rich-text-output').get_attribute('value')
            if web_component:
                soup = BeautifulSoup(web_component, 'html.parser')
                spans = soup.find_all('span')
                self.rental_scrape(spans, customer_info)
            else:
                print("emailui-rich-text-output value was not found or is empty.")  
        
        elif mm_swap:
            
            web_component = salesforcePage.locator('div.forceChatterMessageSegments').nth(0).inner_html()
            if web_component:
                soup = BeautifulSoup(web_component, 'html.parser')
                paragraphs = soup.find_all('p')
                customer_info['subject'] = "MMSW"
                for i, p in enumerate(paragraphs):
                    self.mm_swap_scrape("Customer Account Number:", paragraphs, p, i, customer_info, 'accountNumber')
                    self.mm_swap_scrape('Customer:', paragraphs, p, i, customer_info, 'name')
                    self.mm_swap_scrape('Telephone Number:', paragraphs, p, i, customer_info, 'phone')
                    self.mm_swap_scrape('Email for Order Confirmation & Tracking:', paragraphs, p, i, customer_info, 'email')
                    self.mm_swap_scrape('Terminals', paragraphs, p, i, customer_info, 'model')
                    self.mm_swap_scrape('Terminal language:', paragraphs, p, i, customer_info, 'country') #break if complete 
                self.mm_follow_up(salesforcePage, customer_info)
            else:
                print("MM Swap data was not found or is empty.")                

        time.sleep(1)
        salesforcePage.get_by_title("Send Email").click()
        time.sleep(1)
        salesforcePage.locator("label").filter(has_text="To").click()
        time.sleep(1)
        salesforcePage.locator("label").filter(has_text="To").fill(customer_info["email"])
        salesforcePage.get_by_title("Post", exact=True).click()
        time.sleep(1)
        salesforcePage.get_by_label("Share an update...").click()

        if customer_info["country"] == "NO":
            if customer_info["subject"] == "ST": 
                salesforcePage.get_by_label("Share an update...").fill(f"S/N: {serial_numbers_str} \n\nDHL WAYBILL: \nDHL RETURN WAYBILL:")
            else: 
                salesforcePage.get_by_label("Share an update...").fill(f"S/N: {serial_numbers_str} \n\nDHL WAYBILL: ")
        else:
            if customer_info["subject"] == "ST":
                salesforcePage.get_by_label("Share an update...").fill(f"S/N: {serial_numbers_str} \n\nPOSTNORD WAYBILL: \nPOSTNORD RETURN WAYBILL:")
            else:
                salesforcePage.get_by_label("Share an update...").fill(f"S/N: {serial_numbers_str} \n\nPOSTNORD WAYBILL: ")
        return customer_info

    def get_case(self, salesforcePage, caseNumber, rental, mm_swap):
        salesforcePage.get_by_role("link", name="Cases").click()
        time.sleep(2)
        if rental:
            salesforcePage.get_by_role("button", name="Select a List View: Cases").click()
            salesforcePage.get_by_role("option", name="Logistics - Rental Orders").click()
            time.sleep(2)
        elif mm_swap:
            salesforcePage.get_by_role("button", name="Select a List View: Cases").click()
            try:
                salesforcePage.get_by_role("option", name="Selected Logistics - MM Swap").click()
            except:
                try:
                    salesforcePage.get_by_role("option", name="Logistics - MM Swap").click()
                except:
                    print("Couldnt find correct option 'MM-SWAP'")
            time.sleep(2)
        salesforcePage.get_by_role("link", name=caseNumber).click()

    def rental_scrape(self, spans, customer_info):
        terminal_span = None
        customer_span = None
        lang_span = None
        subject_span = None
        for span in spans:
            if self.match_span(span, "Package:"):
                subject_span = span
                subject_rows = subject_span.get_text(separator='\n', strip=True).split('\n')
                if "BAMBORA_ONE_SHORT_TERM" in subject_rows[1] or "BAMBORA_DEVICE_SHORT_TERM" in subject_rows[1]:
                    customer_info['subject'] = "ST" 
                elif "ONE" in subject_rows[1]:
                    customer_info['subject'] = "ONE"
                elif "DEVICE" in subject_rows[1]:
                    customer_info['subject'] = "DEVICE"
                else:
                    customer_info['subject'] = "NULL"

            if self.match_span(span, "Terminal language:"):
                lang_span = span
                lang_rows = lang_span.get_text(separator='\n', strip=True).split('\n')
                customer_info['country'] = lang_rows[1][-2:]
            if self.match_span(span, "License-numbers:"):
                terminal_span = span
                terminal_rows = terminal_span.get_text(separator='\n', strip=True).split('\n')
                model_row = terminal_rows[1].split(' ')
                customer_info['model'] = model_row[1]
                license_row = terminal_rows[3].split(' ')
                license_row.pop(0)
                if(len(license_row) > 0):
                    for i in range(len(license_row)):
                        license_row[i] = license_row[i].replace(',', '')
                customer_info['licenseNumber'] = license_row
            if self.match_span(span, "Customer Account Number:"):
                customer_span = span
                customer_rows = customer_span.get_text(separator='\n', strip=True).split('\n')
                customer_info['accountNumber'] = customer_rows[1]
                customer_info['name'] = customer_rows[7]
                customer_info['address'] = customer_rows[8]
                if len(customer_rows[9].split(' ')) > 2:
                    customer_info['zip'] = customer_rows[9].split(' ')[0] + customer_rows[9].split(' ')[1]
                else:
                    customer_info['zip'] = customer_rows[9].split(' ')[0]
                customer_info['county'] = customer_rows[9].split(' ')[1]
                customer_info['phone'] = customer_rows[14]
                customer_info['email'] = customer_rows[16]

            if customer_span and terminal_span and lang_span != None:
                break

    def mm_swap_scrape(self, subject, paragraphs, p, i, customer_info, customer_info_key):
        if "Deliver Address:" in p.get_text():
            next_paragraph_text = paragraphs[i + 1].get_text()
            pattern = re.compile(r'(.+?)\s(\d{4}|\d{3}\s?\d{2})\s(.+)')
            match = pattern.match(next_paragraph_text)
            if match:
                result = [match.group(1), match.group(2), match.group(3)]
                customer_info['address'] = result[0].replace(",", "")
                customer_info['zip'] = result[1].replace(",", "")
                customer_info['county'] = result[2].replace(",", "")
            else:
                customer_info['address'] = "None"
                customer_info['zip'] = "None"
                customer_info['county'] = "None"

        elif subject in p.get_text():
            if p.get_text() == "Terminals":
                model = paragraphs[i + 2].get_text()
                terminal_model_list = model.split(" ")
                customer_info[customer_info_key] = terminal_model_list[1]
                model = paragraphs[i + 3].get_text()
                terminal_model_list = model.split(" ")
            elif i + 1 < len(paragraphs):
                next_paragraph_text = paragraphs[i + 1].get_text()
                customer_info[customer_info_key] = next_paragraph_text
                
    def match_span(self, span, text):
        if text in span.get_text():
            return True
        return False
    def mm_follow_up(self, salesforcePage, customer_info):
        time.sleep(1)
        salesforcePage.get_by_title("Follow Up Date").click()
        time.sleep(1)
        salesforcePage.get_by_label("Follow Up Date").click()
        followup_date = date.today() + timedelta(days=30)
        salesforcePage.get_by_label("Follow Up Date").fill(f"{followup_date}")
        time.sleep(1)
        salesforcePage.locator("button").filter(has_text="Save").nth(3)
        time.sleep(1)
        salesforcePage.get_by_role("button", name="Edit Case Owner").click()
        time.sleep(1)
        salesforcePage.get_by_label("*Case Owner").click()
        salesforcePage.locator("lightning-base-combobox").filter(has_text="QueueClear").get_by_role("button").click()
        salesforcePage.get_by_label("*Case Owner").fill("contact center ")
        time.sleep(1)
        if customer_info['country'] == "DK":
            salesforcePage.get_by_role('option', name='Contact Center Denmark')
        elif customer_info['country'] == "SE":
            salesforcePage.get_by_role('option', name='Contact Center Sweden')
        elif customer_info['country'] == "FI":
            salesforcePage.get_by_role('option', name='Contact Center Finland')
        elif customer_info['country'] == "NO":
            salesforcePage.get_by_role('option', name='Contact Center Norway')
        time.sleep(1)
        salesforcePage.get_by_role("button", name="Save")