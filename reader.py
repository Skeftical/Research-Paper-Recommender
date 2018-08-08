# pdfFileObj = open('1.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# print(pdfReader.numPages)
# pageObj = pdfReader.getPage(0)
# print(pageObj.extractText())
import glob
import re
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
# from cStringIO import StringIO
from io import StringIO
def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    password = ""
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    try:
        for page in PDFPage.get_pages(fp, password =password):
            interpreter.process_page(page)
            break; # JUST ONE PAGE
    except PDFTextExtractionNotAllowed as e:
        print('Error occured for {0} pdf extraction was not allowed'.format(pdfname))
        pass;
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text


# path = '/home/fotis/Dropbox/PhD/(Year.*|[0-9].*)'
# files = glob.glob(path)
# for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
# 	print(name)
INPUT_FILE_PATH = str(os.environ['INPUT_FILE_PATH'])
print(INPUT_FILE_PATH)
with open('library.corr', 'w+') as outfile:
    for dir_path,subpaths,files in os.walk(INPUT_FILE_PATH):
        # if re.search('(Year 1|[0-9]\.)', dir_path):
        # print(dir_path)
        # print(subpaths)
        # print(files)
        files = glob.glob(dir_path+'/*.pdf')
        for name in files:
            print(name)

            a = pdf_to_text(name)
            n = name.split('/')[-1].replace('\n', '')
            n = n.replace(',', '')
            abstr = a.replace('\n', '\t')
            abstr = re.sub('[!@#$,]', '', abstr)
            name = name.replace(',','')
            #  print(abstr[:2048])
            outfile.write(','.join([name.replace('\n', ''), n, abstr[:2048], '\n']))
outfile.close()
        # for file in files:
        #     if re.search('(Year.*|[0-9].*)', str(file)):
        #         print "file:%s"  %file
