# a module is a single .py file, while a package is at least two files inside a directory
# library can refer to both a module or package
# packages are better because it is more flexible to add code later
# invoicing is a package

import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


# user can define the directory from where the files are taken - relative paths (variables)
def generate(invoices_path, pdfs_path, image_path,
             product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice excel files into PDF invoices.
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for i in filepaths:
        pdf = FPDF(orientation="p", unit="mm", format="a4")
        pdf.add_page()

        filename = Path(i).stem     # file name
        invoice_nr = filename.split("-")[0]
        invoice_date = filename.split("-")[1]

        pdf.set_font(family="arial", size=14, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)
        pdf.cell(w=50, h=8, txt=f"Date: {invoice_date}", ln=1)
        pdf.cell(w=0, h=4, ln=1)   # breakline

        df = pd.read_excel(i, sheet_name="Sheet 1")
        columns_names = df.columns

        columns_names = [name.title().replace("_", " ") for name in columns_names]

        pdf.set_fill_color(200, 200, 200)
        pdf.set_font(family="arial", size=10, style="B")
        pdf.cell(w=30, h=8, txt=columns_names[0], border=1, fill=1)
        pdf.cell(w=70, h=8, txt=columns_names[1], border=1, fill=1)
        pdf.cell(w=30, h=8, txt="Amount", border=1, fill=1)
        pdf.cell(w=30, h=8, txt=columns_names[3], border=1, fill=1)
        pdf.cell(w=30, h=8, txt=columns_names[4], border=1, fill=1, ln=1)

        # Add items
        for index, row in df.iterrows():
            pdf.set_font(family="arial", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # Add total price row
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=30, h=8, txt="Total price", border="TLB", fill=1)
        pdf.cell(w=70, h=8, border="TB", fill=1)
        pdf.cell(w=30, h=8, border="TB", fill=1)
        pdf.cell(w=30, h=8, border="TB", fill=1)
        total_sum = str(df[total_price].sum())
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, fill=1, ln=1)

        pdf.cell(w=0, h=8, ln=1)   # breakline

        # Add total sum sentence
        pdf.set_font(family="arial", size=12, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}.", ln=1)

        pdf.cell(w=0, h=4, ln=1)   # breakline

        # Add company name and logo
        pdf.cell(w=30, h=8, txt="PythonHow", ln=1)
        pdf.image(image_path, w=10)

        # pdfs_path is supposed to exist, it will create de directory is it doesn't exist
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
