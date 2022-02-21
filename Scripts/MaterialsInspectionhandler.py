#handler for scripts for the Materials Inspection merger 
print('Content-Type: text/plain')
print()

import sys
if sys.argv[1] == 'D:\\Webtools\\Materials-Inspection\\tools':
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
