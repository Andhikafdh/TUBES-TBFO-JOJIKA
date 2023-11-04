import sys

pathFilePda = "pda/" + sys.argv[1]
pathFileHTML = "html/" + sys.argv[2].replace('"', "")

filePda = open(pathFilePda, "r")
isiPda = filePda.read()
filePda.close()


fileHTML = open(pathFileHTML, "r")
isiHTML = fileHTML.read()
fileHTML.close()
