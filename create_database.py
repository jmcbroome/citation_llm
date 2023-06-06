import sys
from itertools import islice
from txtai.embeddings import Embeddings

def produce_embeddings(file, start_index = 0):
    i = 0
    with open(file) as inf:
        for entry in inf:
            #ignore entries before the start index value
            if i >= start_index:
                text, reference = entry.strip().split("\t")
                yield (i, {"text":text,"reference":reference},None)
            i += 1

embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True, "objects": True, "backend":"faiss", "faiss":{"quantize":True, "mmap":True}})
if len(sys.argv) == 2:
    iterator = produce_embeddings(sys.argv[1])
else:
    iterator = produce_embeddings(sys.argv[1],int(sys.argv[2]))
batchsize = 10
steps = 0
prefix = None
try:
    while True:
        batch = list(islice(iterator, batchsize))
        if not batch:
            break
        embeddings.upsert(batch)
        steps += 1
except KeyboardInterrupt:
    prefix = str(steps*batchsize)
    print(f"Halted on step {prefix}")
except Exception as error:
    prefix = str(steps*batchsize)
    print(f"Failed on step {prefix}")
    print(f"Error: {error}")
if prefix == None:
    print("Completed successfully.")
    embeddings.save("full_citations")
elif steps > 0:
    print("Saving partial dataset.")
    embeddings.save(prefix+"_steps_citations")
