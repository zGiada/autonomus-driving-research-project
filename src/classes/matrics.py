import math
import random
import numpy as np


# global useful variables
car = 1
buildings = -1
road = 0

there_is_the_car = 1
not_see = 0
can_see = 1

# ############################################ #
#   Definition of the class Matrix             #
#                           ^    ^             #
#                           |    |             #
# and subclasses     Occupancy  Visibility     #
# ############################################ #

class Matrix:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def return_dims_occupation(self):
        return self.rows, self.cols


class Visibility(Matrix):
    def __init__(self, rows, cols):
        super().__init__(rows*rows, cols*cols)

    # function that create the visibility matrix of a single cell
    def create_single_visibility(self, coordinates, occ_matrix):
        occupation_base = (occ_matrix).tolist()
        starting_pos_i = coordinates[0]
        starting_pos_j = coordinates[1]
        dim_rows = int(math.sqrt(self.rows))
        dim_cols = int(math.sqrt(self.cols))
        visibility_matrix = [[0] * dim_cols for _ in range(dim_rows)]

        #insert car/road position (1 or 0)
        visibility_matrix[starting_pos_i][starting_pos_j] = there_is_the_car

        # set the visibility for all cells that are in the same row and to the right of the input cell
        x = starting_pos_j + 1
        found_b = False
        while x < dim_cols:
            cell = occupation_base[starting_pos_i][x]
            if found_b:
                visibility_matrix[starting_pos_i][x] = not_see
            else:
                if cell == -1:
                    visibility_matrix[starting_pos_i][x] = not_see
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[starting_pos_i][x] = can_see
            x += 1

        # set the visibility for all cells that are in the same row and to the left of the input cell
        x = starting_pos_j - 1
        found_b = False
        while x >= 0:
            cell = occupation_base[starting_pos_i][x]
            if found_b:
                visibility_matrix[starting_pos_i][x] = not_see
            else:
                if cell == -1:
                    visibility_matrix[starting_pos_i][x] = not_see
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[starting_pos_i][x] = can_see
            x -= 1

        # sets the visibility for all cells that are in the same column and below the input cell
        found_b = False
        x = starting_pos_i + 1
        while x < dim_rows:
            cell = occupation_base[x][starting_pos_j]
            if found_b:
                visibility_matrix[x][starting_pos_j] = not_see
            else:
                if cell == -1:
                    visibility_matrix[x][starting_pos_j] = not_see
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[x][starting_pos_j] = can_see
            x += 1


        # sets the visibility for all cells that are in the same column and above the input cell
        x = starting_pos_i - 1
        found_b = False
        while x >= 0:
            cell = occupation_base[x][starting_pos_j]
            if found_b:
                visibility_matrix[x][starting_pos_j] = not_see
            else:
                if cell == -1:
                    visibility_matrix[x][starting_pos_j] = not_see
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[x][starting_pos_j] = can_see
            x -= 1

        # sets the visibility for all cells that are in the previous row and to the left of the input cell
        if (starting_pos_j - 1 >= 0 and starting_pos_i - 1 >= 0):
            x = starting_pos_j - 1
            found_b = False
            while x >= 0:
                cell = occupation_base[starting_pos_i - 1][x]
                if found_b:
                    visibility_matrix[starting_pos_i - 1][x] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[starting_pos_i - 1][x] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[starting_pos_i - 1][x] = can_see
                x -= 1

        # sets the visibility for all cells that are in the next row and to the left of the input cell
        if (starting_pos_j - 1 >= 0 and starting_pos_i + 1 < dim_rows):
            x = starting_pos_j - 1
            found_b = False
            while x >= 0:
                cell = occupation_base[starting_pos_i + 1][x]
                if found_b:
                    visibility_matrix[starting_pos_i + 1][x] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[starting_pos_i + 1][x] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[starting_pos_i + 1][x] = can_see
                x -= 1

        # sets the visibility for all cells that are in the next column and above the given input cell
        if (starting_pos_i-1>=0 and starting_pos_j + 1 < dim_rows):
            x = starting_pos_i - 1
            found_b = False
            while x >= 0:
                cell = occupation_base[x][starting_pos_j + 1]
                if found_b:
                    visibility_matrix[x][starting_pos_j + 1] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[x][starting_pos_j + 1] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[x][starting_pos_j + 1] = can_see
                x -= 1

        # sets the visibility for all cells that are in the previous column and above the given input cell
        if (starting_pos_i-1>=0 and starting_pos_j - 1 >= 0):
            x = starting_pos_i - 1
            found_b = False
            while x >= 0:
                cell = occupation_base[x][starting_pos_j - 1]
                if found_b:
                    visibility_matrix[x][starting_pos_j - 1] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[x][starting_pos_j - 1] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[x][starting_pos_j - 1] = can_see
                x -= 1

        # sets the visibility for all cells that are in the previous column and below the given input cell
        if (starting_pos_i + 1 < dim_rows and starting_pos_j - 1 >= 0):
            found_b = False
            x = starting_pos_i + 1
            while x < dim_rows:
                cell = occupation_base[x][starting_pos_j - 1]
                if found_b:
                    visibility_matrix[x][starting_pos_j - 1] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[x][starting_pos_j - 1] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[x][starting_pos_j - 1] = can_see
                x += 1

        # sets the visibility for all cells that are in the next column and below the given input cell
        if (starting_pos_i + 1 < dim_rows and starting_pos_j + 1 < dim_rows):
            found_b = False
            x = starting_pos_i + 1
            while x < dim_rows:
                cell = occupation_base[x][starting_pos_j + 1]
                if found_b:
                    visibility_matrix[x][starting_pos_j + 1] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[x][starting_pos_j + 1] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[x][starting_pos_j + 1] = can_see
                x += 1

        # sets the visibility for all cells that are in the previous row and to the right of the input cell
        if (starting_pos_i -1 >= 0 and starting_pos_j + 1 < dim_cols):
            x = starting_pos_j + 1
            found_b = False
            while x < dim_cols:
                cell = occupation_base[starting_pos_i - 1][x]
                if found_b:
                    visibility_matrix[starting_pos_i - 1][x] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[starting_pos_i - 1][x] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[starting_pos_i - 1][x] = can_see
                x += 1

        # sets the visibility for all cells that are in the next row and to the right of the input cell
        if (starting_pos_i + 1 < dim_rows and starting_pos_j + 1 < dim_rows):
            x = starting_pos_j + 1
            found_b = False
            while x < dim_cols:
                cell = occupation_base[starting_pos_i + 1][x]
                if found_b:
                    visibility_matrix[starting_pos_i + 1][x] = not_see
                else:
                    if cell == -1:
                        visibility_matrix[starting_pos_i + 1][x] = not_see
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[starting_pos_i + 1][x] = can_see
                x += 1

        return np.array(visibility_matrix)

    # function that given all the single visibility matrix creates the complete visibility matrix
    def create_complete_visibility(self, occupation_matrix):
        complete_visibility = []
        rows = occupation_matrix.shape[0]
        cols = occupation_matrix.shape[1]
        for x in range(rows):
            cella = []
            for y in range(cols):
                if (occupation_matrix[x][y] != -1):
                    vis = self.create_single_visibility([x, y], occupation_matrix)
                    vis = vis.tolist()
                    flattened_list = [element for sublist in vis for element in sublist]
                    complete_visibility.append(flattened_list)
                else:
                    flattened_list = [[0] * cols for _ in range(rows)]
                    flattened_list = [element for sublist in flattened_list for element in sublist]
                    complete_visibility.append(flattened_list)
        complete_visibility = np.array(complete_visibility)
        return complete_visibility


class Occupation(Matrix):

    def __init__(self, rows, cols):
        super().__init__(rows, cols)

    # function that inserts the number of cars into the occupancy matrix
    def insert_cars(self, matrix, num_cars):
        tmp = matrix.tolist()
        positions = []
        while num_cars > 0:
            i = random.randint(0, self.rows-1)
            j = random.randint(0, self.cols-1)
            if tmp[i][j] == road:
                tmp[i][j] = car
                positions.append([i,j])
                num_cars = num_cars - 1
        return np.array(tmp), positions

    # function that creates the occupation matrix, given the number of rows and columns
    def create_occupation_matrix(self):
        matrix = [[buildings] * self.cols for _ in range(self.rows)]
        start = True
        count = 0
        i = 0
        while i < self.rows:
            if i == 0 or start:
                # create the first row
                create_row = []
                first_block = False
                second_block = False
                for j in range(self.cols):
                    value = buildings
                    num = random.randint(buildings, road)
                    if (num == road) or first_block:
                        if not (first_block) and not (second_block):
                            value = road
                            matrix[i][j] = value
                            first_block = True
                        else:
                            if first_block and not (second_block):
                                value = road
                                matrix[i][j] = value
                                second_block = True

                            else:
                                first_block = False
                                second_block = False
                                value = buildings
                                matrix[i][j] = value

                    create_row.append(value)

                if create_row[len(create_row) - 1] == road:
                    if create_row[len(create_row) - 2] == road:
                        pass
                    else:
                        create_row[len(create_row) - 1] = buildings
                if create_row.count(road) == 1:
                    create_row = [buildings] * len(create_row)
                if create_row.count(road) == 0:
                    start = random.randint(0, len(create_row) - 2)
                    create_row[start] = road
                    create_row[start + 1] = road

                row = create_row

                for j in range(self.cols):
                    matrix[i][j] = row[j]

                count = random.randint(1, round(self.rows / 2))
                start = False
            else:
                if count > 0:
                    while count > 0:
                        if i >= self.rows:
                            break
                        else:
                            for j in range(self.cols):
                                matrix[i][j] = row[j]
                        i += 1
                        count -= 1

                    count = 0
                    ones = 0
                    while ones < 2:
                        if ones > self.rows:
                            break
                        else:
                            if i == self.rows:
                                break
                            else:
                                for j in range(self.cols):
                                    matrix[i][j] = road
                            ones += 1
                            i += 1
                i = i - 1
                start = True
            i += 1            

        return np.array(matrix)