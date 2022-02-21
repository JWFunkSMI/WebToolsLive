import pymssql as sql
import sys
import datetime

def Query(s):

    connection = sql.connect('smi-sql-01')
    cursor = connection.cursor()

    cursor.execute(s)
    result = []
    if "UPDATE" not in s:
        list = cursor.fetchall()
        for item in list:
            s = ''
            for i in item:
                s = s + str(i) + ','
            s = s.replace('Decimal','')
            s = s.replace('(','')
            s = s.replace(')','')
            s = s.replace("'",'')
            s = s[0:len(s) - 1]
            result.append(s)
		
    connection.commit()
    return result
def getJobStats(vendor, sdate, edate):
    import query
    file = open("C:\\Users\\funk.admin\\WebTools\\bad.txt","a")
    file.write('Naughty List\n')
    file.close()

    q = "SELECT NAME_VND FROM TCM99.sms.VENMAS_PAYTO WHERE ID_VND='" + vendor + "'"
    name = query.Query(q)[0][0]
    q = "SELECT HDR.ID_PO, CHG.DATE_PROM, CHG.ID_LINE_PO FROM TCM99.sms.PORHDR_HDR AS HDR JOIN TCM99.sms.PORLIN_ITEM AS LINE ON HDR.ID_PO=LINE.ID_PO JOIN TCM99.sms.POHIST_LINE_CHG AS CHG ON HDR.ID_PO=CHG.ID_PO AND LINE.ID_LINE_PO=CHG.ID_LINE_PO WHERE HDR.ID_VND_ORDFM='" + vendor + "' AND DATE_RCV>='" + sdate + "' AND DATE_RCV<='" + edate + "' AND NOT CHG.DATE_PROM IS NULL GROUP BY CHG.DATE_PROM, HDR.ID_PO, CHG.ID_LINE_PO, CHG.DATE_ADD ORDER BY ID_PO, ID_LINE_PO, CHG.DATE_ADD"
    entries = query.Query(q)
    d = {}
    for e in entries:
        key = e[0] + e[2]
        if key in d:
            d[key].append(e[1])
        else:
            d[key] = [e[1]]
    changes = 0
    pchanges = 0
    nchanges = 0
    for k in d:
        if len(d[k]) > 1:
            date = datetime.datetime.strptime(d[k][0], '%Y-%m-%d %H:%M:%S')
            for x in range(len(d[k]) - 1):
                nextDate = datetime.datetime.strptime(d[k][x + 1], '%Y-%m-%d %H:%M:%S')
                changes = changes + 1
                if date < nextDate:
                    nchanges = nchanges + 1
                else:
                    pchanges = pchanges + 1
    q = "SELECT COUNT(*) FROM TCM99.sms.PORHDR_HDR AS HDR JOIN TCM99.sms.PORLIN_ITEM AS LINE ON HDR.ID_PO=LINE.ID_PO WHERE DATE_RCV>='" + sdate + "' AND DATE_RCV<='" + edate + "' AND DATE_RQST < DATE_RCV AND ID_VND_ORDFM='" + vendor + "'"
    reqDatesMissed = query.Query(q)[0][0]
    q = "SELECT COUNT(*) FROM TCM99.sms.PORHDR_HDR AS HDR JOIN TCM99.sms.PORLIN_ITEM AS LINE ON HDR.ID_PO=LINE.ID_PO WHERE DATE_RCV>='" + sdate + "' AND DATE_RCV<='" + edate + "' AND DATE_PROM < DATE_RCV AND ID_VND_ORDFM='" + vendor +"'"
    promDatesMissed = query.Query(q)[0][0]
    q = "SELECT COUNT(*) FROM TCM99.sms.PORHDR_HDR AS HDR JOIN TCM99.sms.PORLIN_ITEM AS LINE ON HDR.ID_PO=LINE.ID_PO WHERE DATE_RCV>='" + sdate + "' AND DATE_RCV<='" + edate + "' AND ID_VND_ORDFM='" + vendor + "'"
    totalDates = query.Query(q)[0][0]
    return [changes, nchanges, pchanges, int(reqDatesMissed), int(promDatesMissed), int(totalDates)]
