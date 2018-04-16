def main():
    """Basic sudoku solver Version 1"""
    #input_sodoku()

    box_index_dict = {1 : {11, 12, 13, 21, 22, 23, 31, 32, 33},
                      2 : {14, 15, 16, 24, 25, 26, 34, 35, 36},
                      3 : {17, 18, 19, 27, 28, 29, 37, 38, 39},
                      4 : {41, 42, 43, 51, 52, 53, 61, 62, 63},
                      5 : {44, 45, 46, 54, 55, 56, 64, 65, 66},
                      6 : {47, 48, 49, 57, 58, 59, 67, 68, 69},
                      7 : {71, 72, 73, 81, 82, 83, 91, 92, 93},
                      8 : {74, 75, 76, 84, 85, 86, 94, 95, 96},
                      9 : {77, 78, 79, 87, 88, 89, 97, 98, 99}}
    sudoku = given_sudoku()
    sudoku_updated = True
    while sudoku_updated:
        sudoku = check_cols(sudoku)
        boxes = get_boxes(sudoku, box_index_dict)
        sudoku = check_boxes(sudoku, boxes, box_index_dict)
        sudoku, sudoku_updated = set_length_one(sudoku)
        sudoku = check_rows(sudoku)

    print_sudoku(sudoku)

def input_sodoku():
    """For a user inputted sudoku
    creates a dictionary with indexs for each element"""
    output = {}
    j = 1
    while j < 10:
        question = "Please print row " + str(j) + ": "
        row = input(question)

        list = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        temp_list = list

        for char in row:
            if char != " ":
                temp_list.remove(int(char))

        i = 1
        for number in row:
            index = (10*j) + i
            if number == " ":
                output[index] = temp_list
            else:
                output[index] = int(number)
            i += 1
        j += 1
    print(output)

def given_sudoku():
    """a given sudoku for testing purposes"""
    output = {}
    j = 1
    row_list = [' 69  4  8', '28  5 34 ', '      9  ', '1   69 85', '3 6   1 4', '95 24   6', '  2      ', ' 14 2  59', '8  6  47 ']
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


main()
