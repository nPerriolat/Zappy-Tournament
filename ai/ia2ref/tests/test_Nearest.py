x = 6
y = 13
liste: list[list[str | int]] = [['' for j in range(x)] for i in range(y)]
liste2: list[list[str | int]] = [['' for j in range(x)] for i in range(y)]

# right -> up
# i_sz = len(liste)
# j_sz = len(liste[0])
# size = i_sz + j_sz
# for i in range(i_sz):
#     for j in range(min(i, j_sz - 1), -1, -1):
#         print(i, j)
#         liste[i - j][j] = i

# right -> down
# i_sz = len(liste)
# j_sz = len(liste[0])
# size = i_sz + j_sz
# for i in range(i_sz):
#     for j in range(min(i, j_sz - 1), -1, -1):
#         print(i, j)
#         liste2[j - i - 1][j] = i

# left -> up
# i_sz = len(liste)
# j_sz = len(liste[0])
# size = i_sz + j_sz
# for i in range(i_sz):
#     for j in range(min(i, j_sz - 1), -1, -1):
#         print(i, j)
#         liste2[i - j][-j + j_sz - 1] = i

# left -> down
# i_sz = len(liste)
# j_sz = len(liste[0])
# size = i_sz + j_sz
# for i in range(i_sz):
#     for j in range(min(i, j_sz - 1), -1, -1):
#         print(i, j)
#         liste2[j - i - 1][-j + j_sz - 1] = i


# for row in liste2:
#     print(row)

def get_d(start: int, dest: int, maxi: int) -> tuple[int, int]:
    if start == dest:
        return (0, 0)

    a = dest - start
    x = (a, abs(a))

    b = (maxi + 1 - start) + dest
    y = (b, abs(b))

    mini = min(x[1], y[1])
    if mini == x[1]:
        return x
    return y
    # return y

print(get_d(8, 9, 10))


# size = 11
# liste: list[list[int | None]] = [[None] * 4 for _ in range(7)]

# for i in range(size):
#     for j in range(min(i + 1, 7)):
#         if j >= 4:
#             continue
#         liste[i - j][j] = i

# for row in liste:
#     print(row)
