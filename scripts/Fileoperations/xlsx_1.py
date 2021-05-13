import xlsxwriter,xlrd
def write():
    file_name=input("enter file name in .xlsx format")
    workbook = xlsxwriter.Workbook(file_name)
    worksheet=workbook.add_worksheet()
    rows=int(input('enter the number of rows'))
    cols=int(input('enter the number of column'))
    print("enter data rowwise")
    for i in range (0,rows):
        for j in range(0,cols):
            data=input("enter data")
            worksheet.write(i,j,data)
    workbook.close()
  
def read():
    #file_name=input("enter file name in .xlsx format")
    wb = xlrd.open_workbook("abhinav.xls")
    sheet = wb.sheet_by_index(0)
    print(sheet.cell_value(0,0))
    
#write()
read()
