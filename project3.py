

def display_stations(metro_location):
    """
    :param metro_location: dictionary of all metro location
    :return: displays all stations
    """
    for i in metro_location:
        print(f'\t{i}')



def display_trains(metro_trains):
    """

    :param metro_trains: dictionary of all trains
    :return: displays all trains
    """
    for i in metro_trains:
        print(f'*** Information for Train {metro_trains[i]["train_print"][0]} ***')
        print(f'\tLine : {i}')
        print(f'\tCurrent Position : {metro_trains[i]["trains"][0]} ')





def connect_stations(metro_location, to_connect):
    """
    :param metro_location: dictionary of all metro location
    :param to_connect: splitted user command
    :return: adds connections of stations in dictionary
    """
    loc_1 = to_connect[2]
    loc_2 = to_connect[3]
    metro_location[loc_1]['connections'].append(loc_2)
    metro_location[loc_2]['connections'].append(loc_1)



def create_trains(metro_trains, command):
    """

    :param metro_trains:dictionary of all trains
    :param command: user command used to get name of train
    :return: adds train name and line in dictionary
    """
    line = command[3]
    train = command[4]
    metro_trains[line]["trains"].append(train)
    metro_trains[line]["train_print"].append(command[2])



def train_check(connect_list, command):
    """

    :param connect_list: list of lines
    :param command: user command splitted
    :return: boolean values
    """
    if command[3] in connect_list:
        return True
    else:
        if len(command) != 5:
            print("Invalid command")
        else:
            print("There is no connection between the stations, Enter command again.")
        return False


def plan_trip(metro_location, current, end_location):  #recursive function
    """
    :param metro_location: dictionary of all metro location
    :param current: current metro station
    :param end_location: final metro station
    :return: displays trip planned
    """
    if current == end_location:
        return [end_location]    #base case of recursion

    metro_location[current]['visited'] = True

    for new_place in metro_location[current]['connections']:
        if not metro_location[new_place]['visited']:
            trip_plan = plan_trip(metro_location, new_place, end_location)
            if trip_plan:
                return [current] + trip_plan
    return []



def main_plan_trip(metro_location, current, end_location, connections):
    """

    :param metro_location:  dictionary of metro locations
    :param current: current station
    :param end_location: station to reach
    :param connections: list of connected stations
    :return: prints the trip planned from initial to final station
    """
    station_list = plan_trip(metro_location, current, end_location)
    # print(station_list)
    new_list = []
    for i in connections:
        if i[0] in station_list:
            new_list.append(i)

    print(f'Start on the {new_list[0]} --> {" --> ".join(station_list)}')


def step(metro_trains, metro_location):
    """
    :param metro_trains: disctionary of trains and their position with line
    :return: trains moving from one station to other
    """
    a = -1
    for i in metro_trains:
        initial_pos = metro_trains[i]["trains"][0]
        for j in metro_location:
            if j == initial_pos:
                final_pos = metro_location[j]["connections"][a]
                print(f'{metro_trains[i]["train_print"][0]} has moved from {initial_pos} to {final_pos}')
                metro_trains[i]["trains"][0] = final_pos    #updating train position




def reset_visited(locations):
    """
    :param locations: dictionary of all metro location
    :return: updtes values of visited in dictionary
    """
    for place in locations:
        locations[place]['visited'] = False    #resatating false value in dictionary of metro locations

def metro_system():
    """
    :return: main metro function
    """
    metro_name = input(">>>")
    metro_location = {}
    metro_trains = {}
    connection_list  = []

    user_command = input(f'[{metro_name}] >>> ')
    while user_command != 'exit':     #input validation to end the program if its "exit"
        split_command = user_command.split()
        # print(split_command)
        if not split_command:    #checking if user input is empty
            print("Empty, Enter again")
            pass

        elif split_command[0].lower() == "create" and split_command[1].lower() == "station":
            metro_location[split_command[2]] = {'connections': [], 'visited': False}     #adding station


        elif split_command[0].lower() == "create" and split_command[1].lower() == "train":    #create train
            if train_check(connection_list, split_command):
                metro_trains[split_command[3]] = {"trains" : [], "train_print" : [] }
                create_trains(metro_trains, split_command)       #adding train
            else:
                pass



        elif split_command[0].lower() == "connect" and split_command[1].lower() == "stations":    #connect train
            if split_command[2] in metro_location and split_command[3] in metro_location:
                if split_command[4] not in connection_list:
                    connection_list.append(split_command[4])
                connect_stations(metro_location, split_command)        #calling function to connect stations
            else:
                pass


        elif split_command[0].lower() == "plan":
            if split_command[2] in metro_location and split_command[3] in metro_location:
                loc_1 = split_command[2]
                loc_2 = split_command[3]
                reset_visited(metro_location)
                main_plan_trip(metro_location, loc_1, loc_2, connection_list)  #plan trip recursive function
                reset_visited(metro_location)
            else:
                print("There is no station to plan trip")
                pass


        elif split_command[0].lower() == "step":
            step(metro_trains, metro_location)
            pass

        elif split_command[0].lower() == "display" and split_command[1].lower() == "stations":
            display_stations(metro_location)       #displaying all stations

        elif split_command[0].lower() == "display" and split_command[1].lower() == "trains":
            display_trains(metro_trains)        #displaying all trains

        else:
            print("Enter command correctly")
            pass

        # print(metro_location)
        # print(metro_trains)

        user_command = input(f'[{metro_name}] >>> ')

if __name__ == '__main__':
    metro_system()
