import query
def buildTree():
    managers = {}
    entries = query.Query("SELECT Badge, ReportsTo FROM Stark.dbo.Employee_Info")
    for entry in entries:
        if entry[1] not in managers:
            managers[entry[1]] = [] 
        managers[entry[1]].append(entry[0])
    return managers
def printSubbordinates(badge, chain, managers):
    if len(chain) != 0 and chain[0] == ',':
        chain = chain[1:len(chain)]
    subbordinates = managers[badge]
    for s in subbordinates:
        print(chain + badge + ',' + s)
        if s in managers:
            printSubbordinates(s,chain + badge + ',', managers)
def getSubbordinatesHours(badge, sdate, edate, managers):
    subbordinates = managers[badge]
    for s in subbordinates:
        entries = query.Query("SELECT HW.CODE_PAY_DC AS Code, SUM(HW.HR_WORK) AS Hours FROM Stark.dbo.Employees_Master AS EM LEFT OUTER JOIN Stark.dbo.HoursWorked_Master AS HW ON EM.ID_BADGE=HW.ID_BADGE INNER JOIN Stark.dbo.Date_Info AS DI ON HW.Date_TRX = DI.Date JOIN Stark.dbo.Employee_Info AS EI ON EM.ID_BADGE=EI.Badge WHERE (EI.Badge='" + s + "'AND DI.Date>='" + sdate + "' AND DI.Date<= '" + edate + "') OR (EI.Badge='" + s + "'AND DI.Date>=DATEFROMPARTS(YEAR(GETDATE()), 1, 1) AND DI.Date<=DATEFROMPARTS(YEAR(GETDATE()), 12, 31) AND (HW.CODE_PAY_DC='ES' OR HW.CODE_PAY_DC='EP'))  GROUP BY HW.CODE_PAY_DC")
        usedOff = query.Query("SELECT HW.CODE_PAY_DC AS Code, SUM(HW.HR_WORK) AS Hours FROM Stark.dbo.Employees_Master AS EM LEFT OUTER JOIN Stark.dbo.HoursWorked_Master AS HW ON EM.ID_BADGE=HW.ID_BADGE INNER JOIN Stark.dbo.Date_Info AS DI ON HW.Date_TRX = DI.Date JOIN Stark.dbo.Employee_Info AS EI ON EM.ID_BADGE=EI.Badge WHERE (EI.Badge='" + s + "'AND DI.Date>='" + sdate + "' AND DI.Date<= '" + edate + "' AND (HW.CODE_PAY_DC='EP' OR HW.CODE_PAY_DC='ES'))  GROUP BY HW.CODE_PAY_DC")
        hoursDict = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'UP': '0', 'US': '0'}
        for entry in entries:
            hoursDict[entry[0].replace(' ','')] = entry[1].replace(' ','')
        for entry in usedOff:
            if 'ES' == entry[0].replace(' ',''):
                hoursDict['US'] = entry[1].replace(' ','')
            if 'EP' == entry[0].replace(' ',''):
                hoursDict['UP'] = entry[1].replace(' ','')
        if 'None' in hoursDict:
            hoursDict['E2'] = hoursDict['None']
        empInfo = query.Query("SELECT FirstName, LastName, VacationHours, SickHours FROM Stark.dbo.Employee_Info WHERE Badge='" + s + "'")[0]
        print(s + ',' + empInfo[0].replace(' ','') + ' ' + empInfo[1].replace(' ','') + ',' + hoursDict['E1'] + ',' + hoursDict['E2'] + ',' + hoursDict['E3'] + ',' + hoursDict['UP'] + ',' + hoursDict['EP'] + ',' + str(int(empInfo[2].split('.')[0]) - int(hoursDict['EP'].split('.')[0])) + ',' + hoursDict['US'] + ',' + hoursDict['ES'] + ',' + str(int(empInfo[3].split('.')[0]) - int(hoursDict['ES'].split('.')[0])))
        if s in managers:
            getSubbordinatesHours(s, sdate, edate, managers)

