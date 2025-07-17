import random_dict_generator as rdg
import time

road1 = rdg.rand_dict_creator()
road2 = rdg.rand_dict_creator()
road3 = rdg.rand_dict_creator()
road4 = rdg.rand_dict_creator()
roads = [road1, road2, road3, road4]

print(*roads, sep="\n", end="\n")
print("\n-----------------------------\n")

def get_roads():
    """Returns a list of roads"""
    road1 = rdg.rand_dict_creator()
    road2 = rdg.rand_dict_creator()
    road3 = rdg.rand_dict_creator()
    road4 = rdg.rand_dict_creator()
    roads = [road1, road2, road3, road4]
    return roads

def set_unlocked(locked, roads):
    """Returns a list with the items not in locked"""
    unlocked = []
    for i, r in enumerate(roads):
        if i not in locked:
            unlocked.append(r)
    return unlocked

def find_now_road_index(max_road, roads):
    """Returns an integer index of roads which is max_road"""
    for r in range(len(roads)):
        if roads[r] == max_road:
            return r

def unlocked2unlocked_time(unlocked):
    """Returns a list with the green light time in unlocked"""
    unlocked_time = []
    for dict_unlocked in unlocked:
        unlocked_time.append(dict_unlocked["Green light time"])
    return unlocked_time

def max_dict_in_dict(roads):
    """Returns a dict which has max number of green light time"""
    max_road = []
    for i, road in enumerate(roads):
        max_road.append(road["Green light time"])
    max_road = max(max_road)
    for road in roads:
        if max_road == road["Green light time"]:
            max_road = road
            break
    return max_road

def get_order_lights():
    """Returns the order of roads which should be given green light"""
    global roads
    order = []
    locked = []
    unlocked = {}
    now_road = 0
    for road in roads:
        roads = get_roads()
        unlocked = set_unlocked(locked, roads)
        print("\n")
        print(*unlocked, sep="\n", end="\n")
        max_road = max_dict_in_dict(unlocked)
        print("\n")
        print(max_road)
        now_road = find_now_road_index(max_road, roads)
        order.append(f"road" + str(now_road + 1))
        locked.append(now_road)
        print("Green light given to road", str(now_road + 1) + ".\n")
        print("---------------------")

    return order

def string2list(order_list_str):
    """Returns a list with the variables specified."""
    order_list = []
    for key, string in enumerate(order_list_str):
        if "1" in string:
            order_list.append(1)
        elif "2" in string:
            order_list.append(2)
        elif "3" in string:
            order_list.append(3)
        elif "4" in string:
            order_list.append(4)

    return order_list

order = get_order_lights()
print(*order, sep="\n", end="\n")
order = string2list(order)
print(*order, sep="\n")