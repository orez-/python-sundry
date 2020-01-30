import itertools

fmt = "[{}] {}> ".format
x = ((yield fmt(i, 1)) + (yield fmt(i, 2)) for i in itertools.count(1))
for first_msg in x:
    print(first_msg, end='')
    print(x.send(int(input())), end='')
    print(x.send(int(input())))
