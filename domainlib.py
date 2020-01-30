class Domain:
    def __init__(self, name):
        self._name = name

    def __getattr__(self, key):
        # TODO: validate tlds?
        return Domain(f"{self._name}.{key}")

    def __rmatmul__(self, left):
        # TODO: Validate, return value of type "EmailAddress"
        return f"{left}@{self._name}"


gmail = Domain("gmail")
warbyparker = Domain("warbyparker")

print("brian"@gmail.com)  # 'brian@gmail.com'
print("brian.shaginaw"@warbyparker.com)  # 'brian.shaginaw@warbyparker.com'
