from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import LongTable, TableStyle, BaseDocTemplate,Frame, PageTemplate
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak

from data_extrator import DataExtrator
from sms_analyzer import MessagesAnalyzer
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

def call_table():
    query = DataExtrator()
    data_tmp = list(query.get_call_hisotry())
    data = [['Row ID', 'Contact Name', 'Number', 'Date', 'Type', 'Duration\n in seconds']]

    for i in data_tmp:
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

    colwidths = [2*cm, 3*cm, 3*cm, 4*cm, 3*cm, 2.2*cm]

    call_table = LongTable(data2, colWidths=colwidths, repeatRows=1)
    call_table.setStyle(TableStyle(tableStyle))

    return call_table

def sms_table():
    query = DataExtrator()
    data_tmp = list(query.get_sms_list())
    data = [['Message ID', 'Thread ID', 'Receipent', 'Date', 'Body', 'Sent/revceived']]

    for i in data_tmp:
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

    colwidths = [2*cm, 2*cm, 3*cm, 4*cm, 6*cm, 2*cm]

    t = LongTable(data2, colWidths=colwidths, repeatRows=1)
    t.setStyle(TableStyle(tableStyle))

    return t

def all_words_marking_table():
    query = DataExtrator()
    analyzer = MessagesAnalyzer()

    analyzer.calculate_words(query.get_sms_list())

    all_words_list = analyzer.all_words

    print(all_words_list)

    data_tmp = list(all_words_list)
    data = [['Word', 'Times repeated']]

    for i in data_tmp:
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

    colwidths = [2*cm, 2*cm]

    tableWords = LongTable(data2, colWidths=colwidths, repeatRows=1)
    tableWords.setStyle(TableStyle(tableStyle))

    return tableWords

def create_report():
    doc = BaseDocTemplate(
        "report.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    elements = []

    grant_root_permissions()

    styles = getSampleStyleSheet()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    sms_title = Paragraph('Messages history log table.', styles["Heading1"])
    call_title = Paragraph('Call history log table.', styles["Heading1"])
    all_words_marking_title = Paragraph('Words marking through all chats', styles["Heading1"])

    
    elements.append(all_words_marking_title)
    elements.append(all_words_marking_table())

    elements.append(PageBreak())

    elements.append(sms_title)
    elements.append(sms_table())

    elements.append(PageBreak())

    elements.append(call_title)
    elements.append(call_table())

    template = PageTemplate(id='longtable', frames=frame)
    doc.addPageTemplates([template])
    doc.build(elements)


if __name__ == '__main__':
    create_report()