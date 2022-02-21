#functions that read and write dataa

import os

#looks for pdf files in the merging folder for Materials Inspection
def detectMergingFiles():    
    pdfs = []
    path = r"\\smi-fs-02\public\qa\Material Inspection Log\Merging folder\merge"
    files = os.listdir(path)
    for f in files:
        if '.pdf' in f :
            print(f) 

#returns what the resulting files will be when merged
def getMergingTargets():
    import xlrd
    p = r"\\smi-fs-02\public\QA\Material Inspection Log"

    #grab info from cells in SMI-LOG-010
    workbook = xlrd.open_workbook("\\\\smi-fs-02\\public\\QA\\Material Inspection Log\\Merging Folder\\SMI-LOG-010 Material Inspection Log (Rev 4.1).xlsx")
    worksheet = workbook.sheet_by_index(3)
    jobs = str(worksheet.cell_value(1,14)).split(' - ')
    part = worksheet.cell_value(1,4)
    po = worksheet.cell_value(2,4)
    heat1 = worksheet.cell_value(2,14)
    if '.' in str(heat1):
        heat1 = round(heat1)
    heat2 = worksheet.cell_value(3,14)
    if '.' in str(heat2):
        heat2 = round(heat2)
    heat3 = worksheet.cell_value(4,14)
    if '.' in str(heat3):
        heat3 = round(heat3)

    heat = str(heat1)
    if heat != '' and str(heat2) != '':
        heat = heat + ' - ' + str(heat2)
        if str(heat3) != '':
            heat = heat + ' - ' + str(heat3)
    pdfs = []
    path = r"\\smi-fs-02\public\qa\Material Inspection Log\Merging folder\merge"
    files = os.listdir(path)
    name = ''
    for f in files:
        if '.pdf' in f and 'SMI-LOG-010' not in f:
            pdfs.append('merge\\' + f)
    for job in jobs:
        if '.' in str(job):
            name = str(part) + ' - ' + str(po) + ' - ' + str(round(float(job)))
        else:
            name = str(part) + ' - ' + str(po) + ' - ' + str(job)
        if str(heat) != '':
            name = name + ' - ' + heat
        name = name + '.pdf'
        print('Jobs\\' + str(job).split('.')[0] + '\\' + name)

#performs the merge and creates the necessary folders if needed
def merge(pdfs, names):
    from PyPDF2 import PdfFileMerger
    p = r"\\smi-fs-02\public\QA\Material Inspection Log"
    merger = PdfFileMerger(strict=False)
    merger.append(p + '\\Merging Folder\\merge\\SMI-LOG-010 Material Inspection Log (Rev 4.1).pdf')

    for pdf in pdfs:
        if 'SMI-LOG-010' not in pdf:
            merger.append(p + '\\Merging Folder\\merge\\' + pdf)
    for name in names:
        split = name.split('\\')
        if not(os.path.isdir(p + '\\Jobs\\' + split[1])):
            os.system('mkdir "' + p + '\\Jobs\\' + split[1] + '"')
        merger.write(p + '\\' + name)
        print('File created: ' + p + '\\' + name)
    merger.close()
    for pdf in pdfs:
        os.system('del "' + p + '\\Merging Folder\\merge\\' + pdf + '"')
