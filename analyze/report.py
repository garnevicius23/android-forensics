from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import LongTable, TableStyle, BaseDocTemplate,Frame, PageTemplate
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak

import glob
from PyPDF2 import PdfFileMerger

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

    #print(all_words_list)

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

    colwidths = [3*cm, 1.85*cm]

    tableWords = LongTable(data2, colWidths=colwidths, repeatRows=1)
    tableWords.setStyle(TableStyle(tableStyle))

    return tableWords

def words_marking_by_chat():
    query = DataExtrator()
    analyzer = MessagesAnalyzer()

    analyzer.calculate_words(query.get_sms_list())

    styles = getSampleStyleSheet()

    words_by_threads = analyzer.words_by_thread

    elements = []

    words_by_threads_title = Paragraph('Words marking grouped by receipent', styles["Heading1"])
    elements.append(words_by_threads_title)

    for thread in words_by_threads.keys():
        chat_title = Paragraph('Conversation with - ' + thread, styles["Heading3"])
        elements.append(chat_title)
        #print(words_by_threads[thread])

        data_tmp = words_by_threads[thread]
        data_tmp = sorted(data_tmp.items(), key=lambda x: x[1], reverse=True)
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

        styleN = styles['Normal']

        styleN.wordWrap = 'CJK'

        data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]

        colwidths = [3*cm, 1.85*cm]

        tableWordsByThread = LongTable(data2, colWidths=colwidths, repeatRows=1)
        tableWordsByThread.setStyle(TableStyle(tableStyle))

        elements.append(tableWordsByThread)

    return elements

def create_report_with_more_columns():
    doc = BaseDocTemplate(
        "report1.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    grant_root_permissions()

    styles = getSampleStyleSheet()

    all_words_marking_title = Paragraph('Words marking through all chats', styles["Heading1"])

    elements = words_marking_by_chat()
    elements.append(PageBreak())

    elements.append(all_words_marking_title)
    elements.append(all_words_marking_table())

    frameWidth = doc.width/2
    frameHeight = doc.height-.05*cm
    frames = []
    for frame in range(2):
        leftMargin = doc.leftMargin + frame*frameWidth
        column = Frame(leftMargin, doc.bottomMargin, frameWidth, frameHeight)
        frames.append(column)
    template = PageTemplate(id='threecolumns', frames=frames)

    doc.addPageTemplates([template])
    doc.build(elements)

def create_report():
    doc = BaseDocTemplate(
        "report2.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    #elements = []

    grant_root_permissions()

    styles = getSampleStyleSheet()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    sms_title = Paragraph('Messages history log table.', styles["Heading1"])
    call_title = Paragraph('Call history log table.', styles["Heading1"])

    elements = []

    elements.append(sms_title)
    elements.append(sms_table())

    elements.append(PageBreak())

    elements.append(call_title)
    elements.append(call_table())
    
    template = PageTemplate(id='longtable', frames=frame)
    doc.addPageTemplates([template])
    doc.build(elements)

def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []

    for path in input_paths:
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


if __name__ == '__main__':
    create_report()
    create_report_with_more_columns()

    os.remove('report.pdf')
    paths = glob.glob('report*.pdf')
    paths.sort()
    merger('report.pdf', paths)