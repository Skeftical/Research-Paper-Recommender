import glob
import re
import os
from io import StringIO



INPUT_FILE_PATH = str(os.environ['INPUT_FILE_PATH'])
print(INPUT_FILE_PATH)
# with open('library.corr', 'w+') as outfile:
for dir_path,subpaths,files in os.walk(INPUT_FILE_PATH):
    if re.search('(Year 1|[0-9]\.)', dir_path):
        # print(dir_path)
        # print(subpaths)
        # print(files)
        files = glob.glob(dir_path+'/*.pdf')
        for name in files:
            print("\"%s\"" % name)
            # a = pdf_to_text(name)
            n = name.split('/')[-1].replace('\n', '')
            n = n.replace(',', '')
            print('txtfiles/%s.txt'%n)
            cmd = "pdftotext \"%s\" \"%s\"" % (name ,'txtfiles/%s.txt'%n)
            os.system(cmd)
