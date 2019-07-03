# coding: utf-8


# Khayyam Triangle

# The French mathematician, Blaise Pascal, who built a mechanical computer in
# the 17th century, studied a pattern of numbers now commonly known in parts of
# the world as Pascal's Triangle (it was also previously studied by many Indian,
# Chinese, and Persian mathematicians, and is known by different names in other
# parts of the world).

# The pattern is shown below:

#                    1
#                   1 1
#                  1 2 1
#                 1 3 3 1
#                1 4 6 4 1
#                   ...

# Each number is the sum of the number above it to the left and the number above
# it to the right (any missing numbers are counted as 0).

# Define a procedure, triangle(n), that takes a number n as its input, and
# returns a list of the first n rows in the triangle. Each element of the
# returned list should be a list of the numbers at the corresponding row in the
# triangle.


def triangle(n):
    tri = []
    for i in range(n):
        tri.append([])
        tri[i].append(1)
        for j in range(1, i):
            tri[i].append(tri[i - 1][j - 1] + tri[i - 1][j])
        if i > 0:
            tri[i].append(1)
    return tri


# For example:

print(triangle(0))
# >>> []

print(triangle(1))
# >>> [[1]]

print(triangle(2))
# >> [[1], [1, 1]]

print(triangle(3))
# >>> [[1], [1, 1], [1, 2, 1]]

print(triangle(6))
# >>> [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]
