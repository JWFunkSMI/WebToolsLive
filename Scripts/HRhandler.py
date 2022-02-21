import sys
from dateutil import parser
def isDate(string):
    try:
        parser.parse(string, False)
        return True
    except ValueError:
        return False
print('Content-Type: text/plain')
print()
if sys.argv[1] == 'D:\\Webtools\\HR\\getBadCodes':
    import humanResources
    humanResources.getBadCodes()
if sys.argv[1] == 'D:\\Webtools\\HR\\payroll':
    import humanResources
    humanResources.payroll(sys.argv[2], sys.argv[3])
if sys.argv[1] == 'D:\\Webtools\\HR\\index':
    import humanResources
    humanResources.getEmployees(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
if sys.argv[1] == 'D:\\Webtools\\HR\\addEmployee':
    import humanResources
    humanResources.addEmployee(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
if sys.argv[1] == 'D:\\Webtools\\HR\\removeEmployee':
    import humanResources
    humanResources.removeEmployee(sys.argv[2])
if sys.argv[1] == 'D:\\Webtools\\HR\\updateEmployee':
    import humanResources
    humanResources.updateEmployee(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
if sys.argv[1] == 'D:\\Webtools\\HR\\payPeriod':
    import humanResources
    humanResources.payPeriod()
if sys.argv[1] == 'D:\\Webtools\\HR\\getHolidays':
    import employees 
    employees.getHolidays()
if sys.argv[1] == 'D:\\Webtools\\HR\\getEmployeeTime':
    import employees 
    if sys.argv[2].isdigit()  and isDate(sys.argv[3]) and isDate(sys.argv[4]):
        employees.getEmployeeTime(False, 0, sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print('Invalid Input')
if sys.argv[1] == 'D:\\Webtools\\HR\\getEmployeeOfftime':
    import employees 
    if sys.argv[2].isdigit():
        employees.getEmployeeOfftime(False, 0, sys.argv[2])
    else:
        print('Invalid Input')
if sys.argv[1] == 'D:\\Webtools\\HR\\getLaborHours':
    import humanResources
    financial = False
    if sys.argv[5] == 'F':
        financial = True
    humanResources.getLaborHours(sys.argv[2],sys.argv[3],sys.argv[4],financial)
