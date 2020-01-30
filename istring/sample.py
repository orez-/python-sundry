names = "names"
expressions = lambda: "expressions"

result = i"Substitute {names} and {expressions()!r} at runtime"
result = i"{expressions()!r}"
print(format(result))
