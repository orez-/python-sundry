import ast
import string

import astunparse


class InterpolationTemplate:
    __slots__ = ("raw_template", "parsed_template", "field_values", "format_specifiers")

    def __new__(cls, raw_template, parsed_template, field_values, format_specifiers):
        self = super().__new__(cls)
        self.raw_template = raw_template
        self.parsed_template = parsed_template
        self.field_values = field_values
        self.format_specifiers = format_specifiers
        return self

    def __repr__(self):
        return (f"<{type(self).__qualname__} {repr(self.raw_template)} at {id(self):#x}>")

    def __format__(self, format_specifier):
        # When formatted, render to a string, and use string formatting
        return format(self.render(), format_specifier)

    def render(self, *, render_template=''.join, render_field=format):
        iter_fields = enumerate(self.parsed_template)
        values = self.field_values
        specifiers = self.format_specifiers
        template_parts = []
        for field_pos, (leading_text, field_expr) in iter_fields:
            template_parts.append(leading_text)
            if field_expr is not None:
                value = values[field_pos]
                specifier = specifiers[field_pos]
                rendered_field = render_field(value, specifier)
                template_parts.append(rendered_field)
        return render_template(template_parts)


class IStringFormatter(string.Formatter):
    def vformat(self, format_string, args, kwargs):
        parsed_template = []
        format_specifiers = []
        for i, (literal_text, field_name, format_spec, conversion) in enumerate(self.parse(format_string)):
            parsed_template.append((literal_text, field_name))
            if format_spec is not None:
                format_specifiers.append(format_spec)
            if conversion:
                args[i] = self.convert_field(args[i], conversion)

        return InterpolationTemplate(
            raw_template=format_string,
            parsed_template=parsed_template,
            field_values=args,
            format_specifiers=format_specifiers,
        )


def check(filename):
    with open(filename, "r") as file:
        contents = file.read()
    parsable_contents = contents.replace("i'", "f'").replace('i"', 'f"')
    result = ast.parse(parsable_contents)
    IStringVisitor().visit(result)
    # print(astunparse.unparse(result))


class IStringVisitor(ast.NodeVisitor):
    def visit_JoinedStr(self, node):
        print(dir(node))
        if hasattr(self, 'istring_fields'):
            raise SyntaxError("Can't nest i-strings.")
        self.istring_fields = []
        super().generic_visit(node)
        node.istring_fields = self.istring_fields
        print("!?", self.istring_fields)
        del self.istring_fields

    def visit_FormattedValue(self, node):
        if hasattr(self, 'istring_fields'):
            self.istring_fields.append(astunparse.unparse(node.value).rstrip('\n'))
        super().generic_visit(node)


# ---

check("sample.py")

# names = "names"
# expressions = lambda: "expressions"

# isf = IStringFormatter().format("Substitute {names} and {expressions()!r} at runtime", names, expressions())
# print(isf)
# print(format(isf))
