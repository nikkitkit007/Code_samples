import curses
import os
import time
from curses.textpad import rectangle
from curses import wrapper
from logo_curses import show_logo


def update_view_win(view_win, dir_to_view):
    view_win.clear()

    view_list = os.listdir(dir_to_view)
    for i in range(len(view_list)):
        view_win.addstr(i, 0, view_list[i])

    view_win.refresh()


def sort_dir_files(unsorted_dir):
    files_list = []
    dir_list = []
    for el in unsorted_dir:
        if el.count('.') == 1:
            files_list.append(el)
        else:
            dir_list.append(el)

    files_list.sort()
    dir_list.sort()

    for i in range(len(files_list)):
        files_list[i] = {'type': 'file', 'is_current': False, 'data': files_list[i]}

    for i in range(len(dir_list)):
        if i == 0:
            dir_list[i] = {'type': 'dir', 'is_current': True, 'data': dir_list[i]}
        else:
            dir_list[i] = {'type': 'dir', 'is_current': False, 'data': dir_list[i]}

    return dir_list + files_list


def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # инициализация цветов
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    YELLOW = curses.color_pair(1)
    GREEN = curses.color_pair(2)
    CYAN = curses.color_pair(3)

    curses.curs_set(0)

    cur_position = 0

    dir_files = sort_dir_files(os.listdir())  # парсинг файлов и папок в текущей дирректории

    navi_win = curses.newwin(20, 32, 2, 1)  # создание окон
    view_win = curses.newwin(20, 40, 2, 36)

    show_logo(stdscr, CYAN)
    time.sleep(1.7)

    stdscr.clear()

    stdscr.addstr(0, 1, "Code Samples", curses.A_BOLD)
    rectangle(stdscr, 1, 0, 1 + 20 + 1, 1 + 32 + 1)  # отрисовка границ вокруг окон
    rectangle(stdscr, 1, 35, 1 + 20 + 1, 1 + 74 + 1)
    rectangle(stdscr, 23, 0, 26, 76)  # отрисовка нижнего бара
    stdscr.addstr(24, 1, "Use arrows to navigate", CYAN | curses.A_BOLD)
    stdscr.addstr(25, 1, "Press q to exit the program", CYAN | curses.A_BOLD)

    stdscr.refresh()

    while True:

        navi_win.clear()

        for i in range(len(dir_files)):
            if dir_files[i]['is_current']:
                navi_win.addstr(i, 0, "> " + dir_files[i]['data'], GREEN | curses.A_BOLD)
                if dir_files[i]['type'] == 'dir':
                    update_view_win(view_win, dir_files[i]['data'])
                else:
                    view_win.clear()
                    view_win.refresh()
            elif dir_files[i]['type'] == 'dir':
                navi_win.addstr(i, 0, dir_files[i]['data'], YELLOW)
            else:
                navi_win.addstr(i, 0, dir_files[i]['data'])

        navi_win.refresh()

        key = stdscr.getkey()
        if key == "KEY_UP":  # обработка нажатий клавиш
            if cur_position > 0:
                dir_files[cur_position]['is_current'] = False
                cur_position -= 1
                dir_files[cur_position]['is_current'] = True
            else:
                curses.beep()
                curses.flash()

        elif key == "KEY_DOWN":
            if cur_position < len(dir_files)-1:
                dir_files[cur_position]['is_current'] = False
                cur_position += 1
                dir_files[cur_position]['is_current'] = True
            else:
                curses.beep()
                curses.flash()

        elif key == "q" or key == "Q":
            break


if __name__ == "__main__":
    wrapper(main)

    # todo улучшить функциональность обозревателя папок
