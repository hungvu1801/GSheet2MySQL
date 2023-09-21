from mysql.connector import connect
import pygsheets
import datetime
from inventory.authenticationMYSQL import enter_authentication_mysql
import os.path

def enter_authentication_gsheet():
    # authorization to gsheet
    try:        
        my_path = os.path.abspath(os.path.dirname(__file__))
        path_to_servive_file = os.path.join(
            my_path, 'credentialKeyJson/inventorywithpythonandmysql-1e9415153787.json'
            )
        print(path_to_servive_file)
        gc = pygsheets.authorize(service_file=path_to_servive_file)
        return gc
    except Exception as err:
        print(f'...Error in authenticating GSheet...{err}')
        return

def open_spreadsheet(gc):
    # Open spreadsheet inbound 
    sh_inbound = gc.open('HNOPS_INVENTORY_MANAGEMENT_INBOUND')

    # Open spreadsheet outbound
    sh_outbound = gc.open('HNOPS_INVENTORY_MANAGEMENT_OUTBOUND')

    # Open spreadsheet master
    sh_barcode = gc.open('HNOPS_INVENTORY_MANAGEMENT')
    barcode = sh_barcode.worksheets('title','PRINT_BARCODE')[0]

    # Get data in spreadsheet Inbound scan, sheet("InboundScan")
    ibScan = sh_inbound[1]

    # Get data in spreadsheet Outbound scan, sheet("OutboundScanLog_VM")
    obVMScan = sh_outbound.worksheets('title','OutboundScanLog_VM')[0]

    # Get data in spreadsheet Outbound scan, sheet("OutboundScanLog")
    obScan = sh_outbound.worksheets('title','OutboundScanLog')[0]

    # get all the records of inbound
    records_data_ib = ibScan.get_all_records()

    # get all the records of outbound
    records_data_ob = obScan.get_all_records()

    # get all the records of outboundvm
    records_data_obvm = obVMScan.get_all_records()

    i = len(barcode.get_all_records(head=3))
    records_data_barcode = barcode.get_all_records(head=3)[0:i]

    return records_data_ib, records_data_ob, records_data_barcode, records_data_obvm

def insert_data_barcode(connection, cursor, records_data_barcode):
    # get barcode database
    cursor.execute('select * from barcodehn')
    dbBarcode = cursor.fetchall()
    print('Importing Barcode...')
    # Barcode scan insert into database
    if len(records_data_barcode) > len(dbBarcode):
        records_data_barcode_write = records_data_barcode[len(dbBarcode):]
        val_barcode_to_sql = [
            (
                datetime.datetime.strptime(i['Ngày nhập'], '%m/%d/%Y'),
                i['Loại'],
                i['Loại_Encode'],
                i['Số lượng'],
                i['Encode'],
                i['Barcode'].replace('*', '')
            ) 
            for i in records_data_barcode_write
        ]
        query = 'INSERT INTO barcodehn VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.executemany(query, val_barcode_to_sql)
        connection.commit()
        print('Finished import barcode.')
    else:
        print('Not import new data Barcode.')
    return

def insert_data_inbound(connection, cursor, records_data_ib):
    ''' Get data inbound in GSheet and import into database'''
    print('Importing inbound stocks...')
    # Inbound scan insert into database
    if records_data_ib:
        val_ib_to_sql = [
            (
                i['Scan_Field'], 
                datetime.datetime.strptime(i['Scan_Date'], '%m/%d/%Y %H:%M:%S')
            ) 
            for i in records_data_ib
        ]
        query = 'INSERT INTO inboundscanlog VALUES (%s, %s)'
        cursor.executemany(query, val_ib_to_sql)
        connection.commit()
        print('Finished import inbound stocks.')
    else:
        print('Not import new data Inboundscanlog.')
    return

def insert_data_outbound(connection, cursor, records_data_ob):
    ''' Get data outbound in GSheet and import into database'''
    print('Importing outbound stocks...')
    # Outbound scan insert into database
    if records_data_ob:
        val_ob_to_sql = [
            (
                i['Scan_Field'], 
                datetime.datetime.strptime(i['Scan_Date'], '%m/%d/%Y %H:%M:%S')
            ) 
            for i in records_data_ob
        ]
        query = 'INSERT INTO outboundscanlog(scanfield, scandate) VALUES (%s, %s)'
        cursor.executemany(query, val_ob_to_sql)
        connection.commit()
        print('Finished import outbound stocks.')
    else:
        print('Not import new data Outboundscanlog.')
    return

def insert_data_outboundvm(connection, cursor, records_data_obvm):
    ''' Get data outbound VM in GSheet and import into database'''
    print('Importing outbound stocks Vending Machine...')
    # Outbound scan VM insert into database
    if records_data_obvm:
        val_obvm_to_sql = [
            (
                i['Scan_Field'], 
                datetime.datetime.strptime(i['Scan_Date'], '%m/%d/%Y %H:%M:%S')
            ) 
            for i in records_data_obvm
        ]
        query = 'INSERT INTO outboundscanlogvm(scanfield, scandate) VALUES (%s, %s)'
        cursor.executemany(query, val_obvm_to_sql)
        connection.commit()
        print('Finished import outbound stocks: Vending Machine.')
    else:
        print('Not import new data OutboundscanlogVM.')
    return

def main():
    dbname = 'hnopsinventory'
    db_Info, cursor, connection = enter_authentication_mysql(dbname)
    with cursor, connection:
        print('Connecting to GSheet...')
        gc = enter_authentication_gsheet()
        if not db_Info or not cursor or not gc:
            print('>>> Error critical. Can not connect to database. Please revise code.....<<<')
            return
        try:
            records_data_ib, records_data_ob, \
            records_data_barcode, records_data_obvm = open_spreadsheet(gc)

            insert_data_barcode(connection, cursor, records_data_barcode)
            print('***')
            insert_data_inbound(connection, cursor, records_data_ib)
            print('***')
            insert_data_outbound(connection, cursor, records_data_ob)
            print('***')
            insert_data_outboundvm(connection, cursor, records_data_obvm)
            print('***')
        except Exception as err:
            print(f' Error critical. {err}')
            return

