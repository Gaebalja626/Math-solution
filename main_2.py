import numpy as np


def goodprint(s, m=2, k=2):
    s = float(s)
    a, b = str(s).split(".")
    return " " * (m - len(a)) + a + "." + b[:k] + " " * (k - len(b))


class tsts:
    def __init__(self, m):
        self.a, self.b = m

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return tsts((self.a * other, self.b * other))
        return tsts((self.a * other.a, self.b * other.b))

    def __add__(self, other):
        return tsts((self.a * other.b + self.b * other.a, self.b * other.b))

    def __sub__(self, other):
        return tsts((self.a * other.b - self.b * other.a, self.b * other.b))

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            return tsts((self.a / other, self.b / other))
        return tsts((self.a * other.b, self.b * other.a))

    def __call__(self):
        return self.a / self.b


"""0 4 3 -2
-1 2 -3 9
1 1 -1 2"""
# unique solution
# x1 = -1.0 , x2 = 1.0 , x3 = -2.0 ,

"""0 -3 -6 4 9
-1 -2 -1 3 1
-2 -3 0 3 -1
5 4 1 -9 -7"""
# unique solution
# x1 = -2.5 , x2 = 2.0 , x3 = -2.5 , x4 = -0.0 ,


"""0 3 -6 6 4 -5
3 -7 8 -5 8 9
3 -9 12 -9 6 15"""
# infinite solution

input_data = """1 2 -5 -4 0 -5
0 1 -6 -4 0 2
"""  # input()

augmentMatrix = np.array(
    [list(map(lambda x: tsts(float(x).as_integer_ratio()), line.split())) for line in input_data.split("\n")])
# np.array(list(map(lambda x: list(map(int, x.split())), (input_data.split("\n")))))

shape = augmentMatrix.shape

print("\nAugmented Matrix")
for x in augmentMatrix:
    print(' '.join(tuple(map(lambda y: goodprint(y()), x))))

point_column = 0  # leading entry
row = 0

while row < shape[0] - 1 and point_column < shape[1]:
    if augmentMatrix[row][point_column]() == 0:  # target row를 0이 아니게 시작하는것
        for point_row in range(row + 1, shape[0]):
            if augmentMatrix[point_row][point_column]() != 0:
                temp = np.array(augmentMatrix[point_row])
                augmentMatrix[point_row] = augmentMatrix[row]
                augmentMatrix[row] = temp
                break  # 만약 0이 아닌거로 시작하면 그거로 끝
        else:
            point_column += 1  # 만약 point_column에서 0을 찾아낼 수 없다면, 다음거로 넘어감
            continue
    # 이제 target row가 완벽하게 설정 됐으니까, leading entry아래의 모든것들을 0으로 만들자!
    for point_row in range(row + 1, shape[0]):
        print("\n")
        print((augmentMatrix[point_row][point_column](), " / ", augmentMatrix[row][point_column]()))
        augmentMatrix[point_row] -= augmentMatrix[row] * (
            (augmentMatrix[point_row][point_column] / augmentMatrix[row][point_column]))
        for x in augmentMatrix:
            print(' '.join(tuple(map(lambda y: goodprint(y()), x))))
    row += 1
    point_column += 1

echelonMatrix = np.array(augmentMatrix)
# 이제는 echolen Matrix이므로, reduce 시켜야함!


print("\nEchelon Matrix")
for x in echelonMatrix:
    print(' '.join(tuple(map(lambda y: goodprint(y()), x))))
pivot_column_test = False
pivot_column_count = 0
row = shape[0] - 1
while row >= 0:
    pivot_column = 0
    for column in range(shape[1]):
        if echelonMatrix[row][column]() != 0:
            pivot_column = column
            if pivot_column == shape[1] - 1:
                pivot_column_test = True
            break
    else:
        row -= 1
        continue


    echelonMatrix[row] /= echelonMatrix[row][pivot_column]

    for point_row in range(row):
        echelonMatrix[point_row] -= echelonMatrix[row] * (echelonMatrix[point_row][pivot_column])
    print()
    for x in echelonMatrix:
        print(' '.join(tuple(map(lambda y: goodprint(y()), x))))
    # print(row, "번째 row를 확인!!")
    # print(echelonMatrix)
    pivot_column_count += 1
    row -= 1

print("\nReduced Echelon Matrix")
for x in echelonMatrix:
    print(' '.join(tuple(map(lambda y: goodprint(y()), x))))

if pivot_column_test:
    print("inconsistent")
elif pivot_column_count == shape[1] - 1:  # 모든 variables가 pivot column이 있다면, unique고 아닌 모든경우는 무한한 해를 가진다?
    print("unique solution")
    for x in range(shape[1] - 1):
        print("x" + str(x + 1) + " = " + str(round(np.transpose(echelonMatrix)[-1][x](), 7)), end="\n")
else:
    print("infinite solution")
