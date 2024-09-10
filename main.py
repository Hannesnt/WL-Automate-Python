import re
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
import time
import tkinter as tk
import threading
from tkinter import simpledialog, messagebox, ttk
from Salesforce import ScrapeCaseData
from CC import CC
from DHL import DHLWaybill
from PostNord import PostNordWaybill
def run(playwright: Playwright, serialNumbers, caseNumber, rental, mm_swap, service_and_repair) -> None:

    salesForce = ScrapeCaseData()
    cc = CC()
    dhl = DHLWaybill()
    postnord = PostNordWaybill()
    serial_numbers_str = ', '.join(serialNumbers)
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    default_context = browser.contexts[0]
    pages = default_context.pages


    salesforcePage = "Salesforce"
    ccPage = "CC"
    dhlPage = "DHL"
    unifaunPage = "Unifaun"
    for page in pages:
        if "bambora.lightning.force" in page.url:
            salesforcePage = page
        if "cc.samport" in page.url:
            ccPage = page
        if "mydhl.express" in page.url:
            dhlPage = page
        if "unifaun" in page.url:
            unifaunPage = page
    if salesforcePage == "Salesforce":
        messagebox.showinfo("Information", "Salesforce is not opened")
        return None
    elif ccPage == "CC":
        messagebox.showinfo("Information", "CC is not opened")
        return None
    elif dhlPage == "DHL":
        messagebox.showinfo("Information", "DHL is not opened")
        return None
    elif unifaunPage == "Unifaun":
        messagebox.showinfo("Information", "Unifaun is not opened")
        return None

    customer_info = salesForce.scrape_case_data(salesforcePage, caseNumber, serial_numbers_str, rental, mm_swap, service_and_repair)
    if service_and_repair:
        cc.sr_handle_merchant(serialNumbers, ccPage, customer_info)
    else:
        cc.map_terminal_license(serialNumbers, ccPage, customer_info)

    if customer_info['country'] == "NO" or customer_info['subject'] == "SR":
        dhl.create_dhl_waybill(dhlPage, customer_info, serialNumbers, caseNumber, default_context)
    else:
        postnord.create_postnord_waybill(unifaunPage, serialNumbers, customer_info, caseNumber, default_context)

def show_alert():
    messagebox.showinfo("Information", "Program runned")


def set_rental():
    global rental
    rental = True
    root.destroy()

def set_mm_swap():
    global mm_swap
    mm_swap = True
    root.destroy()

def set_service_and_repair():
    global service_and_repair
    service_and_repair = True
    root.destroy()

def get_terminal_inputs():
    global serialNumbers, caseNumber, root, rental, mm_swap, service_and_repair
    
    root = tk.Tk()
    window_width = 300
    window_height = 200
    root.geometry(f'{window_width}x{window_height}')
    root.title("Choice Selection")
    rental_button = tk.Button(root, text="Rental", command=set_rental)
    rental_button.pack(pady=15)
    mm_swap_button = tk.Button(root, text="MM SWAP", command=set_mm_swap)
    mm_swap_button.pack(pady=15)
    mm_swap_button = tk.Button(root, text="Service & Repair", command=set_service_and_repair)
    mm_swap_button.pack(pady=15)
    root.mainloop() 
    if rental or mm_swap or service_and_repair:
        try:
            amountOfTerminals = simpledialog.askinteger("Input", "Enter the amount of terminals")
            serialNumbers = []
            for i in range(amountOfTerminals):
                serials_list = "\n".join(serialNumbers)
                serialN = simpledialog.askstring("Input", f"Amount of terminals: {amountOfTerminals}\n{serials_list}\nEnter a TERMINAL S/N")
                serialNumbers.append(serialN)
            serials_list = "\n".join(serialNumbers)
            caseNumber = simpledialog.askstring("Input", f"Amount of terminals: {amountOfTerminals}\nS/N: {serials_list}\nEnter the CASE NUMBER")
        except Exception as e:
            messagebox.showinfo("Error", f"Error occurred: {e}")



def run_playwright():
    with sync_playwright() as playwright:
        run(playwright, serialNumbers, caseNumber, rental, mm_swap, service_and_repair)

def main():
    global rental, mm_swap, serialNumbers, caseNumber, service_and_repair
    while True:
        try:
            rental = False  
            mm_swap = False
            service_and_repair = False
            serialNumbers = []
            caseNumber = ""

            # root = tk.Tk()
            # window_width = 300
            # window_height = 200
            # root.geometry(f'{window_width}x{window_height}')
            # root.title("Choice Selection")
            # rental_button = tk.Button(root, text="Rental", command=set_rental)
            # rental_button.pack(pady=15)
            # mm_swap_button = tk.Button(root, text="MM SWAP", command=set_mm_swap)
            # mm_swap_button.pack(pady=15)
            # mm_swap_button = tk.Button(root, text="Service & Repair", command=set_service_and_repair)
            # mm_swap_button.pack(pady=15)
            # root.mainloop()  # Start the GUI event loop

            get_terminal_inputs()
            if serialNumbers and caseNumber:
                run_playwright()

            messagebox.showinfo("Alert", "Process completed. Restarting...")
        except Exception as e:
            messagebox.showinfo("Error", f"Error occurred: {e}")
    

if __name__ == '__main__':
    main()