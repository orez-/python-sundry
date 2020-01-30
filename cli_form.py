import functools
import re

import curses

missing = object()


def snakecase(word):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Element:
    @classmethod
    def get_by_type(cls, type_):
        return next(
            subcls for subcls in cls.__subclasses__()
            if subcls.method_name() == type_
        )

    @classmethod
    def method_name(cls):
        return snakecase(cls.__name__)

    def on_add(self, form):
        ...

    def click(self):
        ...

    def submit_value(self):
        return missing


class Radio(Element):
    def __init__(self, text, value, name):
        self.text = text
        self.value = value
        self.name = name
        self._checked = False
        self._form = None

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        value = bool(value)
        if value != self._checked:
            if value:
                radio = self._form._active_radios.get(self.name)
                if radio:
                    radio.checked = False
                self._form._active_radios[self.name] = self
            else:
                del self._form._active_radios[self.name]
            self._checked = value
            self._form.mark_dirty(self)

    def render(self, screen):
        symbol = "◉" if self.checked else "○"
        screen.addstr("{} {}\n".format(symbol, self.text))

    def on_add(self, form):
        self._form = form

    def click(self):
        if not self.checked:
            self.checked = True

    def submit_value(self):
        radio = self._form._active_radios.get(self.name)
        if radio is None:
            return None
        return radio.value


class Checkbox(Element):
    def __init__(self, text, name):
        self.text = text
        self.name = name
        self._checked = False
        self._form = None

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        value = bool(value)
        if value != self._checked:
            self._checked = value
            self._form.mark_dirty(self)

    def render(self, screen):
        symbol = "▣" if self.checked else "□"
        screen.addstr("{} {}\n".format(symbol, self.text))

    def on_add(self, form):
        self._form = form

    def click(self):
        self.checked = not self.checked

    def submit_value(self):
        return self.checked


# class Textbox(Element):
#     def __init__(self, name, value=""):
#         self.name = name
#         self.value = value
#         self.width = 20

#     def render(self, screen):
#         screen.addstr("║{:<{}}║\n".format(self.value, self.width))

#     def submit_value(self):
#         return self.value


class NewLine(Element):
    def render(self, screen):
        screen.addstr("\n")

    @classmethod
    def method_name(cls):
        return "br"


class SubmitButton(Element):
    def __init__(self, text="Submit"):
        self.text = text

    def render(self, screen):
        screen.addstr("[ {} ]".format(self.text))

    def on_add(self, form):
        self._form = form

    def click(self):
        self._form.submit()


class Form:
    def __init__(self):
        self._elements = []
        self._dirty = True
        self._submit = None
        self._active_radios = {}

    def __getattr__(self, elem_type):
        try:
            element_cls = Element.get_by_type(elem_type)
        except StopIteration:
            message = "{!r} object has no attribute {!r}".format(type(self).__name__, elem_type)
            raise AttributeError(message) from None
        return lambda *args, **kwargs: self.add(element_cls(*args, **kwargs))

    def mark_dirty(self, element):
        self._dirty = True

    def add(self, element):
        element.on_add(self)
        self._elements.append(element)

    def click(self, mx, my):
        if my < len(self._elements):
            self._elements[my].click()  # no gross

    def render(self, screen):
        self._dirty = False
        screen.clear()
        for elem in self._elements:
            elem.render(screen)

    def submit(self):
        values = {}
        for elem in self._elements:
            value = elem.submit_value()
            if value is not missing:
                name = getattr(elem, 'name', None)
                if name:
                    values[name] = value
        self._submit = values

    def run(self):
        try:
            screen = curses.initscr()
            curses.noecho()
            curses.curs_set(0)
            screen.keypad(1)
            curses.mousemask(1)

            while self._submit is None:
                if self._dirty:
                    self.render(screen)
                event = screen.getch()
                if event == ord("q"): break
                elif event == curses.KEY_MOUSE:
                    _, mx, my, _, btype = curses.getmouse()
                    self.click(mx, my)
                    # y, x = screen.getyx()
                    # screen.addstr(my, mx, 'o')
            return self._submit
        finally:
            curses.endwin()


if __name__ == '__main__':
    form = Form()
    form.radio(name="radio1", value=1, text="Choice 1")
    form.radio(name="radio1", value=2, text="Choice 2")
    form.radio(name="radio1", value=3, text="Choice 3")
    form.br()
    form.checkbox(name="checkbox1", text="Checkbox 1")
    form.checkbox(name="checkbox2", text="Checkbox 2")
    form.checkbox(name="checkbox3", text="Checkbox 3")
    # form.br()
    # form.textbox(name="textbox1")
    form.submit_button()

    value = form.run()
    print(value)
