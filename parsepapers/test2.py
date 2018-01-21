import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#write a for-loop to open many files -- leave a comment if you'd #like to learn how
filename = 'enter the name of the file here'
#open allows you to read the file
pdfFileObj = open("1202.0984.pdf",'rb')
#The pdfReader variable is a readable object that will be parsed
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#discerning the number of pages will allow us to parse through all #the pages
num_pages = pdfReader.numPages
count = 0
text = ""
#The while loop will read each page
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

tokens = word_tokenize(text)
for el in tokens:
    print el