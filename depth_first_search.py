# car path
e12 = 12
e13 = 16
e23 = 17

B1 = 10
M1 = 10
C1 = 1
S1 = 1
D1 = 1

B2 = 10
M2 = 10
C2 = 1
S2 = 11
D2 = 11

B3 = 100
M3 = 100
C3 = 1
S3 = 1
D3 = 1

dist_mat = [[0, e12, e13], [e12, 0, e23], [e13, e23, 0]]


class city:
    def __init__(self, num: int,charging_rate:float):
        self.num = num
        self.crg_rate = charging_rate # charging rate
        self.dist = dist_mat[num]  # distance from other cities (list)


class car:
    def __init__(self, source: city, destination: city, bat_in: float, crg_rate: float, discrg_rate: float, max_cap: float,
                 avg_speed: float):
        self.src = source
        self.desti = destination  # destination city
        self.init_chrg = bat_in  # initial charge in the battery
        self.discrg_rate = discrg_rate  # discharge rate
        self.max_cap = max_cap  # maximum charge in battery
        self.avg_speed = avg_speed


def path_plot(car_t: car, city_list):
    # dfs basic    NOT OPTIMISED
    open = list()
    openl = list()
    jme = list()
    crg = car_t.init_chrg
    pre = None
    src = car_t.src
    temp = [src.num, None]
    while src.num != car_t.dest.num:
        for i in range(len(src.dist)):
            if src.dist[i] is not None and src.dist[i] <= car_t.max_cap and i not in openl and src.dist[i] != 0:
                jme.append([i, src.num])
        if len(jme) == 0:
            return -1
        else:
            open.append([src.num, pre])
            openl.append(src.num)
            temp = jme.pop()
            src = city_list[temp[0]]
            pre = temp[1]

    # path
    path = list()
    curr = temp[0]
    prev = temp[1]
    while curr != car_t.src.num:
        path.insert(0, curr)
        for i in open:
            if i[0] == prev:
                prev = i[1]
                curr = i[0]
                break
    path.insert(0, car_t.src.num)

    return path


if __name__ == '__main__':
    V1 = city(0,1)
    V2 = city(1,0.5)
    V3 = city(2,0.5)

    C1 = car(V1, V2, B1, C1, D1, M1, S1)
    C2 = car(V2, V3, B2, C2, D2, M2, S2)
    C3 = car(V3, V1, B3, C3, D3, M3, S3)

    city_list = [V1, V2, V3]
    car_list = [C1, C2, C3]

    solution = list()
    for i in car_list:
        solution.append(path_plot(i, city_list))

    for i in solution:
        print(i)
