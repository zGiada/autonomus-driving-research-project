import random
import numpy as np

car = 1
buildings = -1
road = 0

class Matrix:
    # righe
    # colonne
    # matrice di occupazione
    # matrici di visibilità (?)

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def return_dims_occupation(self):
        return self.rows, self.cols


class Visibility(Matrix):
    def __init__(self, rows, cols):
        super().__init__(rows*rows, cols*cols)


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
        while num_cars > 0:
            i = random.randint(0, self.rows-1)
            j = random.randint(0, self.rows - 1)
            if tmp[i][j] == road:
                tmp[i][j] = car
                num_cars -= 1
        return np.array(tmp)

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
