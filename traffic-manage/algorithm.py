import traffic_collect_data as tcd
from turtle import Turtle, Screen
import time

road1 = tcd.get_dict(1)
road2 = tcd.get_dict(2)
road3 = tcd.get_dict(3)
road4 = tcd.get_dict(4)
roads = [road1, road2, road3, road4]

print("Starting...")

def get_roads(order=["1", "2", "3", "4"]):
    """Returns a list of roads"""
    road1 = tcd.get_dict(1)
    road2 = tcd.get_dict(2)
    road3 = tcd.get_dict(3)
    road4 = tcd.get_dict(4)
    roadss = [road1, road2, road3, road4]
    roads = ["road1", "road2", "road3", "road4"]
    roads_updated = []
    for i, r in enumerate(order):
        for ind, road in enumerate(roads):
            if r in road:
                roads_updated.append(roadss[ind])
                break
    return roads_updated

def lighting_set(sec, road_no):
    """Sets timer in the desktop"""
    writer = Turtle()
    road_no_writer = Turtle()
    screen = Screen()
    writer.hideturtle()
    writer.color('black')
    writer.penup()
    road_no_writer.hideturtle()
    road_no_writer.color('black')
    road_no_writer.penup()
    style = ("Courier",30,'bold')
    writer.setposition(0,100)
    road_no_writer.setposition(0,50)
    screen.title("Timer")
    screen.setup(width=800, height=600, startx=100, starty=100)
    for i in range(sec, 0, -1):
        writer.clear()
        writer.write(i, font=style, align='center')
        road_no_writer.write(road_no, font=style, align='center')
        time.sleep(1)
    screen.clearscreen()

def close_leds(roads):
    """Closes the LEDs"""
    for i, r in enumerate(roads):
        r["Red led"].off()
        r["Green led"].off()
        r["Red led"].close()
        r["Green led"].close()

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

def light_set(roads, now_road):
    """Sets the lighting for the roads"""
    for r, i in enumerate(roads):
        roads[r]["Red led"].on()
        roads[r]["Green led"].off()
    roads[now_road]["Green led"].on()
    roads[now_road]["Red led"].off()

def get_order_lights():
    """Returns the order of roads which should be given green light"""
    global roads
    order = []
    locked = []
    unlocked = {}
    now_road = 0
    for k, road in enumerate(roads):
        if not k == 0:
            close_leds(roads)
            roads = get_roads()
        unlocked = set_unlocked(locked, roads)
        max_road = max_dict_in_dict(unlocked)
        now_road = find_now_road_index(max_road, roads)
        order.append(f"road" + str(now_road + 1))
        locked.append(now_road)
        print("\nGreen light given to road", str(now_road + 1) + ".\n")
        light_set(roads, now_road)
        lighting_set(roads[now_road]["Green light time"], "Road: " + str(now_road + 1))
        print("---------------------")

    close_leds(roads)
    return order

def string2list(order_list_str):
    """Returns a list with the variables specified."""
    order_list = []
    for key, string in enumerate(order_list_str):
        if "1" in string:
            order_list.append("1")
        elif "2" in string:
            order_list.append("2")
        elif "3" in string:
            order_list.append("3")
        elif "4" in string:
            order_list.append("4")

    return order_list

order = get_order_lights()
order = string2list(order)

try:
    while True:
        lists = get_roads(order=order)
        for i, r in enumerate(lists):
            if not i == 0:
                close_leds(lists)
                lists = get_roads(order=order)
            light_set(lists, i)
            print("\nGreen light given to road", str(int(order[i])) + ".\n")
            lighting_set(r["Green light time"], "Road: " + str(int(order[i])))
            print("---------------------")
        close_leds(lists)
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    close_leds(lists)
