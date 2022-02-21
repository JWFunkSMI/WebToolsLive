import sys
import pymssql as sql

def addSalaried(f):
    connection = sql.connect('smi-sql-01','sa','P@ssw0rd')
    cursor = connection.cursor()

    lines = []
    with open(f) as file:
        lines = file.readlines()
        file.close()

    query = "SELECT [EmpID] FROM [Stark].[dbo].[Employee_Info] WHERE PayType='Salary' OR PayType='Salaried'"

    cursor.execute(query)

    response = cursor.fetchall()
    salaried = []
    for item in response:
        badge = str(item).replace("(Decimal('",'').replace("'),)",'')
        if len(badge) == 3:
            badge = '0' + badge
        salaried.append(badge)

    file = open("\\\\smi-fs-02\\HR\\HR\\Paychex\\testreport2.txt", "w")
    nonRegularHours = []
    for line in lines:
        badge = line.split(' ')[0]
        
        if badge in salaried:
            if 'E1' not in line and 'E2' not in line:
                nonRegularHours.append([i for i in line.replace('\n','').split(' ') if i != ''])
                file.write(line)
        else:
            file.write(line)

    file.write('\n')
    for employee in salaried:
        hours = 80
        for vals in nonRegularHours:
            if employee == vals[0]:
                hours = hours - int(vals[2].split('.')[0])
        if hours > 0:
            file.write(employee + '                                              E1          ' + str(hours) + '.00\n') 

    file.close()

    file = open("\\\\smi-fs-02\\HR\\HR\\Paychex\\testreport2.txt")
    lines = file.readlines()
    file.close()
    file = open("\\\\smi-fs-02\\HR\\HR\\Paychex\\testreport2.txt", "w")
    lines.sort()
    for line in lines:
        if line != '\n':
            file.write(line)
    file.close()
