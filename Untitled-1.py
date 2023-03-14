
def origin(pos) :
    x0 = pos[0] // 3 * 3
    y0 = pos[1] // 3 * 3
    return x0, y0


print(origin((2,1)))
print(origin((5,2)))
print(origin((7,0)))
print(origin((5,5)))
print(origin((4,2)))
print(origin((8,8)))
print(origin((6,8)))