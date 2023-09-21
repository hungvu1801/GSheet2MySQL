# from inventory.authenticationMYSQL import enter_authentication_mysql
from inventory.authenticationMYSQL import enter_authentication_mysql
import pandas as pd
import os.path
from time import sleep
from datetime import date
def total():
    try:
        today = date.today().strftime('%Y-%m-%d')
        dbname = 'hnopsinventory'
        _, cursor, connection = enter_authentication_mysql(dbname)
        my_path = os.path.abspath(os.path.dirname(__file__))
        # Get script total directory
        directory_query_total = os.path.join(
            my_path, "Scripts/queryScript_TotalHN.txt"
            )
        # Get script detail directory
        directory_query_detail = os.path.join(
            my_path, "Scripts/queryScript_DetailHN.txt"
            )
        # Get export directory for total csv file
        directory_export_total =  os.path.join(
            os.path.dirname(my_path), 
            f'Export_Files/[InventoryHN]_{today}_total.csv')
        # Get export directory for detail csv file    
        directory_export_detail =  os.path.join(
            os.path.dirname(my_path), 
            f'Export_Files/[InventoryHN]_{today}_detail.csv')
        # Read total query
        with open(directory_query_total) as f:
            query_total = f.read()
        # Read detail query
        with open(directory_query_detail) as f:
            query_detail = f.read()
 
        with cursor, connection:
            # Get total
            print('Exporting data to csv....')
            cursor.execute(query_total)
            db_total = cursor.fetchall()
            # Header of export file
            header_total = ['barcodeIn', 'Barcode_Out', 'Category', 
                            'Quantity', 'SoLuongBanRa', 'SoLuongXuatVM',
                            'SoLuongTon', 'InboundScan_Date', 'OutboundScan_Latest_Time', 
                            'OutboundScan_VM_Latest_Time']
            df_total = pd.DataFrame(db_total)
            df_total.columns = header_total
            df_total.to_csv(directory_export_total)
            sleep(2)
            ## Get detail based on date
            header_detail = ['Category', 'InboundBefore', 'OutboundBefore', 
                             'OutboundVMBefore', 'Ton dau ky', 'Nhap trong ky', 
                             'Xuat trong ky', 'Xuat VM trong ky', 'Ton cuoi ky'] 
            cursor.execute("SET @datesearch = current_date();")           
            cursor.execute(query_detail)
            db_detail = cursor.fetchall()            
            df_detail = pd.DataFrame(db_detail)

            df_detail.columns = header_detail
            df_detail.to_csv(directory_export_detail)
            print('Completed.')
    except Exception as err:
        print(err)
        return

def search_by_date():
    try:
        today = date.today().strftime('%Y-%m-%d')
        date_search = input('Please enter date by format [yyyy-mm-dd]: ')
        dbname = 'hnopsinventory'
        _, cursor, connection = enter_authentication_mysql(dbname)
        my_path = os.path.abspath(os.path.dirname(__file__))
        # Get script detail directory
        directory_query_detail = os.path.join(
            my_path, "Scripts/queryScript_DetailHN.txt"
            )
        # Get export directory for total csv file
        directory_export_search = os.path.join(
            os.path.dirname(my_path), 
            f'Export_Files/[InventoryHN]_{today}_DetailSearchIn_{date_search}.csv')
    
        # Read total query
        with open(directory_query_detail) as f:
            query_search = f.read()

        with cursor, connection:
            query1 = f"SET @datesearch = date('{date_search}');"
            cursor.execute(query1)
            cursor.execute(query_search)
            
            ## Get dentail based on date
            header_detail = ['Category', 'InboundBefore', 'OutboundBefore', 
                            'OutboundVMBefore', 'Ton dau ky', 'Nhap trong ky', 
                            'Xuat trong ky', 'Xuat VM trong ky', 'Ton cuoi ky']

            db_detail = cursor.fetchall()            
            df_detail = pd.DataFrame(db_detail)

            df_detail.columns = header_detail
            df_detail.to_csv(directory_export_search)

        print('Completed.')
    except Exception as err:
        print(err)
        return
    return

def search_by_week():
    try:
        today = date.today().strftime('%Y-%m-%d')
        input_search = input('Please enter week and year by format [ww, yyyy]: ')
        week_search, year_search = input_search.split(',')
        week_search = str(int(week_search.strip()) - 1)
        year_search = year_search.strip()
        dbname = 'hnopsinventory'
        _, cursor, connection = enter_authentication_mysql(dbname)
        my_path = os.path.abspath(os.path.dirname(__file__))
        # Get script detail directory
        directory_query_detail = os.path.join(
            my_path, "Scripts/queryScript_DetailHN_searchbyWeek.txt"
            )
        # Get export directory for total csv file
        directory_export_search = os.path.join(
            os.path.dirname(my_path), 
            f'Export_Files/[InventoryHN]_{today}_DetailSearchIn_{year_search}-{week_search}.csv')

        # Read total query
        with open(directory_query_detail) as f:
            query_search = f.read()

        with cursor, connection:

            cursor.execute(f"SET @yearsearch = '{year_search}';")
            cursor.execute(f"SET @weeksearch = '{week_search}';")
            cursor.execute(query_search)

            ## Get detail based on date
            header_detail = ['Category', 'InboundBefore', 'OutboundBefore', 
                            'OutboundVMBefore', 'Ton dau ky', 'Nhap trong ky', 
                            'Xuat trong ky', 'Xuat VM trong ky', 'Ton cuoi ky']

            db_detail = cursor.fetchall()            
            df_detail = pd.DataFrame(db_detail)

            df_detail.columns = header_detail
            df_detail.to_csv(directory_export_search)

        print('Completed.')
    except Exception as err:
        print(err)
        return
    return