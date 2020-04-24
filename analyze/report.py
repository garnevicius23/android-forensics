from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import LongTable, TableStyle, BaseDocTemplate,Frame, PageTemplate
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle

from data_extrator import DataExtrator
import os, sys
import numpy as np


def grant_root_permissions():
    euid = os.geteuid()
    if euid != 0:
        print ("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

    print ('Running. Your euid is', euid)

def test():
    doc = BaseDocTemplate(
        "question.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    elements = []

    grant_root_permissions()
    query = DataExtrator()
    datas = list(query.get_sms_list())
    data = [['Message ID', 'Thread ID', 'Receipent', 'Date', 'Body', 'Sent/revceived']]

    for i in datas:
        tmp = []
        for j in i:
            tmp.append(str(j))
        data.append(tmp)

    tableStyle = [
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (5, 0), colors.lightgreen)
        ]


    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    styleN.wordWrap = 'CJK'

    data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    colwidths = [2*cm, 2*cm, 3*cm, 4*cm, 6*cm, 2*cm]

    t = LongTable(data2, colWidths=colwidths, repeatRows=1)
    t.setStyle(TableStyle(tableStyle))
    elements.append(t)

    template = PageTemplate(id='longtable', frames=frame)
    doc.addPageTemplates([template])
    doc.build(elements)


if __name__ == '__main__':
    test()