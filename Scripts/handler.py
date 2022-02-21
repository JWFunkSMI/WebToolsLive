#handler for scripts that do not require any special permissions

import sys
from dateutil import parser

#function to check whether or not a string is a date
def isDate(string):
    try:
        parser.parse(string, False)
        return True
    except ValueError:
        return False

#headers
print('Content-Type: text/plain')
print()
#end of headers

#requests are separated based on sub script files

#input validation should be mostly handled in the handler files
if sys.argv[1] == 'D:\\Webtools\\Employees':
    import employees#TODO: specify imports another level
    if sys.argv[2] == 'getEmployeeTime':
        if sys.argv[3].isdigit() and sys.argv[4].isdigit() and isDate(sys.argv[5]) and isDate(sys.argv[6]):
            employees.getEmployeeTime(True, sys.argv[3], sys.argv[4],sys.argv[5],sys.argv[6])
        else:
            print('Invalid Input')
    if sys.argv[2] == 'getEmployeeOfftime':
        if sys.argv[3].isdigit() and sys.argv[4].isdigit():
            employees.getEmployeeOfftime(True, sys.argv[3], sys.argv[4])
        else:
            print('Invalid Input')
    if sys.argv[2] == 'getHolidays':
        employees.getHolidays()

if sys.argv[1] == 'D:\\Webtools\\VendorReport':
    import vendorReport 
    if sys.argv[2] == 'removeVendor':
        vendorReport.removeVendor(sys.argv[3])
    if sys.argv[2] == 'addVendor':
        vendorReport.addVendor(sys.argv[3], sys.argv[4], sys.argv[5])
    if sys.argv[2] == 'getVendors':
        vendorReport.getVendors()

if sys.argv[1] == 'D:\\Webtools\\payPeriod':
    import humanResources
    humanResources.payPeriod()

if sys.argv[1] == 'D:\\Webtools\\reports':
    import reports
    if sys.argv[2] == 'getOpenJobs':
        reports.getOpenJobs()
    if sys.argv[2] == 'getItems':
        reports.getItems(sys.argv[3])
    if sys.argv[2] == 'getPOs':
        reports.getPOs(sys.argv[3])

if sys.argv[1] == 'D:\\Webtools\\tools':
    import tools
    if sys.argv[2] == 'detectMergingFiles':
        tools.detectMergingFiles()
    if sys.argv[2] == 'getMergingTargets':
        tools.getMergingTargets()
    if sys.argv[2] == 'merge':
        names = []
        pdfs = []
        i = 4
        string = sys.argv[3] 
        while i < len(sys.argv) - 1:
            string = string + ' ' + sys.argv[i]
            i = i + 1
        split = string.split(' . ')
        pdfs = split[0].split(" ' ")
        names = split[1].split(" ' ")
        tools.merge(pdfs, names)

if sys.argv[1] == 'D:\\Webtools\\managers':
    import query
    query.validate(sys.argv[3],sys.argv[4])
    if sys.argv[4] == '4715':
        sys.argv[4] = '4990'
    import managers 
    if sys.argv[2] == 'getManagerTree':
        managerDict = managers.buildTree()
        if sys.argv[4] in managerDict:
            managers.printSubbordinates(sys.argv[4],'',managerDict)
        else:
            print('Not a manager')
    if sys.argv[2] == 'getSubbordinatesHours':
        managerDict = managers.buildTree()
        managers.getSubbordinatesHours(sys.argv[4], sys.argv[5], sys.argv[6], managerDict)
