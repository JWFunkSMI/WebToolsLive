import query
def getBadCodes():
    Dates = [["-01-","A"],["-02-","B"],["-03-","C"],["-04-","D"],["-05-","E"],["-06-","F"],["-07-","G"],["-08-","H"],["-09-","I"],["-10-","J"],["-11-","K"],["-12-","L"]]
    entries = query.Query("SELECT        ID_BADGE, DATE_TRX, ID_SO, HR_LABOR_ACTUAL_UEDT FROM            Stark.dbo.HoursWorked_Preposting WHERE (ID_SO LIKE '%OFFLAB%' OR ID_SO LIKE '%INDLAB_') AND HR_LABOR_ACTUAL_UEDT <> '0.00' GROUP BY ID_BADGE, DATE_TRX, ID_SO, HR_LABOR_ACTUAL_UEDT")
    response = ''
    for e in entries:
        for val in Dates:
            if val[0] in e[1]:
                if val[1] != e[2][len(e[2]) - 1]:
                    response = response + e[0] + ',' + e[1][0:10] + ',' + e[2] + ',' + e[3] + '\n'
    if response == '':
        print('NONE,NONE,,all is calm tonight')
    else:
        print(response)

def payroll(sdate, edate):
    import os
    entries = query.Query("SELECT CONVERT(char(50), LTRIM(code_user)) AS code_user, code, SUM(Hours) AS hours FROM Stark.dbo.HoursWorked_Summed WHERE (Day >= '" + sdate + "') AND (Day <= '" + edate + "') AND Code <> 'E20' GROUP BY code_user, code ORDER BY code_user, code")
    file = open("HR/needsSalaried.txt",'w')
    for line in entries:
        file.write(line[0] + "" + line[1] + "" + line[2] + "\n")
        if 'E1' in line[1] and float(line[2]) > 80:
            print('ALERT ' + line[0] + ' HAS MORE THAN 80 E1')
    file.close()
    import addSalaried
    addSalaried.addSalaried("HR/needsSalaried.txt")
    print('File successfully created')
    os.system('del HR/needsSalaried.txt')

def payPeriod():
    import datetime
    val = '';
    with open('C:\\Users\\funk.admin\\WebTools\\periodStart.txt') as file:
        val = file.readlines()[0].replace('\n','')
    
    start = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    while datetime.datetime.today().date() > (start + datetime.timedelta(13)):
        start = start + datetime.timedelta(14)
    with open('C:\\Users\\funk.admin\\WebTools\\periodStart.txt','w') as file:
        file.write(str(start))

    print(str(start) + " " + str(start + datetime.timedelta(13)))

def getEmployees(badge, empid, fname, lname, dept, pay):
    import datetime
    conditions = []
    if empid != "null":
        conditions.append("EmpID LIKE '%" + empid + "%'")
    if pay != "null":
        conditions.append("PayType LIKE '%" + pay + "%'")
    if fname != "null":
        conditions.append("FirstName LIKE '%" + fname + "%'")
    if lname != "null":
        conditions.append("LastName LIKE '%" + lname + "%'")
    if dept != "null":
        conditions.append("Department LIKE '%" + dept + "%'")
    if badge != "null":
        conditions.append("Badge LIKE '%" + badge + "%'")
    filterQuery = "SELECT Badge, EmpID, FirstName, LastName, Department, PayType, PayrollAlert, AlertCount, SickHours, VacationHours FROM Stark.dbo.Employee_Info"
    conditionsString = ""
    for c in conditions:
        if conditionsString == "":
            conditionsString = " WHERE " + c
        else:
            conditionsString = conditionsString + " AND " + c
    filterQuery = filterQuery + conditionsString + " ORDER BY FirstName, LastName"
    employees = query.Query(filterQuery)
    sdate = str(datetime.date(datetime.date.today().year, 1, 1)) 
    edate = str(datetime.date(datetime.date.today().year, 12, 31))  
    timeOff = query.Query("SELECT  EI.Badge, HW.CODE_PAY_DC AS Code, SUM(HW.HR_PAID) AS Hours FROM Stark.dbo.Employees_Master AS EM LEFT OUTER JOIN Stark.dbo.HoursWorked_Master AS HW ON EM.ID_BADGE = HW.ID_BADGE INNER JOIN Stark.dbo.Date_Info AS DI ON HW.DATE_TRX = DI.Date JOIN Stark.dbo.Employee_Info AS EI ON EM.ID_BADGE=EI.Badge WHERE HW.CODE_PAY_DC<>'E1' AND HW.CODE_PAY_DC<>'E2' AND HW.CODE_PAY_DC<>'E3' AND HW.CODE_PAY_DC<>'E20' AND HW.CODE_PAY_DC<>'EH' AND HW.CODE_PAY_DC<>'EF' AND HW.DATE_TRX>='" + sdate + "' AND HW.DATE_TRX<='" + edate + "' GROUP BY EI.Badge, HW.CODE_PAY_DC")
    timeOffDict = {}
    for entry in timeOff:
        key = (entry[0] + entry[1]).replace(' ','')
        timeOffDict[key] = float(entry[2])
    for e in employees:
        us = 0
        uv = 0
        if e[0] + 'ES' in timeOffDict:
            us = timeOffDict[e[0] + 'ES']
        if e[0] + 'EP' in timeOffDict:
            uv = timeOffDict[e[0] + 'EP']
        print(e[0] + ',' + e[1] + ',' + e[2].replace(' ','') + ',' + e[3].replace(' ','') + ',' + e[4].replace(' ','') + ',' + e[5].replace(' ','') + ',' + e[6][4] + ',' + e[7] + ',' + e[8] + ',' + str(us) + ',' + str(float(e[8]) - us) + ',' + e[9] + ',' + str(uv) + ',' + str(float(e[9]) - uv))

def addEmployee(badge, empid, fname, lname, dept, deptid, pay, reminder, ssick, svac):
    query.Query("INSERT [Stark].[dbo].[Employee_Info] ([Badge],[EmpID],[DeptID],[PayType],[LastName],[FirstName],[Department],PayrollAlert,VacationHours,SickHours,AlertCount) OUTPUT INSERTED.Badge VALUES (" + badge + "," + empid + ",'" + deptid + "','" + pay + "','" + lname + "','" + fname + "','" + dept + "'," + reminder + "," + svac + "," + ssick + ",0)")
    print("Added Successfully")

def removeEmployee(badge):
    query.Query("DELETE FROM Stark.dbo.Employee_Info where Badge=" + badge )
    print("Removed Successfully")

def updateEmployee(badge, empid, fname, lname, dept, deptid, pay, reminder, ssick, svac):
    updates = []
    if empid != 'null':
        updates.append("EmpID=" + empid)
    if pay != 'null':
        updates.append("PayType='" + pay + "'")
    if dept != 'null':
        updates.append("Department='" + dept + "'")
    if deptid != 'null':
        updates.append("DeptID=" + deptid)
    if fname != 'null':
        updates.append("FirstName='" + fname + "'")
    if lname != 'null':
        updates.append("LastName='" + lname + "'")
    if reminder != 'null':
        updates.append("PayrollAlert=" + reminder + ' ')
    if ssick != 'null':
        updates.append("SickHours=" + ssick + " ")
    if svac != 'null':
        updates.append("VacationHours=" + svac + " ")
    attributes = ''
    for u in updates:
        if attributes == '':
            attributes = u
        else:
            attributes = attributes + ',' + u
    #TODO: handle no update
    query.Query("UPDATE [Stark].[dbo].[Employee_Info] SET " + attributes + " WHERE Badge=" + badge)
    print("Updated Successfully")

def getLaborHours(sdate, edate, group, financial):#This can be cut up into methods to make more readable and half as long
    import datetime
    salariedTime = 80.0
    sd = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    ed = datetime.datetime.strptime(edate, "%Y-%m-%d")
    if abs((sd - ed).days) <= 7:
        salariedTime = 40.0
    condition = " AND DeptID=41 "
    if group == "O":
        condition = " AND DeptID<>41 "

    if financial:
        if group == 'S':
            entries = query.Query("SELECT NAME, CODE, SUM(Hours) FROM Stark.dbo.LaborReportFinancial WHERE SSN_encrypt IS NOT NULL AND Date >= '" + sdate + "' AND Date <= '" + edate + "'" + condition + " GROUP BY CODE, NAME")
        else:
            entries = query.Query("SELECT NAME, CODE, SUM(Hours) FROM Stark.dbo.LaborReportFinancial WHERE Date >= '" + sdate + "' AND Date <= '" + edate + "'" + condition + " GROUP BY CODE, NAME")
    else:
        entries = query.Query("SELECT NAME, CODE, SUM(Hours) FROM Stark.dbo.LaborReport WHERE SSN_encrypt IS NOT NULL AND Date >= '" + sdate + "' AND Date <= '" + edate + "'" + condition + " GROUP BY CODE, NAME")
    timeTracker = {}
    for entry in entries:
        if entry[0] not in timeTracker:
            timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
        timeTracker[entry[0]][entry[1].replace(' ','')] = entry[2]
    Totals = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    if financial:
        entries = query.Query("SELECT NAME FROM Stark.dbo.LaborReport WHERE PayType='Salaried'" + condition)
        for entry in entries:
            if entry[0] not in timeTracker:
                timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
            hours = timeTracker[entry[0]]
            hours['E1'] = str(salariedTime - float(hours['EP']) - float(hours['ES']) - float(hours['EF']) - float(hours['EJ']))
            hours['E2'] = '0'
            hours['E3'] = '0'
            hours['SAT'] = '0'
            hours['SUN'] = '0'
        for employee in sorted (timeTracker.keys()):
            time = timeTracker[employee]
            total = 0.0
            for code in time:
                if code != 'E20':
                    total = total + float(time[code])
            total = round(total,2)
            print(employee.replace(' ','') + ' ' + time['E1'] + ' ' + time['E2'] + ' ' + time['E3'] + ' ' + time['EP'] + ' ' + time['ES'] + ' ' + time['EF'] + ' ' + time['EJ'] + ' ' + str(total))
            Totals[0] = Totals[0] + float(time['E1'])
            Totals[1] = Totals[1] + float(time['E2'])
            Totals[3] = Totals[3] + float(time['E3'])
            Totals[5] = Totals[5] + float(time['EP'])
            Totals[6] = Totals[6] + float(time['ES'])
            Totals[7] = Totals[7] + float(time['EF'])
            Totals[9] = Totals[9] + float(time['EJ'])
            Totals[8] = Totals[8] + total
        for i in range(0,len(Totals)):
            Totals[i] = round(Totals[i],2)
        print('Total ' + str(Totals[0]) + ' ' + str(Totals[1]) + ' ' + str(Totals[3]) + ' ' + str(Totals[5]) + ' ' + str(Totals[6]) + ' ' + str(Totals[7]) + ' ' + str(Totals[9]) + ' ' + str(Totals[8]))
    else:
        entries = query.Query("SELECT NAME FROM Stark.dbo.LaborReport WHERE PayType='Salaried'" + condition)
        for entry in entries:
            if entry[0] not in timeTracker:
                timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
            hours = timeTracker[entry[0]]
        for employee in sorted (timeTracker.keys()):
            time = timeTracker[employee]
            if 'E20' in time:
                time['E2'] = str(float(time['E2']) + float(time['E20']))
            total = 0.0
            for code in time:
                if code != 'E20':
                    total = total + float(time[code])
            total = round(total,2)
            print(employee.replace(' ','') + ' ' + time['E1'] + ' ' + time['E2'] + ' ' + time['SAT'] + ' ' + time['SUN'] + ' ' + time['EP'] + ' ' + time['ES'] + ' ' + time['EF'] + ' ' + time['EJ'] + ' ' + str(total))
            Totals[0] = Totals[0] + float(time['E1'])
            Totals[1] = Totals[1] + float(time['E2'])
            Totals[3] = Totals[3] + float(time['SAT'])
            Totals[4] = Totals[4] + float(time['SUN'])
            Totals[5] = Totals[5] + float(time['EP'])
            Totals[6] = Totals[6] + float(time['ES'])
            Totals[7] = Totals[7] + float(time['EF'])
            Totals[9] = Totals[9] + float(time['EJ'])
            Totals[8] = Totals[8] + total
        for i in range(0,len(Totals)):
            Totals[i] = round(Totals[i],2)
        print('Total ' + str(Totals[0]) + ' ' + str(Totals[1]) + ' ' + str(Totals[3]) + ' ' + str(Totals[4]) + ' ' + str(Totals[5]) + ' ' + str(Totals[6]) + ' ' + str(Totals[7]) + ' ' + str(Totals[9]) + ' ' + str(Totals[8]))
    if group == 'S':
        entries = query.Query("SELECT NAME, CODE, SUM(Hours) FROM Stark.dbo.LaborReport WHERE SSN_encrypt IS NULL AND Date >= '" + sdate + "' AND Date <= '" + edate + "'" + condition + " GROUP BY CODE, NAME")
        timeTracker = {}
        for entry in entries:
            if entry[0] not in timeTracker:
                timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
            timeTracker[entry[0]][entry[1].replace(' ','')] = entry[2]
        Totals = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        if financial:
            entries = query.Query("SELECT NAME FROM Stark.dbo.LaborReport WHERE PayType='Salaried'" + condition)
            for entry in entries:
                if entry[0] not in timeTracker:
                    timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
                hours = timeTracker[entry[0]]
                hours['E1'] = str(salariedTime - float(hours['EP']) - float(hours['ES']) - float(hours['EF']) - float(hours['EJ']))
                hours['E2'] = '0'
                hours['E3'] = '0'
                hours['SAT'] = '0'
                hours['SUN'] = '0'
            for employee in sorted (timeTracker.keys()):
                time = timeTracker[employee]
                total = 0.0
                for code in time:
                    if code != 'E20':
                        total = total + float(time[code])
                total = round(total,2)
                print(employee.replace(' ','') + ' ' + time['E1'] + ' ' + time['E2'] + ' ' + time['E3'] + ' ' + time['EP'] + ' ' + time['ES'] + ' ' + time['EF'] + ' ' + time['EJ'] + ' ' + str(total))
                Totals[0] = Totals[0] + float(time['E1'])
                Totals[1] = Totals[1] + float(time['E2'])
                Totals[3] = Totals[3] + float(time['E3'])
                Totals[5] = Totals[5] + float(time['EP'])
                Totals[6] = Totals[6] + float(time['ES'])
                Totals[7] = Totals[7] + float(time['EF'])
                Totals[9] = Totals[9] + float(time['EJ'])
                Totals[8] = Totals[8] + total
            for i in range(0,len(Totals)):
                Totals[i] = round(Totals[i],2)
            print('Total ' + str(Totals[0]) + ' ' + str(Totals[1]) + ' ' + str(Totals[3]) + ' ' + str(Totals[5]) + ' ' + str(Totals[6]) + ' ' + str(Totals[7]) + ' ' + str(Totals[9]) + ' ' + str(Totals[8]))
        else:
            entries = query.Query("SELECT NAME FROM Stark.dbo.LaborReport WHERE PayType='Salaried'" + condition)
            for entry in entries:
                if entry[0] not in timeTracker:
                    timeTracker[entry[0]] = {'E1': '0', 'E2':'0', 'E3': '0', 'EP': '0', 'ES': '0', 'SAT': '0', 'SUN': '0', 'EF': '0', 'EJ': '0'}
                hours = timeTracker[entry[0]]
            for employee in sorted (timeTracker.keys()):
                time = timeTracker[employee]
                if 'E20' in time:
                    time['E2'] = str(float(time['E2']) + float(time['E20']))
                total = 0.0
                for code in time:
                    if code != 'E20':
                        total = total + float(time[code])
                total = round(total,2)
                print(employee.replace(' ','') + ' ' + time['E1'] + ' ' + time['E2'] + ' ' + time['SAT'] + ' ' + time['SUN'] + ' ' + time['EP'] + ' ' + time['ES'] + ' ' + time['EF'] + ' ' + time['EJ'] + ' ' + str(total))
                Totals[0] = Totals[0] + float(time['E1'])
                Totals[1] = Totals[1] + float(time['E2'])
                Totals[3] = Totals[3] + float(time['SAT'])
                Totals[4] = Totals[4] + float(time['SUN'])
                Totals[5] = Totals[5] + float(time['EP'])
                Totals[6] = Totals[6] + float(time['ES'])
                Totals[7] = Totals[7] + float(time['EF'])
                Totals[9] = Totals[9] + float(time['EJ'])
                Totals[8] = Totals[8] + total
            for i in range(0,len(Totals)):
                Totals[i] = round(Totals[i],2)
            print('Total ' + str(Totals[0]) + ' ' + str(Totals[1]) + ' ' + str(Totals[3]) + ' ' + str(Totals[4]) + ' ' + str(Totals[5]) + ' ' + str(Totals[6]) + ' ' + str(Totals[7]) + ' ' + str(Totals[9]) + ' ' + str(Totals[8]))
