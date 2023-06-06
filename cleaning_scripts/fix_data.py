#https://ordo.open.ac.uk/articles/dataset/Citation-Context_Dataset_C2D_/6865298/1
of = open("fixed_CitationContextbasedDataset.csv",'w+')
with open("CitationContextbasedDataset.csv",'rb') as inf:
    for entry in inf:
        elements = entry.strip().split(b'\t')
        new_elements = []
        if len(elements) == 12:
            elements = elements[1:]
        for i,se in enumerate(elements):
            #try to decode.
            try:
                se_c = se.decode("UTF-8")
            except:
                se_c = "ERROR"
            new_elements.append(se_c)
        print(",".join(new_elements),file=of)
of.close()
