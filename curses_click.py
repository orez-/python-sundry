import curses

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
curses.mousemask(1)

screen.addstr("This is a Sample Curses Script\n\n")

try:
    while True:
        event = screen.getch()
        if event == ord("q"): break
        elif event == curses.KEY_MOUSE:
            _, mx, my, _, btype = curses.getmouse()
            y, x = screen.getyx()
            screen.addstr(my, mx, 'o')
finally:
    curses.endwin()
