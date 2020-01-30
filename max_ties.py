# max, but returns a list of ties

def max_list(iterable, key=None):
    max_value = None
    elements = []
    for element in iterable:
        value = element if key is None else key(element)
        if value > max_value:
            max_value = value
            elements = [element]
        elif value == max_value:
            elements.append(element)
    return elements


positions = [436, 3653, 3453, 3653, 1214, 324]
print max_list(enumerate(positions), key=lambda x: x[1])
