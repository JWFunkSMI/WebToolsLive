import query
import datetime
def getOpenJobs():#prevent sql injection attack
    entries = query.Query("SELECT DISTINCT ID_SO FROM TCM99.sms.SHPORD_MATL WHERE QTY_ALLOC > 0 ORDER BY ID_SO")
    for e in entries:
        print(e[0])
def getItems(SO):#prevent sql injection attack
    entries = query.Query("SELECT ID_SO, SUFX_SO, ID_ITEM_COMP, DESCR_ITEM_1, DESCR_ITEM_2, DATE_NEED, QTY_PER, QTY_ISS, QTY_ALLOC, ID_USER_ADD, DATE_ADD, ID_USER_CHG, DATE_CHG FROM TCM99.sms.SHPORD_MATL WHERE QTY_ALLOC > 0 AND LTRIM(RTRIM(ID_SO))='" + SO + "' ORDER BY SUFX_SO, DESCR_ITEM_1")
    for e in entries:
        print(e[0] + ',' + e[1] + ',' + e[2].replace(' ','') + ',' + e[3].replace(',',' ') + ',' + e[4].replace(',',' ') + ',' + e[5].split(' ')[0] + ',' + e[6] + ',' + e[7] + ',' + e[8] + ',' + e[9] + ',' + e[10].split(' ')[0] + ',' + e[11] + ',' + e[12])
def getPOs(item):#prevent sql injection attack
    entries = query.Query("SELECT DISTINCT ID_PO, ID_ITEM, QTY_ORD, DATE_PROM  FROM Stark.dbo.PO_Info WHERE LTRIM(RTRIM(ID_ITEM))='" + item + "'")
    for e in entries:
        print(e[0] + ',' + e[1] + ',' + e[2] + ',' + e[3].split(' ')[0])
