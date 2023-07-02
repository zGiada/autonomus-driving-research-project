import math
import random
import numpy as np

car = 1
buildings = -1
road = 0

there_is_the_car = 1 #None 
not_see = 0
can_see = 1


class Matrix:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def return_dims_occupation(self):
        return self.rows, self.cols


class Visibility(Matrix):
    def __init__(self, rows, cols):
        super().__init__(rows*rows, cols*cols)

    

    def create_single_visibility(self, coordinates, occ_matrix):
        occupation_base = (occ_matrix).tolist()
        starting_pos_i = coordinates[0]
        starting_pos_j = coordinates[1]
        dim_rows = int(math.sqrt(self.rows))
        dim_cols = int(math.sqrt(self.cols))
        visibility_matrix = [[0] * dim_cols for _ in range(dim_rows)]

        #insert car position
        visibility_matrix[starting_pos_i][starting_pos_j] = there_is_the_car

        #print("******* car coordinates: ", coordinates, "\n")
        #print("\noccupation:\n", np.array(occupation_base), "\nvisibility:\n", np.array(visibility_matrix))



        #'''
        # scorro la riga dopo la cella
        # print("riga dopo la cella...")
        x = starting_pos_j + 1
        found_b = False
        while x < dim_cols:
            cell = occupation_base[starting_pos_i][x]
            # print("cell: ", cell)
            if found_b:
                visibility_matrix[starting_pos_i][x] = 0
            else:
                if cell == -1:
                    visibility_matrix[starting_pos_i][x] = 0
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[starting_pos_i][x] = 1
            x += 1

        # scorro la riga prima della cella
        # print("riga prima della cella...")
        x = starting_pos_j - 1
        found_b = False
        while x >= 0:
            cell = occupation_base[starting_pos_i][x]
            # print("cell: ", cell)
            if found_b:
                visibility_matrix[starting_pos_i][x] = 0
            else:
                if cell == -1:
                    visibility_matrix[starting_pos_i][x] = 1
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[starting_pos_i][x] = 1
            x -= 1

        # scorro la colonna dopo la cella
        # print("colonna dopo della cella...")
        i = starting_pos_j + 1
        count = 0
        while i < dim_cols:
            x = starting_pos_i + 1 + count
            #print("x value = ",x, "count value = ", count)
            found_b = False
            while x < dim_rows:
                cell = occupation_base[x][starting_pos_j + count]
                #print("cell coordinates[",x,",",(starting_pos_j + count), "] => value = ", cell)
                if found_b:
                    visibility_matrix[x-count][starting_pos_j + count] = 0
                else:
                    if cell == -1:
                        visibility_matrix[x-count][starting_pos_j + count] = 1
                        found_b = True
                    if cell == 1 or cell == 0:
                        visibility_matrix[x-count][starting_pos_j + count] = 1
                x += 1
            i+=1
            count+=1

        # scorro la colonna prima della cella
        # print("colonna prima della cella...")
        x = starting_pos_i - 1
        found_b = False
        while x >= 0:
            cell = occupation_base[x][starting_pos_j]
            # print("cell: ", cell)
            if found_b:
                visibility_matrix[x][starting_pos_j] = 0
            else:
                if cell == -1:
                    visibility_matrix[x][starting_pos_j] = 1
                    found_b = True
                if cell == 1 or cell == 0:
                    visibility_matrix[x][starting_pos_j] = 1
            x -= 1

        return np.array(visibility_matrix)


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

    # non funziona, ma sarebbe carino per impostare il massimo numero di
    def max_cars(self):
        matrix = Occupation.create_occupation_matrix()
        value = np.count_nonzero(matrix == road)
        return value/3 # a caso

    def insert_cars(self, matrix, num_cars):
        tmp = matrix.tolist()
        positions = []
        while num_cars > 0:
            i = random.randint(0, self.rows-1)
            j = random.randint(0, self.cols-1)
            if tmp[i][j] == road:
                tmp[i][j] = car
                #l'indice definisce la macchina
                # es. indice 0 => coordinate della posizione della car 0
                positions.append([i,j])
                num_cars = num_cars - 1
        return np.array(tmp), positions

    def create_occupation_matrix(self):
        matrix = [[buildings] * self.cols for _ in range(self.rows)]
        start = True
        count = 0
        i = 0
        while i < self.rows:
            #print(" i = ", i, "\n")
            if i == 0 or start:
                # creo la prima riga
                create_row = []
                first_block = False
                second_block = False
                # creo la riga
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
                #print("count", count)
                start = False
            else:
                if count > 0:
                    while count > 0:
                        #print("sto facendo la riga di indice", i, "con count che vale",count ,"e n vale ",n)
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
                        #print("sto facendo la riga di indice", i, "con ones che vale",ones ,"e n vale ", n)
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
            #print("\n",np.array(matrix), "\n---------------\n")

        return np.array(matrix)
