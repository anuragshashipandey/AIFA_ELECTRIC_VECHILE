class city:
    def __init__(self, num: int, distance_arr: list):
        self.num = num

        self.distance = distance_arr  # distance_mat[num] #distanceance from other cities (list)


class car:
    def __init__(self, source_vertex: city, dest_vertex: city, battery_current_charge: float, discharge_rate: float,
                 max_capacity: float, avg_speed: float,
                 charging_rate: float):
        # given
        self.src = source_vertex
        self.dest = dest_vertex  # destination city
        self.init_charge = battery_current_charge  # initial charge in the battery
        self.discrg_rate = discharge_rate  # discharge rate
        self.max_cap = max_capacity  # maximum charge in battery
        self.crg_rate = charging_rate  # charging rate
        self.avg_speed = avg_speed #average speed

        # found
        self.tot_time = None
        self.path = list()


def path_plot(car_s: car, city_list):
    class node:
        def __init__(self, cty: city, pred=None, heuristic_cost=None, t_cost=None):
            self.cty = cty
            self.pred = pred
            self.heuristic_cost = heuristic_cost
            self.t_cost = t_cost
            self.f_cost = None

    node_list = list()
    for i in city_list:
        x = node(i)
        node_list.append(x)

    # supply heuristic value #
    open = list()
    open.append(car_s.dest.num)
    node_list[car_s.dest.num].heuristic_cost = 0
    while len(open) != 0:
        i = open.popen(0)
        for j in range(len(city_list[i].distance)):
            if city_list[i].distance[j] is not None:
                if node_list[j].heuristic_cost is None:
                    node_list[j].heuristic_cost = city_list[i].distance[j] + node_list[i].heuristic_cost
                    open.append(j)
                elif node_list[j].heuristic_cost > (city_list[i].distance[j] + node_list[i].heuristic_cost):
                    node_list[j].heuristic_cost = city_list[i].distance[j] + node_list[i].heuristic_cost
                    open.append(j)
    # heuristic calculation done... # Although, there are various heuristic algorithms such as IDS, A*. We chose A*
    # path traversal algorithm which takes heuristic cost and optimal cost. A* algorithm search #
    closed = list()
    opened = list()
    opened.append(car_s.src.num)
    node_list[car_s.src.num].t_cost = 0
    node_list[car_s.src.num].f_cost = node_list[car_s.src.num].heuristic_cost
    while len(opened) != 0:
        i = opened.popen(0)
        if i == car_s.dest.num:
            # terminate
            break
        for j in range(len(city_list[i].distance)):
            if city_list[i].distance[j] is not None and city_list[i].distance[j] != 0 and city_list[i].distance[j] <= (
                    (car_s.max_cap * car_s.avg_speed) / car_s.discrg_rate):
                cost = (city_list[i].distance[j] / car_s.avg_speed) * (1 + (car_s.discrg_rate / car_s.crg_rate))
                g = cost + (node_list[j].heuristic_cost / car_s.avg_speed)
                if j not in opened and j not in closed:
                    node_list[j].t_cost = cost + node_list[i].t_cost
                    node_list[j].f_cost = node_list[i].t_cost + g
                    node_list[j].pred = i
                    opened.append(j)
                elif j in opened:
                    if node_list[j].t_cost > cost + node_list[i].t_cost:
                        node_list[j].t_cost = cost + node_list[i].t_cost
                        node_list[j].f_cost = node_list[i].t_cost + g
                        node_list[j].pred = i

    # A* search completed... optimal path found #

    # path finding
    path = list()
    i = car_s.dest.num
    while i == car_s.src.num:
        path.insert(0, i)
        i = node_list[i].pred
    path.insert(0, i)
    car_s.path = path
    # ....path found

    # travel and charging time calculated
    travel_time = 0
    crg_time = 0
    for i in range(len(path) - 1):
        di = city_list[path[i]].distance[path[i + 1]]
        cost_crg = (di / car_s.avg_speed) * car_s.discrg_rate
        crg_time += cost_crg / car_s.crg_rate
        travel_time += (di / car_s.avg_speed)
    if crg_time * car_s.crg_rate < car_s.init_chrg:
        crg_time = 0
    else:
        crg_time = crg_time - (car_s.init_chrg / car_s.crg_rate)

    car_s.tot_time = travel_time + crg_time

    return car_s


if __name__ == '__main__':
    n = int(input('Enter number of cars'))
    m = int(input('Enter number of cities'))
    city_list = list()
    car_list = list()
    distance_matrix = [[None] * m] * m
    # Taking the inputs of all the properties
    for i in range(m):
        for j in range(i, m):
            if i == j:
                distance_matrix[i][j] = 0
                distance_matrix[j][i] = 0
            else:
                distance_matrix[i][j] = float(
                    input('Enter distance between city ' + str(i) + ' and ' + str(j) + ' : '))
                distance_matrix[j][i] = distance_matrix[i][j]
    for i in range(m):
        v = city(i, distance_matrix[i])
        city_list.append(v)
    for i in range(n):
        sr = int(input('Enter the source city of car number: ' + str(i)))
        de = int(input('Enter the destination city of car number: ' + str(i)))
        b = float(input('Enter the initial charge:'))
        d = float(input('Enter the discharge rate:'))
        max_b = float(input('Enter the maximum charge capacity:'))
        crg_r = float(input('Enter the charge rate of the car:'))
        avg_s = float(input('Enter the average speed of the car:'))
        car_s = car(city_list[sr], city_list[de], b, d, max_b, avg_s, crg_r)
        car_list.append(car_s)
    for i in range(len(car_list)):
        car_list[i] = path_plot(car_list[i], city_list)

    print('The following are the paths of each car:')
    for i in range(len(car_list)):
        print(i, ':', car_list[i].path)
