import tabula
import os
file = "C:\\Users\\User\\Desktop\\python\\Task2-ReadPDF2\\file.pdf"

tables = tabula.read_pdf(file, pages="all")

folder_name = "Task2-ReadPDF2"


for i, table in enumerate(tables, start=1):
    table.to_json(os.path.join(folder_name, f"table_{i}.json"), index=True)
