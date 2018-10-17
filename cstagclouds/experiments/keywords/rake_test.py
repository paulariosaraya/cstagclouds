from extractkeywords.features import rake

stoppath = '/home/paula/Descargas/Memoria/extractkeywords/features/SmartStoplist_original.txt'

rake_object = rake.Rake(stoppath, 5, 3, 4)

sample_file = open("/home/paula/Descargas/Memoria/extractkeywords/txt/Hogan:Aidan/10.1007%2F978-3-319-25010-6_15_2015.pdf.txt", 'r', encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)

# 3. print results
print("Keywords:", keywords)