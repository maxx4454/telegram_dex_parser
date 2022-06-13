import pandas as pd
import xlsxwriter
import pyodbc


conn = pyodbc.connect('Driver={SQL Server}; Server=ServerIP; uid=UID; pwd=Password; Trusted_Connection=No;')
 with pd.ExcelWriter("Output.xlsx", engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
        try:
            df = pd.read_sql("Select * from Orders", conn)
            df.to_excel(writer, sheet_name = "Sheet1", header = True, index = False)
            print("File saved successfully!")
        except:
            print("There is an error")
