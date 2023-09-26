from utils.data_reader import read_pipelines

for parent, children in read_pipelines():
    print(parent)
