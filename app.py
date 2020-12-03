from b3py.history import read_file, lazy_read
#COTAHIST_D10112020.TXT
sample_file = './b3py/sample/COTAHIST_D10112020.TXT'

# values = read_file(sample_file)
# for i in values:
#     print(i)

# def firstn(n):
#     num = 0
#     while num < n:
#         yield num
#         num += 1

# sum_of_first_n = sum(firstn(6))
# print(sum_of_first_n)

# first_five = firstn(4)

# print(next(first_five))
# print(next(first_five))
# print(next(first_five))
# print(next(first_five))

values = lazy_read(sample_file)
line_count = 0
for i in values:
    line_count = line_count + len(i)

# while True:
#     try:
#         line_count = line_count + (len(next(values)))
#     except StopIteration:
#         print('Cheguei no fim')
#         break

print(f'LAZY lines: {line_count}')

values = read_file(sample_file)
# print(values[:10])
print(f'Full read lines: {len(values)}')