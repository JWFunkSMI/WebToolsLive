import pymssql as sql
def Query(s):

    connection = sql.connect('smi-sql-01','sa','P@ssw0rd')
    cursor = connection.cursor()

    cursor.execute(s)
    result = []
    if "UPDATE" not in s and "DELETE" not in s:
        list = cursor.fetchall()
        for item in list:
            s = ''
            s = []
            for i in item:
                s.append(str(i).replace('Decimal','').replace('(','').replace(')','').replace("'",''))
            result.append(s)
		
    connection.commit()
    return result
def validate(ssn, badge):
    valid = Query("SELECT PWDCOMPARE('" + ssn + "',SSN_encrypt) FROM Stark.dbo.Employee_Info WHERE Badge='" + badge + "'")[0][0]
    if(valid == '0'):
        print("Access Denied")
        quit()
