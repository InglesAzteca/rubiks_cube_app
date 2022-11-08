# st = 'wogrby'
# cube = list(st)

# def cube_rotation(cube, direction, amount): # up, down, left, right
#     if direction == 'up':
#         cube[0], cube[2] = cube[2], cube[0]
#         cube[2], cube[5] = cube[5], cube[2]
#         cube[5], cube[4] = cube[4], cube[5]

#     return cube

# print(cube_rotation(cube, 'up', 1))


def cube_rotation(X_Y_Z, amount, prime=1):
    X = [[0, 2], [2, 5], [5, 4]]
    Y = [[1, 2], [2, 3], [3, 4]]
    Z = [[0, 1], [1, 5], [5, 3]]

    st = 'wogrby'
    cube = list(st)

    if X_Y_Z == 'X':
        rotation = X
    elif X_Y_Z == 'Y':
        rotation = Y
    elif X_Y_Z == 'Z':
        rotation = Z

    for n in range(amount):
        for r in rotation[::prime]:
            r = r[::prime]
            cube[r[0]], cube[r[1]] = cube[r[1]], cube[r[0]]

    return cube


l = [1, 2, 3, 4, 5, 6, 7]
print(l[:6])
