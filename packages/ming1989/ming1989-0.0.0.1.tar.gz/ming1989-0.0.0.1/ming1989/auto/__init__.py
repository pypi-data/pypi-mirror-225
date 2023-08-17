ls = [
    [3,4,2,6,45],
    [85,8,87,45,4],
    [8,89,90,2,46],
    [34,34,7,34,8]
]

for i in ls:
    print(i)
ls = sorted(ls,key=(lambda x:x[1]),reverse=True)


for i in ls:
    print(i)