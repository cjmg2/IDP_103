import Box_Collection
import Line_Following

#to fix = TO_QR< make it fixed, and also step fwd, try to integrate a mixture of junction and also blind forward so its more foolproof
SMALL = 5/20
OUT_OF_HOME = 20/20
OUT_OF_BAY = 10/20
STEP_FWD = 40

connections = {
    "Home": {"Yellow": 270, "Green": 90},
    "Yellow": {"Red": 270, "Home": 90},
    "Green": {"Home": 270, "Blue": 90},
    "Red": {"L_purple": 180, "Yellow": 90},
    "Blue": {"L_orange": 180, "Green": 270},
    "L_orange": {"Blue": 0, "J_L_orange": 180},
    "L_purple": {"Red": 0, "J_L_purple": 180},
    "J_L_orange": {"L_orange": 0, "Ramp": 270},
    "J_L_purple": {"L_purple": 0, "Ramp": 90},
    "Ramp": {"U_T": 0, "J_L_orange": 90, "J_L_purple": 270},
    "U_T": {"J_U_orange": 90, "Ramp": 180, "J_U_purple": 270},
    "J_U_orange": {"U_orange": 180, "U_T": 270},
    "J_U_purple": {"U_purple": 180, "U_T": 90},
    "U_orange": {"J_U_orange": 0},
    "U_purple": {"J_U_purple": 0}
    }

path_det = {
    "Home": 5,
    "Yellow": 6,
    "Green": 4,
    "Red": 7,
    "Blue": 3,
    "L_purple": 8,
    "L_orange": 2,
    "Ramp": None
}

class State:
    """
    global class containing all information about the state of the robot
    self.loc: location of the robot
    self.orien: orientation of the robot, with 0 degrees meaning the robot points towards the side of the map with the four colored loading/unloading bays
    self.destination: destination of the robot at the moment, which of the four shelf the robot will be depositing the box it is carrying
    self.bay: which exact bay, out of six, does the box belong to within each row of shelves
    self.remaining_boxes: contains the bays which still have not yet been unloaded in phase 1
    """

    def __init__(self, loc, orien):
        self.loc = loc
        self.orien = orien
        self.destination = None
        self.bay = None
        self.remaining_boxes = ["Red", "Blue", "Green", "Yellow"]

global state
state = State("Home", 180)

def mini_path_find(start, dest, min_max):
    """
    pathfinds a route from loading/unloading bay to a desired shelf by finding the shortest path.
    The shortest path is determined by the starting position, and from this the robot decides to go clockwise or anticlockwise
    """

    queue = [start]
    while start != dest:
        branches = list(connections[start].keys())
        if min_max == "min":
            start = min(branches, key = lambda branches: path_det[branches])
        elif min_max == "max":
            start = max(branches, key = lambda branches: path_det[branches])
            
        queue.append(start)
    return queue

def path_find(start, dest):
    """
    pathfinds from a loading/unlaoding bay to the desired shelf
    outputs an array with all the nodes to pass
    """

    if dest == "L_orange":
        return mini_path_find(start, dest, "min")
    elif dest == "L_purple":
        return mini_path_find(start, dest, "max")
    elif dest == "U_purple" or dest == "U_orange":
        if start == "Red" or start == "Yellow":
            queue = mini_path_find(start, "L_purple", "max")
            queue.append("J_L_purple")
        elif start == "Green" or start == "Blue":
            queue = mini_path_find(start, "L_orange", "min")
            queue.append("J_L_orange")
        else:
            raise Exception("error 2, elifs ran out")
        queue.append("Ramp")
        queue.append("U_T")
        queue.append("J_" + dest)
        queue.append(dest)
        return queue
        
    else:
        raise Exception("error 1, elifs ran out")
    



def fwd_until_junc():
    Line_Following.line_following(pickup=False, dropoff=False)

def clockwise():
    Line_Following.turn_clockwise()

def anticlockwise():
    Line_Following.turn_anticlockwise()

def load_fork():
    Box_Collection.lift_block()

def unload_fork():
    if state.destination == "U_orange" or state.destination == "U_purple":
        Box_Collection.lower_to_ground()
    elif state.destination == "L_orange" or state.destination == "L_purple":
        Box_Collection.lower_onto_rack()

def fwd_until_black():
    Line_Following.line_following(pickup=False, dropoff=True)

def fwd_until_box():
    Line_Following.line_following(pickup=True, dropoff=False)

def fwd(distance):
    Line_Following.blind_forward(distance_wanted = distance)

def is_RHS_lidar_pos():
    pass

def is_LHS_lidar_pos():
    pass

def rvs(distance):
    Line_Following.blind_reverse(distance_wanted = distance)

def read_qr():
    text = Box_Collection.get_qr_code()

    translator = {
        "A": "orange",
        "B": "purple",
        "upper": "U",
        "lower": "L"
    }

    # Split the string by commas and strip any extra spaces
    parts = [part.strip() for part in text.split(',')]

    # Extract the required parts
    rack = parts[0].split()[1]
    level = parts[1]
    position = parts[2]

    destination = translator[level.lower()] + "_" + translator[rack.upper()]
    return destination, int(position)

def count_unload_return():
    """
    counts how many bays it has moved past and turns into the desired bay.
    tells robot to unload and return back to original position
    """
    counter = 0
    if state.destination == "U_purple" or state.destination == "L_orange":
        dest_general = 7 - state.bay
    else:
        dest_general = state.bay
    while counter < dest_general:
        fwd_until_junc()
        counter += 1
    turn_unload_return(dest_general)

def execute_travel(route):
    """
    Tells the robot to move according to the route provided.
    Contains code to ignore loading bay lines on the bottom floor is the target destination is on the top floor
    """
    destination = route[-1]
    output = route.copy()
    next_node = route.pop(0)
    while route:
        current_node = next_node
        next_node = route.pop(0)
        # print(current_node, next_node)
        wanted_orien = connections[current_node][next_node]
        #clockwise is positive
        turn_angle = wanted_orien - state.orien
        if turn_angle == 90 or turn_angle == -270:
            clockwise()
            state.orien = (state.orien + 90) % 360
        elif turn_angle == -90 or turn_angle == 270:
            anticlockwise()
            state.orien = (state.orien - 90) % 360
        elif turn_angle == 180 or turn_angle == -180:
            clockwise()
            clockwise()
            state.orien = (state.orien + 180) % 360
        if {current_node, next_node} in [{"Red", "L_orange"}, {"Blue", "L_purple"}] and not destination in ["L_purple", "L_orange"]:
            for i in range(6):
                fwd_until_junc()
                fwd(SMALL)
        fwd_until_junc()
        state.loc = next_node
        print(turn_angle)
    # print("\n\n\n\n")
    return output

def return_to_color(path_fwd):
    """
    instructs the robot to move back to the colored loading/unloading bays from its current location
    """
    path_rvs = path_fwd[::-1]
    while path_rvs[-2] in ["Red", "Yellow", "Green", "Blue"]:
        print(path_rvs)
        path_rvs.pop()
    execute_travel(path_rvs)


def phase_1_find_box():
    """
    starting at either Red or Blue pointing to 0 degrees, make the robot go to the nearest bay with a box and turn to face the box
    """
    color_order = ["Red", "Yellow", "Green", "Blue"]
    if state.loc == "Red":
        i = 0
        while not state.loc in state.remaining_boxes:
            if i == 0:
                clockwise()
            fwd_until_junc()
            color_order.pop(0)
            state.loc = color_order[0]
            i += 1
        if i != 0:
            anticlockwise()

    elif state.loc == "Blue":
        color_order = color_order[::-1]
        i = 0
        while not state.loc in state.remaining_boxes:
            if i == 0:
                anticlockwise()
            fwd_until_junc()
            color_order.pop(0)
            state.loc = color_order[0]
            i += 1
        if i != 0:
            clockwise()
    else:
        raise Exception("error sth, elifs ran out")

def go_in_for_the_box_readqr():
    """
    with the bot facing the box, go straight in for the box, scan the qr code, lift the box, and move back to initial position
    """
    #edity wedity this wittle cwode bwase pwease becwause there anotwer cwode simiwar
    destination, bay = read_qr()
    fwd(SMALL)
    fwd_until_junc()
    fwd_until_box()
    load_fork()
    if state.loc == "Red" or state.loc == "Yellow":
        clockwise()
        clockwise()
    elif state.loc == "Blue" or state.loc == "Green":
        anticlockwise()
        anticlockwise()

    fwd_until_junc()
    state.orien = 180
    state.remaining_boxes.remove(state.loc)
    return destination, bay

def phase_2_detect_boxes():
    """
    moves from bay to bay, using the lidar sensor to detect whether a box is present in that bay
    """

    color_order = ["Red", "Yellow", "Green", "Blue"]
    if state.loc == "Red":
        clockwise()
        while not is_LHS_lidar_pos():
            color_order.pop(0)
            if not color_order:
                print("NO BOXES DETECTED")
                anticlockwise()
                phase_2_detect_boxes()
            fwd_until_junc()
            state.loc = color_order[0]
        anticlockwise()

    elif state.loc == "Blue":
        color_order = color_order[::-1]
        anticlockwise()
        while not is_RHS_lidar_pos():
            color_order.pop(0)
            if not color_order:
                print("NO BOXES DETECTED")
                anticlockwise()
                phase_2_detect_boxes()
            fwd_until_junc()
            state.loc = color_order[0]
        clockwise()
    else:
        raise Exception("error sth, elifs ran out")


def turn_unload_return(bay):
    """
    Instructs the robot to turn, move towards the shelf, unload and return to the initial position
    """
    
    if state.destination == "U_purple" or state.destination == "L_orange":
        clockwise()
    elif state.destination == "L_purple" or state.destination == "U_orange":
        anticlockwise()
    else:
        raise Exception("error 3, elifs ran out")
    fwd_until_black()
    unload_fork()

    rvs(OUT_OF_BAY)
    clockwise()
    clockwise()
    fwd_until_junc()
    if state.destination == "U_purple" or state.destination == "L_orange":
        anticlockwise()
    elif state.destination == "L_purple" or state.destination == "U_orange":
        clockwise()
    else:
        raise Exception("error 3, elifs ran out")
    state.orien = 0
    if bay != 1:
        for i in range(bay-1):
            fwd_until_junc()
    fwd(SMALL)
    #this is a very fragile part of the code, the bot has to turn quite accurately

def start_at_yellow():
    """
    Instructs the robot to move from home to yellow, the first loading bay
    """

    fwd(OUT_OF_HOME)
    fwd_until_junc()
    clockwise()
    fwd_until_junc()
    clockwise()
    state.loc = "Yellow"
    state.orien = 0


def main():
    """
    Runs the entire program, telling the robot to do phase 1 (boxes in all 4 bays)
    then phase 2 (boxes only added one by one to a random loading bay)
    """
    Box_Collection.initalise_servo()
    for q in range(4):
        if q == 0:
            start_at_yellow()
        else:
            return 0
            phase_1_find_box()
        state.destination, state.bay = go_in_for_the_box_readqr()
        route = path_find(state.loc, state.destination)
        route = execute_travel(route)
        count_unload_return()
        return_to_color(route)
        

    for p in range(90):
        phase_2_detect_boxes()
        state.destination, state.bay = go_in_for_the_box_readqr()
        route = path_find(state.loc, state.destination)
        route = execute_travel(route)
        count_unload_return()
        return_to_color(route)

main()
    