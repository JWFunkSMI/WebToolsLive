
def removeVendor(toRemove):
    vendors = []
    with open('C:\\Users\\funk.admin\\WebTools\\vendors.txt') as file:
        vendors = file.readlines()
    with open('C:\\Users\\funk.admin\\WebTools\\vendors.txt','w') as file:
        for vendor in vendors:
            if not toRemove == vendor.split(',')[0]:
                file.write(vendor)
    print('removed')
def getVendors():
    import POreport 
    response = ''
    with open('C:\\Users\\funk.admin\\WebTools\\vendors.txt') as file:
        vendors = file.readlines()
        for vendor in vendors:
            vendor = vendor.replace('\n','').split(',')
            response = POreport.getJobStats(vendor[0], vendor[1], vendor[2])
            print(vendor[0] + ',' + vendor[1] + ',' + vendor[2] + ',' + str(response[0]) + ',' + str(response[1]) + ',' + str(response[2]) + ',' + str(response[4]) + ',' + str(response[5]) + ',' + str(round((float(response[4]) / float(response[5])) * 100,2)) + '%')
    

def addVendor(vendor, sdate, edate):
    import POreport 
    response = POreport.getJobStats(vendor, sdate, edate)
    print(str(response[0]) + ',' + str(response[1]) + ',' + str(response[2]) + ',' + str(response[4]) + ',' + str(response[5]) + ',' + str(round((float(response[4]) / float(response[5])) * 100,2)) + '%')
    with open('C:\\Users\\funk.admin\\WebTools\\vendors.txt','a') as file:
        file.write(vendor + ',' + sdate + ',' + edate + '\n')
