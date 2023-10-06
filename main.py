from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from queue import PriorityQueue
from collections import deque
import random
import time
import customtkinter
from customtkinter import *
from heapq import *
import os
import webbrowser

# initialize main window
root = customtkinter.CTk()
# root = cTk()
root.geometry("760x650")
root.title('Pathfinding Algorithm Visualizer By Raghav Dube')
root.maxsize(760, 650)
root.resizable(FALSE,FALSE)
# .config(bg='black')
customtkinter.set_appearance_mode("System")

font = ("Helvetica", 11)
color_white="#e7ecef"
# Variables
selected_alg = StringVar()
selected_bld = StringVar()
WIDTH = 500
ROWS = 25
grid = []

# frame layout - for user interface

UI_frame = customtkinter.CTkFrame(root, width=600, height=200)
UI_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")


# create canvas
canvas = Canvas(root, width=WIDTH, height=WIDTH, bg='white')
canvas.grid(row=0, column=1, padx=10, pady=5)

img_logo = PhotoImage(file='logo.png')
root.iconphoto(False, img_logo)

# define class - spot
class Spot:
    start_point = None
    end_point = None

    __slots__ = ['button', 'row', 'col', 'width', 'neighbors', 'g', 'h', 'f',
                 'parent', 'start', 'end', 'barrier', 'clicked', 'total_rows']

    def __init__(self, row, col, width, offset, total_rows):

        self.button = Button(canvas,
                             command=lambda a=row, b=col: self.click(a, b),
                             bg='#eae2b7', bd=2, relief=GROOVE
                             )

        self.row = row
        self.col = col
        self.width = width

        self.button.place(x=row * width + offset, y=col * width + offset,
                          width=width, height=width)

        self.neighbors = []
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.start = False
        self.end = False
        self.barrier = False
        self.clicked = False
        self.total_rows = total_rows

    def make_start(self):
        self.button.config(bg="DarkOrange2")
        self.start = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)

    def make_end(self):
        self.button.config(bg="lime green")
        self.end = True
        self.clicked = True
        Spot.end_point = (self.col, self.row)

    def make_barrier(self):
        self.button.config(bg="black")
        self.barrier = True
        self.clicked = True

    def reset(self):
        self.button.config(bg="#eae2b7")
        self.clicked = False

    def make_path(self):
        self.button.config(bg="gold")

    def make_to_visit(self):
        self.button.config(bg="pink")

    def make_backtracking(self):
        self.button.config(bg="SteelBlue1")

    def make_open(self):
        self.button.config(bg="cornflower blue")

    def make_closed(self):
        self.button.config(bg="LightSkyBlue2")

    def disable(self):
        self.button.config(state=DISABLED)

    def enable(self):
        self.button.config(state=NORMAL)

    def circle(self):
        return (self.row * WIDTH + 1, self.col * WIDTH + 1, WIDTH - 2, WIDTH - 2)

    def click(self, row, col):
        if self.clicked == False:
            if not Spot.start_point:
                self.make_start()
            elif not Spot.end_point:
                self.make_end()
            else:
                self.make_barrier()
        else:
            self.reset()
            if self.start == True:
                self.start = False
                Spot.start_point = None
            elif self.end == True:
                self.end = False
                Spot.end_point = None
            else:
                self.barrier = False

    def update_neighbors(self, grid):
        self.neighbors = []

        # check neighbors a row down - if spot not outside grid and not barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors.append(grid[self.row + 1][self.col])  # add spot to the neighbors

        # check neighbors a row up - if spot not outside grid and not barrier
        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors.append(grid[self.row - 1][self.col])  # add spot to the neighbors

        # check neighbors a col right - if spot not outside grid and not barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors.append(grid[self.row][self.col + 1])  # add spot to the neighbors

        # check neighbors a col left - if spot not outside grid and not barrier
        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors.append(grid[self.row][self.col - 1])  # add spot to the neighbors


def make_grid(width, rows):
    gap = width // rows
    offset = 2
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, offset, rows)
            grid[i].append(spot)
    return grid


# define heuristic function - Manhatten distance
def h(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def reconstruct_path(spot, tickTime):
    current = spot
    while current.start == False:
        parent = current.parent

        parent.make_path()
        root.update_idletasks()
        time.sleep(tickTime)

        current = parent


def Reset():
    global grid

    Spot.start_point = None
    Spot.end_point = None

    for row in grid:
        for spot in row:
            spot.reset()
            spot.neighbors = []
            spot.g = float('inf')
            spot.h = 0
            spot.f = float('inf')
            spot.parent = None
            spot.start = False
            spot.end = False
            spot.barrier = False
            spot.enable()


def break_wall(current, new):
    if current.row == new.row:
        if current.col > new.col:
            # wall to the left from current
            wall = grid[current.row][current.col - 1]
        else:
            # wall to the right
            wall = grid[current.row][current.col + 1]
    else:
        if current.row > new.row:
            # wall above
            wall = grid[current.row - 1][current.col]
        else:
            # wall below
            wall = grid[current.row + 1][current.col]
    # break wall
    wall.reset()
    wall.barrier = False


# A-star algorithm
def a_star(grid, tickTime):
    count = 0
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    # create open_set
    open_set = PriorityQueue()

    # add start in open_set with f_score = 0 and count as one item
    open_set.put((0, count, start))

    # put g_score for start to 0
    start.g = 0

    # calculate f_score for start using heuristic function
    start.f = h(start, end)

    # create a dict to keep track of spots in open_set, can't check PriorityQueue
    open_set_hash = {start}

    # if open_set is empty - all possible spots are considered, path doesn't exist
    while not open_set.empty():

        # popping the spot with lowest f_score from open_set
        # if score the same, then whatever was inserted first - PriorityQueue
        # popping [2] - spot itself
        current = open_set.get()[2]
        # syncronise with dict
        open_set_hash.remove(current)

        # found end?
        if current == end:
            reconstruct_path(end, tickTime)

            # draw end and start again
            end.make_end()
            start.make_start()

            # enable UI frame
            for child in UI_frame.winfo_children():
                child.configure(state='normal')
            return True

        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:

            # calculate g_score for every neighbor
            temp_g_score = current.g + 1

            # if new path through this neighbor better
            if temp_g_score < neighbor.g:

                # update g_score for this spot and keep track of new best path
                neighbor.parent = current
                neighbor.g = temp_g_score
                neighbor.f = temp_g_score + h(neighbor, end)

                if neighbor not in open_set_hash:
                    # count the step
                    count += 1

                    # add neighbor in open_set for consideration
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # draw updated grid with new open_set
        root.update_idletasks()
        time.sleep(tickTime)

        if current != start:
            current.make_closed()

    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False


# Breadth-First algorithm
def breadth_first(grid, tickTime):
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    open_set = deque()

    open_set.append(start)
    visited_hash = {start}

    while len(open_set) >= 0:
        current = open_set.popleft()

        # found end?
        if current == end:
            reconstruct_path(end, tickTime)

            # draw end and start again
            end.make_end()
            start.make_start()
            return

        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:

            if neighbor not in visited_hash:
                neighbor.parent = current
                visited_hash.add(neighbor)
                open_set.append(neighbor)
                neighbor.make_open()

        # draw updated grid with new open_set
        root.update_idletasks()
        time.sleep(tickTime)

        if current != start:
            current.make_closed()

    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False


def depth_first(grid, tickTime):
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    open_set = []

    open_set.append(start)
    visited_hash = {start}

    while len(open_set) >= 0:
        current = open_set.pop()

        # found end?
        if current == end:
            reconstruct_path(end, tickTime)

            # draw end and start again
            end.make_end()
            start.make_start()
            return

        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:

            if neighbor not in visited_hash:
                neighbor.parent = current
                visited_hash.add(neighbor)
                open_set.append(neighbor)
                neighbor.make_open()

        # draw updated grid with new open_set
        root.update_idletasks()
        time.sleep(tickTime)

        if current != start:
            current.make_closed()

    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False


def dijkstra(grid, tickTime):
    count = 0
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    # create open_set
    open_set = PriorityQueue()

    # add start in open_set with f_score = 0 and count as one item
    open_set.put((0, count, start))

    # put g_score for start to 0
    start.g = 0

    # calculate f_score for start using heuristic function
    # start.f = count +1

    # create a dict to keep track of spots in open_set, can't check PriorityQueue
    open_set_hash = {start}

    # if open_set is empty - all possible spots are considered, path doesn't exist
    while not open_set.empty():

        # popping the spot with lowest f_score from open_set
        # if score the same, then whatever was inserted first - PriorityQueue
        # popping [2] - spot itself
        current = open_set.get()[2]
        # syncronise with dict
        open_set_hash.remove(current)

        # found end?
        if current == end:
            reconstruct_path(end, tickTime)

            # draw end and start again
            end.make_end()
            start.make_start()

            # enable UI frame
            for child in UI_frame.winfo_children():
                child.configure(state='normal')
            return True

        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:

            # calculate g_score for every neighbor
            temp_g_score = current.g + 1

            # if new path through this neighbor better
            if temp_g_score <= neighbor.g:

                # update g_score for this spot and keep track of new best path
                neighbor.parent = current
                neighbor.g = temp_g_score
                # neighbor.f = temp_g_score + h(neighbor, end)

                if neighbor not in open_set_hash:
                    # count the step
                    count += 1

                    # add neighbor in open_set for consideration
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # draw updated grid with new open_set
        root.update_idletasks()
        time.sleep(tickTime)

        if current != start:
            current.make_closed()

    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False


# start pathfinding
def StartAlgorithm():
    global grid
    if not grid: return
    if not Spot.start_point or not Spot.end_point:
        messagebox.showinfo("No start/end", "Place starting and ending points")
        return

    # update neighbors based on current maze
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.g = float('inf')
            spot.h = 0
            spot.f = float('inf')
            spot.parent = None
            spot.update_neighbors(grid)
            if spot.clicked == False:
                spot.reset()
            spot.disable()  # disable buttons in the grid for running algorithm

    # disable UI frame for running algorithm
    for child in UI_frame.winfo_children():
        child.configure(state='disable')

    # choose algorithm
    if algMenu.get() == 'A-star Algorithm':
        a_star(grid, speedScale.get())
    elif algMenu.get() == 'BFS Algorithm':
        breadth_first(grid, speedScale.get())
    elif algMenu.get() == 'DFS Algorithm':
        depth_first(grid, speedScale.get())
    elif algMenu.get() == "Dijkstra's Algorithm":
        dijkstra(grid, speedScale.get())

        # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()

    for child in UI_frame.winfo_children():
        child.configure(state='normal')  # enable frame


# Put random walls in the grid
def random_walls(grid):
    # if start and end spots are not indicated - put start and end randomly
    if not Spot.start_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.end == False:
            current.make_start()

    if not Spot.end_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.start == False:
            current.make_end()

    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    # put walls randomly
    for row in grid:
        for spot in row:
            if spot != start and spot != end:
                spot.reset()
                spot.barrier = False
                spot.clicked = False
                if random.randint(0, 100) < wallsScale.get():
                    spot.make_barrier()

    # draw updated grid
    root.update_idletasks()


def circ_maze(grid, rows):
    # Reset all
    Reset()

    # breake into rings
    rings = []
    for n in range(rows // 2 + 1):
        set1 = set()
        set2 = set()
        for row in grid:
            for spot in row:
                if spot.row in range(n, rows - n) and spot.col in range(n, rows - n):
                    set1.add(spot)
                if spot.row in range(n + 1, rows - n - 1) and spot.col in range(n + 1, rows - n - 1):
                    set2.add(spot)
        ring = list(set1 - set2)
        if len(ring) > 0:
            rings.append(ring)

    # put start in the outer ring and end in the inner ring and remove them from rings
    random.choice(rings[0]).make_start()
    for spot in rings[0]:
        if spot.start == True:
            rings[0].remove(spot)

    random.choice(rings[-1]).make_end()
    for spot in rings[-1]:
        if spot.end == True:
            rings[-1].remove(spot)

    # make odd rings into walls
    for ring in rings[1::2]:

        # remove connor spots from rings
        if len(ring) > 0:
            min_row = min([spot.row for spot in ring])
            max_row = max([spot.row for spot in ring])
            tmp = []
            for spot in ring:
                if (spot.row, spot.col) in [(min_row, min_row), (min_row, max_row),
                                            (max_row, min_row), (max_row, max_row)]:
                    tmp.append(spot)
            for item in tmp:
                ring.remove(item)

        for spot in ring:
            spot.make_barrier()

        if len(ring) == 0:
            rings.remove(ring)

    # make oppenings in ring walls
    for ring in rings[1::2]:
        for item in random.sample(ring, 2):
            item.reset()
            item.barrier = False

    # update neighbors based on current maze
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.update_neighbors(grid)

    # add single walls between ring walls
    for ring in rings[2::2]:
        # make random spots into a wall
        tmp = []
        for spot in ring:
            if len(spot.neighbors) < 3:
                tmp.append(spot)
        if len(tmp) > 0:
            single_wall = random.choice(tmp)
            single_wall.make_barrier()

            # draw updated grid
    root.update_idletasks()


def carve_out(grid, rows, tickTime):
    # Reset all
    Reset()

    to_visit = []
    for row in grid[::2]:
        for spot in row[::2]:
            to_visit.append(spot)

    for row in grid:
        for spot in row:
            if spot in to_visit:
                spot.make_to_visit()
            else:
                spot.make_barrier()

    to_visit[0].make_start()
    to_visit[-1].make_end()
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]

    # draw updated grid with new open_set
    root.update_idletasks()
    time.sleep(tickTime)

    visited = []
    open_set = []
    current = start
    open_set.append(current)
    visited.append(current)

    while len(open_set) > 0:
        moves = []

        # right neighbor
        if current.col + 2 < rows:
            neighbor = grid[current.row][current.col + 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        # left neighbor
        if current.col - 2 >= 0:
            neighbor = grid[current.row][current.col - 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        # down neighbor
        if current.row + 2 < rows:
            neighbor = grid[current.row + 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        # up neighbor
        if current.row - 2 >= 0:
            neighbor = grid[current.row - 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        if len(moves) > 0:
            new = random.choice(moves)
            break_wall(current, new)
            if new != end:
                new.reset()
            current = new
            visited.append(current)
            open_set.append(current)
        else:
            current = open_set.pop()
            if current != start and current != end:
                current.make_backtracking()
                # draw updated grid with new open_set
                root.update_idletasks()
                time.sleep(tickTime)
                current.reset()

        # draw updated grid with new open_set
        root.update_idletasks()
        time.sleep(tickTime)

    # draw updated grid with new open_set
    root.update_idletasks()
    time.sleep(tickTime)


# start pathfinding
def build_maze():
    global grid
    if not grid: return

    for row in grid:
        for spot in row:
            spot.disable()  # disable buttons in the grid for running algorithm

    # disable UI frame for running algorithm
    for child in UI_frame.winfo_children():
        child.configure(state='disable')

    # choose algorithm
    if bldMenu.get() == 'Random walls':
        random_walls(grid)
    elif bldMenu.get() == 'Circular maze':
        circ_maze(grid, ROWS)
    elif bldMenu.get() == 'Carved out maze':
        carve_out(grid, ROWS, speedScale.get())


    # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()

    for child in UI_frame.winfo_children():
        child.configure(state='normal')  # enable frame


def scale_action(event):
    if bldMenu.get() == 'Random walls':
        wallsScale.configure(state='normal')
    else:
        wallsScale.configure(state='disable')

def ins_menu_get(val:str):
    if val=="Instructions":
        instructions()
    elif val=="About Me":
        openNewwindow()
    elif val=="Learn":
        run()
    elif val=="Website":
        open_website()

def run():
    os.system("Learn_Page.py")

def open_website():
          webbrowser.open("https://www.google.com")

def instructions():
    messagebox.showinfo("Instructions", "1. Create a maze by clicking on the grid or choose\n"
                                        "    one of the functions from the drop-down menu\n"
                                        "\n"
                                        "    You can always edit generated mazes!\n"
                                        "\n"
                                        "2. Choose one of four algorithms to find the shortest path\n"
                                        "     and visualize the search with desired speed of animation\n"
                                        "\n"
                                        "3. Reset the grid if necessary\n"
                                        "\n"
                                        "4. For learning these algorithms you can visit the website or\n"
                                        "     simply navigate to Instructions --> Learn\n")


# User interface area

customtkinter.CTkLabel(UI_frame, text="PATHFINDING\nVISUALIZER", font=("Helvetica", 18)).grid(row=2, column=0, padx=5, pady=(20, 5))

bldMenu = customtkinter.CTkComboBox(UI_frame,
                       values=['Random walls', 'Circular maze', 'Carved out maze'],width=150, font=("Helvetica", 13), fg_color="#f1faee", border_color="#f1faee",
                                    dropdown_fg_color="#f1faee", dropdown_hover_color="Yellow", text_color="Black", dropdown_text_color="Black"
                                    ,button_color="#f1faee")
bldMenu.grid(row=3, column=0, padx=5, pady=(15,5))


bldMenu.bind("<<ComboboxSelected>>", scale_action)

customtkinter.CTkLabel(UI_frame, text="Wall Density:", font=("Helvetica", 12)).grid(row=6, column=0, padx=5, pady=(5, 5))
wallsScale = customtkinter.CTkSlider(UI_frame, from_=10, to=40, number_of_steps=8
                  )
wallsScale.grid(row=7, column=0, padx=5, pady=5, sticky=W)


customtkinter.CTkButton(UI_frame, text='Build maze', command=build_maze, font=("Helvetica", 14), fg_color="#ffb703",hover_color="#e9c46a",text_color="Black"
      ).grid(row=8, column=0, padx=5, pady=(10, 20))

customtkinter.CTkLabel(UI_frame, text="=================", font=("Helvetica", 18)).grid(row=9, column=0, padx=5, pady=(20, 5))

algMenu = customtkinter.CTkComboBox(UI_frame,
                       values=['A-star Algorithm', 'BFS Algorithm', 'DFS Algorithm',
                               "Dijkstra's Algorithm"] , width=150,font=("Helvetica", 13), fg_color="#f1faee", border_color="#f1faee",
                                    dropdown_fg_color="#f1faee", dropdown_hover_color="Yellow", text_color="Black", dropdown_text_color="Black"
                                    ,button_color="#f1faee")
algMenu.grid(row=10, column=0, padx=5, pady=(20, 5))


customtkinter.CTkLabel(UI_frame, text="Speed:", font=("Helvetica", 12)).grid(row=11, column=0, padx=5, pady=(5, 5))
speedScale = customtkinter.CTkSlider(UI_frame, from_=0, to=0.08, number_of_steps=6)
speedScale.grid(row=13, column=0, padx=5, pady=(5, 5),sticky=W)


customtkinter.CTkButton(UI_frame, text='Start Search', command=StartAlgorithm ,font=("Helvetica", 14),fg_color="#ffb703",hover_color="#e9c46a",text_color="Black"
       ).grid(row=14, column=0, padx=5, pady=(10, 20))

customtkinter.CTkButton(UI_frame, text='Reset', command=Reset, font=("Helvetica", 14),fg_color="#48cae4",text_color="Black",hover_color="#ade8f4"
       ).grid(row=18, column=0, padx=5, pady=(20, 30))



def openNewwindow():
    newWindow = Toplevel()
    newWindow.title("About Us")
    newWindow.geometry("450x200")
    newWindow.maxsize(450, 200)
    Label(newWindow, text="              1. This GUI was made using Python (Tkinter, CustomTkinter) modules.\n"
                          "  follow the steps for installation of all modules.\n"
                          "\n"
                          "    Contact (G-mail): raghav.22111348@viit.ac.in\n"
                          "\n"
                          "2. This is an open source project which can be altered accordingly.\n"
                          "   Future work for this program is to add more DSAs into the GUI.\n"
                          "\n"
                          "3. To know more about this Algorithm Visualizer, visit my GitHub or\n"
                          "    you can simply check out the website.\n"
                          "\n"
                          "4. Thank you for using. HAVE FUN!  :)").pack(side=LEFT)

    img_logo1= PhotoImage(file='logo.png')
    newWindow.iconphoto(False, img_logo1)

ins_menu=customtkinter.CTkOptionMenu(UI_frame, values=["Instructions","Website", "Learn", "About Me"],
                                                                    command=ins_menu_get)
ins_menu.grid(row=20, column=0, padx=20, pady=(10, 10))
ins_menu.set(value="Important")


main_button_1 = customtkinter.CTkButton(UI_frame,text="Learn",command=run ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
main_button_1.grid(row=19, column=0, padx=20, pady=(5, 5),sticky="ns")


# Create grid
grid = make_grid(WIDTH, ROWS)
instructions()

# run loop
root.mainloop()
