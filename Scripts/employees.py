#contains all functions for the employee page

import query
import datetime
def getEmployeeTime(auth, ssn, badge, sdate, edate):#input must be validated to prevent sql injection attack
    if auth:
        query.validate(ssn,badge)#authenticate credentials

    #get all time entries for the specified period. Group them by day and separate by code in each day

    entries = query.Query("SELECT  HW.CODE_PAY_DC AS Code, SUM(HW.HR_WORK) AS Hours, DI.Date AS Day FROM Stark.dbo.Employees_Master AS EM LEFT OUTER JOIN Stark.dbo.HoursWorked_Master AS HW ON EM.ID_BADGE = HW.ID_BADGE INNER JOIN Stark.dbo.Date_Info AS DI ON HW.DATE_TRX = DI.Date JOIN Stark.dbo.Employee_Info AS EI ON EM.ID_BADGE=EI.Badge  WHERE EI.Badge='" + badge + "' AND DI.Date>='" + sdate + "' AND DI.Date<= '" + edate + "' GROUP BY EM.CODE_USER, HW.CODE_PAY_DC, DI.Date ORDER BY DI.Date")
    response = ''
    for e in entries:
        response = response + e[0].replace(' ','') + ' ' + e[1] + ' ' + e[2][0:10] + ','
    entries = query.Query("Select DATE_TRX, HR_LABOR_ACTUAL_UEDT FROM TCM99.sms.DCUTRX_NONZERO WHERE DATE_TRX >= '" + sdate + "' AND DATE_TRX <= '" + edate + "' AND ID_BADGE LIKE '%" + badge + "%' AND ID_SO_POST LIKE '%OFFLAB%'")
    for e in entries:
        response = response + 'PP' + ' ' + e[1] + ' ' + e[0][0:10] + ','
    response = response[0:len(response) - 1]
    entries = response.split(',')
    dates = {}
    codes = []
    if entries[0] == '':#return none if no entries for specified period
        print('NONE')
        quit()
    for e in entries:
        vals = e.split(' ')
        if vals[0] == 'E20':
            vals[0] = 'E2'
        if vals[0] not in codes:
            codes.append(vals[0])
        dayDigits = vals[2].split('-')
        day = datetime.date(int(dayDigits[0]),int(dayDigits[1]),int(dayDigits[2]))
        if day in dates:
            if vals[0] in dates[day]:
                dates[day][vals[0]] = dates[day][vals[0]] + float(vals[1])
            else:
                dates[day][vals[0]] = float(vals[1])
        else:
            dates[day] = {}
            dates[day][vals[0]] = float(vals[1])
    #only return headers for codes that have values
    header = 'Date,'
    sortedCodes = []
    if 'ES' in codes:
        header = header + 'Sick,'
        sortedCodes.append('ES')
    if 'EP' in codes:
        header = header + 'Vac,'
        sortedCodes.append('EP')
    if 'E1' in codes:
        header = header + 'Regular,'
        sortedCodes.append('E1')
    if 'E2' in codes:
        header = header + 'OT,'
        sortedCodes.append('E2')
    p = r"\\smi-fs-02\public\QA\Material Inspection Log"
    if 'E3' in codes:
        header = header + 'Double OT,'
        sortedCodes.append('E3')
    if 'EH' in codes:
        header = header + 'Holiday,'
        sortedCodes.append('EH')
    if 'EF' in codes:
        header = header + 'Funeral,'
        sortedCodes.append('EF')
    if 'PP' in codes:
        header = header + 'PrePosted,'
        sortedCodes.append('PP')
    header = header + 'Total'
    print(header)
    nextSunday = 0 #print sums after every saturday
    weekTotals = {}
    totals = {}
    for code in sortedCodes:
        weekTotals[code] = 0.0
        totals[code] = 0.0
    Days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    for k,v in dates.items():
        if nextSunday == 0:#set the intial next Sunday
            nextSunday = k + datetime.timedelta((6 - k.weekday()) % 7) 
        line = str(k) + ' ' + Days[k.weekday()] + ','
        if k >= nextSunday:#check if Sunday has come/past
            nextSunday = nextSunday + datetime.timedelta(7)
            weekTotal = 'Week Total,'
            lineTotal = 0.0
            for code in sortedCodes:
                weekTotal = weekTotal + str(round(weekTotals[code],2)) + ','
                lineTotal = lineTotal + weekTotals[code]
            weekTotal = weekTotal + str(round(lineTotal,2))
            print(weekTotal)
            for code in sortedCodes:#reset the week totals
                weekTotals[code] = 0.0
        lineTotal = 0.0
        for code in sortedCodes:
            if code in v:
                line = line + str(v[code]) + ','
                weekTotals[code] = weekTotals[code] + v[code]
                totals[code] = totals[code] + v[code]
                lineTotal = lineTotal + v[code]
            else:
                line = line + '0,'
        line = line + str(round(lineTotal,2))
        print(line)
    weekTotal = 'Week Total,'
    lineTotal = 0.0
    for code in sortedCodes:
        weekTotal = weekTotal + str(round(weekTotals[code],2)) + ','
        lineTotal = lineTotal + weekTotals[code]
    weekTotal = weekTotal + str(round(lineTotal,2))#print one more week total
    print(weekTotal)
    Total = 'Total,'
    lineTotal = 0.0
    for code in sortedCodes:
        Total = Total + str(round(totals[code],2)) + ','
        lineTotal = lineTotal + totals[code]
    Total = Total + str(round(lineTotal,2))#print the final total
    print(Total)
def getEmployeeOfftime(auth, ssn, badge):
    if auth:
        valid = query.Query("SELECT PWDCOMPARE('" + ssn + "',SSN_encrypt) FROM Stark.dbo.Employee_Info WHERE Badge='" + badge + "'")[0][0]
        if(valid == '0'):
            print("Access Denied")
            quit()
    sdate = str(datetime.date.today().year) + '-01-01'
    edate = str(datetime.date.today().year) + '-12-31'
    entries = query.Query("SELECT  HW.CODE_PAY_DC AS Code, SUM(HW.HR_PAID) AS Hours, DI.Date AS Day FROM Stark.dbo.Employees_Master AS EM LEFT OUTER JOIN Stark.dbo.HoursWorked_Master AS HW ON EM.ID_BADGE = HW.ID_BADGE INNER JOIN Stark.dbo.Date_Info AS DI ON HW.DATE_TRX = DI.Date JOIN Stark.dbo.Employee_Info AS EI ON EM.ID_BADGE=EI.Badge WHERE (HW.CODE_PAY_DC='EP' OR HW.CODE_PAY_DC='ES') AND EI.BADGE='" + badge + "' AND HW.DATE_TRX>='" + sdate + "' AND HW.DATE_TRX<='" + edate + "' GROUP BY DI.Date, HW.CODE_PAY_DC ORDER BY DI.Date")
    startVals = query.Query("SELECT SickHours, VacationHours FROM Stark.dbo.Employee_Info WHERE Badge='" + badge + "'")
    if len(startVals) == 0:
        print('NONE')
        quit()
    startVals = startVals[0]
    print(str(datetime.date(datetime.date.today().year, 1, 1)) + ',0,' + startVals[0] + ',0,' + startVals[1])
    sick = float(startVals[0])
    vac = float(startVals[1])
    usick = 0.0
    uvac = 0.0
    for entry in entries:
        usick = 0
        uvac = 0
        if entry[0].replace(' ','') == 'ES':
            sick = sick - float(entry[1])
            usick = float(entry[1])
        if entry[0].replace(' ','') == 'EP':
            vac = vac - float(entry[1])
            uvac = float(entry[1])
        print(entry[2][0:10] + ',' + str(int(usick)) + ',' + str(int(sick)) + ',' + str(int(uvac)) + ',' + str(int(vac)))
def getHolidays():
    entries = query.Query("Select * FROM Stark.dbo.Holidays")
    response = ''
    for entry in entries:
        response = response + entry[0] + ',' + entry[1] + '\n'
    print(response)
