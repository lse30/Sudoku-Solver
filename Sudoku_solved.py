from tkinter import *
from tkinter.ttk import *





class SudokuGui:
    """Sudoku Gui for sudoku solver"""

    def __init__(self, window):
        """sets up the window"""

        self.title = Label(window, text="Sudoku Solver")
        self.title.grid(row=0, column=1, pady=10, columnspan = 9)

        self.left_edge = Label(window, text=" ")
        self.left_edge.grid(row=0, column=0, pady=0)

        self.right_edge = Label(window, text=" ")
        self.right_edge.grid(row=0, column=10, pady=0)

        self.entry_dict = {}
        i = 1
        j = 1
        while j < 10:
            while i < 10:
                if i in [3,6] and j in [3,6]:
                    self.entry = Entry(window, width=3)
                    self.entry.grid(row=j, column=i, padx=(0,3), pady=(0,3))
                    k = (j*10) + i
                    self.entry_dict[k] = self.entry
                    i += 1
                elif i in [3,6] and j not in [3,6]:
                    self.entry = Entry(window, width=3)
                    self.entry.grid(row=j, column=i, padx=(0, 3))
                    k = (j * 10) + i
                    self.entry_dict[k] = self.entry
                    i += 1
                elif i not in [3,6] and j in [3,6]:
                    self.entry = Entry(window, width=3)
                    self.entry.grid(row=j, column=i, pady=(0, 3))
                    k = (j * 10) + i
                    self.entry_dict[k] = self.entry
                    i += 1
                else:
                    self.entry = Entry(window, width=3)
                    self.entry.grid(row=j, column=i)
                    k = (j * 10) + i
                    self.entry_dict[k] = self.entry
                    i += 1

            j += 1
            i = 1


        self.calc = Button(window, text="Calculate", command=self.print_dict)
        self.calc.grid(row=10, column=1, columnspan = 9, pady=10)

    def print_dict(self):
        """dfsdfsdfsd sdfsd"""
        sudoku_dict = {}
        for key in self.entry_dict:
            output = self.entry_dict[key]
            new = output.get()
            if new == '':
                sudoku_dict[key] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                sudoku_dict[key] = int(new)
        solver(sudoku_dict)


def solver(sudoku_dict):
    """Basic sudoku solver Version 1"""
    brute_hist = []
    sudoku = sudoku_dict
    not_complete = True
    pre_sudoku = sudoku.copy()
    while not_complete:
        sudoku = cycle_sudoku(sudoku)
        health = check_health(sudoku)
        if health == 1:
            print_sudoku(sudoku)
            break
        elif health == 2:
            brute_hist = brute_backtrack(brute_hist)
            sudoku = pre_sudoku.copy()
            for data in brute_hist:
                sudoku[data[0]] = data[1]
        else:
            brute_hist = brute_forward(sudoku, brute_hist)



def brute_forward(sudoku, brute_hist):
    info = []
    for index in sudoku:
        if type(sudoku[index]) == set:
            set_list = sudoku[index].copy()
            elem = sudoku[index].pop()
            info = (index, elem, sudoku[index], set_list)
            brute_hist.append(info)
            sudoku[index] = elem
            break
    return brute_hist

def brute_backtrack(brute_hist):
    info = brute_hist[-1]
    while info[2] == set():
        del brute_hist[-1]
        info = brute_hist[-1]
    del brute_hist[-1]
    elem = info[2].pop()
    new_info = (info[0], elem, info[2], info[3])
    brute_hist.append(new_info)
    return brute_hist

def check_health(sudoku):
    """1 is a solved sudoku, 2 is an impossible sudoku, 3 is an incomplete sudoku"""
    outcome = empty_set(sudoku)
    if outcome == 1:
        outcome = check_pairs(sudoku)

    return outcome

def empty_set(sudoku):
    for index in sudoku:
        if type(sudoku[index]) == set:
            if sudoku[index] == set():
                return 2
            else:
                return 3
    return 1

def check_pairs(sudoku):
    outcome = row_pairs(sudoku)
    if outcome == False:
        outcome = col_pairs(sudoku)
        if outcome == False:
            outcome = box_pairs(sudoku)
            if outcome == False:
                return 1
    return 2

def col_pairs(sudoku):
    """Iterates through the cols and removes possiblies if the number appears in the cols"""
    i = 1
    col = set()
    while i < 10:
        j = 1
        while j < 10:
            index = (10 * j) + i
            number = sudoku[index]
            col.add(number)
            j += 1
        if len(col) < 9:
            return True
        i += 1
        col = set()
    return False

def row_pairs(sudoku):
    """Iterates through the rows and removes possiblies if the number appears in the row"""
    j = 1
    row = set()
    while j < 10:
        i = 1
        while i < 10:
            index = (10*j) + i
            number = sudoku[index]
            row.add(number)
            i += 1
        if len(row) < 9:
            return True
        j += 1
        row = set()
    return False

def box_pairs(sudoku):
    box_index_dict = {1 : {11, 12, 13, 21, 22, 23, 31, 32, 33},
                      2 : {14, 15, 16, 24, 25, 26, 34, 35, 36},
                      3 : {17, 18, 19, 27, 28, 29, 37, 38, 39},
                      4 : {41, 42, 43, 51, 52, 53, 61, 62, 63},
                      5 : {44, 45, 46, 54, 55, 56, 64, 65, 66},
                      6 : {47, 48, 49, 57, 58, 59, 67, 68, 69},
                      7 : {71, 72, 73, 81, 82, 83, 91, 92, 93},
                      8 : {74, 75, 76, 84, 85, 86, 94, 95, 96},
                      9 : {77, 78, 79, 87, 88, 89, 97, 98, 99}}
    boxes = get_boxes(sudoku, box_index_dict)
    box_set = set()
    for box in boxes:
        for number in box:
            box_set.add(number)
        if len(box_set) < 9:
            return True
        box_set = set()
    return False

def cycle_sudoku(sudoku):
    box_index_dict = {1 : {11, 12, 13, 21, 22, 23, 31, 32, 33},
                      2 : {14, 15, 16, 24, 25, 26, 34, 35, 36},
                      3 : {17, 18, 19, 27, 28, 29, 37, 38, 39},
                      4 : {41, 42, 43, 51, 52, 53, 61, 62, 63},
                      5 : {44, 45, 46, 54, 55, 56, 64, 65, 66},
                      6 : {47, 48, 49, 57, 58, 59, 67, 68, 69},
                      7 : {71, 72, 73, 81, 82, 83, 91, 92, 93},
                      8 : {74, 75, 76, 84, 85, 86, 94, 95, 96},
                      9 : {77, 78, 79, 87, 88, 89, 97, 98, 99}}
    sudoku_updated = True
    while sudoku_updated:
        sudoku = check_cols(sudoku)
        boxes = get_boxes(sudoku, box_index_dict)
        sudoku = check_boxes(sudoku, boxes, box_index_dict)
        sudoku, sudoku_updated = set_length_one(sudoku)
        sudoku = check_rows(sudoku)
    return sudoku

def given_sudoku():
    """a given sudoku for testing purposes"""
    output = {}
    j = 1
    row_list = ['4 8  59 6', ' 7    43 ', '    8    ', '     2  9', '  15793  ', '2  6     ', '    5    ', ' 14    9 ', '8 39  6 2']
    while j < 10:
        for row in row_list:

            list = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            temp_set = list

            for char in row:
                if char != " ":
                    temp_set.remove(int(char))

            i = 1
            for number in row:
                index = (10*j) + i
                if number == " ":
                    output[index] = temp_set
                else:
                    output[index] = int(number)
                i += 1
            j += 1
    return output

def check_cols(sudoku):
    """Iterates through the columns of the sudoku
    and eliminates the options if the number appears in the column"""
    i = 1
    col = set()
    while i < 10:
        j = 1
        while j < 10:
            index = (10*j) + i
            number = sudoku[index]
            if type(number) == int:
                col.add(number)
            j += 1
        k = 1
        while k < 10:
            index = (10*k) + i
            number = sudoku[index]
            k += 1
            if type(number) == set:
                new = number - col
                sudoku[index] = new
        col = set()
        i += 1
    return sudoku

def check_rows(sudoku):
    """Iterates through the rows and removes possiblies if the number appears in the row"""
    j = 1
    row = set()
    while j < 10:
        i = 1
        while i < 10:
            index = (10*j) + i
            number = sudoku[index]
            if type(number) == int:
                row.add(number)
            i += 1

        k = 1
        while k < 10:
            index = (10*j) + k
            number = sudoku[index]
            k += 1
            if type(number) == set:
                new = number - row
                sudoku[index] = new
        row = set()
        j += 1
    return sudoku

def get_boxes(su, box_index_dict):
    """This was the easist way to retrieve the values for the boxes"""
    boxes = []
    for key in box_index_dict:
        box = []
        for index in box_index_dict[key]:
            box.append(su[index])
        boxes.append(box)
    return boxes

def check_boxes(sudoku, boxes, box_index_dict):
    """iterates through the boxes, this needs polishing up because its uses the box dict which is a lot cleaner
    than the get boxes function"""
    box_num = 1
    box_dict = {}
    for box in boxes:
        box_nums = set()
        for value in box:
            if type(value) == int:
                box_nums.add(value)
        box_dict[box_num] = box_nums
        box_num += 1
    for section in box_index_dict:
        test_box = box_dict[section]
        for value in (box_index_dict[section]):
            if type(sudoku[value]) == set:
                new = sudoku[value] - test_box
                sudoku[value] = new
    return sudoku

def set_length_one(sudoku):
    """if there is only one possible number for a certain index then it updates it to an interger and
    notifies main that the sudoku has been updated with a new number solved"""
    sudoku_updated = False
    for index in sudoku:
        if type(sudoku[index]) == set:
            if len(sudoku[index]) == 1:
                element = list(sudoku[index])[0]
                #print("Solved position {0} = {1}".format(index,element))
                sudoku_updated = True

                sudoku[index] = element

    return sudoku, sudoku_updated

def print_sudoku(sudoku):
    """Prints the sudoku in a readable manner"""
    line = []
    count = 1
    for index in sudoku:
        line.append(sudoku[index])
        if count == 9:
            print(line)
            count = 1
            line = []
        else:
            count += 1


def main():
    """the main for sudoku solver"""
    window = Tk()
    sudoku_solver = SudokuGui(window)
    window.mainloop()


main()