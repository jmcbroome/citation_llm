import sys
import csv
reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
current_text = ""
references = []
for entry in reader:
    rid, sid, _, _, _, refname, year, authors, pretext, text, posttext = entry
    if refname == "" or rid == "ERROR":
        continue
    text = "".join([pretext, text, posttext])
    if text != current_text:
        #reset
        if len(current_text) > 0:
            print(current_text, ";".join(references), sep='\t')
        current_text = text
        references = []
    authors_clean = ",".join([a for a in authors.split(";") if len(a) > 0])
    reference = ". ".join([authors_clean,refname,year])
    references.append(reference)

