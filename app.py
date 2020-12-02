from b3py.history import read_file
#COTAHIST_D10112020.TXT
sample_file = './b3py/sample/COTAHIST_D10112020.TXT'

values = read_file(sample_file)
for i in values:
    print(i)

