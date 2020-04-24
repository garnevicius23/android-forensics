import os, sys

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.platypus import Table

from data_extrator import DataExtrator

width, height = letter

def grant_root_permissions():
    euid = os.geteuid()
    if euid != 0:
        print ("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

    print ('Running. Your euid is', euid)


# Content
fileName = 'report.pdf'
documenttitle = 'Forensics report'
title = 'Android device image forensics results'
subTitle = 'Messages'

textLines = [
    'Sveiki',
    'Labai blogas berniukas',
    'netoks blogas kaip tuu'
]

grant_root_permissions()
query = DataExtrator()
datas = query.get_sms_list()
data = []
for i in range(0,10):
    data.append(datas[i])
    

# data = [
#     ['Dedicated Hosting', 'VPS Hosting', 'Sharing Hosting', 'Reseller Hosting' ],
#     ['€200/Month', '€100/Month', '€20/Month', '€50/Month'],
#     ['Free Domain', 'Free Domain', 'Free Domain', 'Free Domain'],
#     ['2GB DDR2', '20GB Disc Space', 'Unlimited Email', 'Unlimited Email']
# ]

pdf = SimpleDocTemplate(fileName, pagesize=letter)

table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                               3* cm, 3 * cm])

table.wrapOn(pdf, width, height)

elems = []
elems.append(table)

pdf.build(elems)

#pdf.setTitle(documenttitle)
#pdf.drawString(50, 800, title)

#pdf.save()