from inventory import UpdateHCM, UpdateHN, ExportHCM, ExportHN

if __name__ == '__main__':
    print('='*100)
    print('')    
    print('INVENTORY MANAGEMENT SYSTEM'.center(100, " "))
    print('')
    print('='*100)
    print('Rider recruitment Operation'.center(100, " "))
    print(('-'*50).center(100, " "))

    ansReturn = 'y'
    while ansReturn.lower() == 'y':
        ans1 = input('''
        MAIN MENU - PLEASE CHOOSE YOU ACTIONS:
            [1]. Update Database.
            [2]. Export reports. 
            [3]. Exit program. ''')
        if ans1 == '1':
            ans3 = 'y'
            while ans3.lower() == 'y':
                ans2 = input('''
                [Update Database] Please choose city to update database:
                [1]. Ha Noi City
                [2]. Ho Chi Minh
                ''')
                if ans2 == '1':
                    UpdateHN.main()
                else:
                    UpdateHCM.main()
                ans3 = input('Do you want to Update more cites? [Y|N] ')

        elif ans1 == '2':
            ans3 = 'y'
            while ans3.lower() == 'y':
                ans2 = input('''
                [Export reports] - Please choose exports type:
                [1]. Ha Noi City - TODAY
                [2]. Ho Chi Minh - TODAY
                [3]. Ha Noi City - CUSTOM DATE
                [4]. Ho Chi Minh - CUSTOM DATE
                [5]. Ha Noi City - CUSTOM WEEK
                [6]. Ho Chi Minh - CUSTOM WEEK
                [7]. Ha Noi City - CUSTOM MONTH
                [8]. Ho Chi Minh - CUSTOM MONTH
                ''')
                            
                if ans2 == '1':
                    ExportHN.total()
                elif ans2 == '2':
                    ExportHCM.total()
                elif ans2 == '3':
                    ExportHN.search_by_date()
                elif ans2 == '4':
                    ExportHCM.search_by_date()
                elif ans2 == '5':
                    ExportHN.search_by_week()
                elif ans2 == '6':
                    ExportHCM.search_by_week()
                else:
                    pass

                ans3 = input('Do you want to export more cites? [Y|N] ')

        else:
            print('End of program...........')
            break
        ansReturn = input('Do you want to return to Main Menu? [Y|N] ')
    