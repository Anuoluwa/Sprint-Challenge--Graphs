from room import Room
from player import Player
from world import World
from utility import Graph, Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


traversalPath = [] #populate with n/s/e/w
# make a visited rooms set
visited = set()
# add room 0 to visited rooms
visited.add(0)
# function to traverse graph
# checks if any room around hasn't been seen
def checkRooms(currentRoomID):
    for any_room in room_graph[currentRoomID][1].values():
        if any_room not in visited:
            return False
    return True

# function to track unvisited rooms
# goes into first unseen room around after traversing a path
def trackNewRooms(currentRoomID):
    for direction, any_room in room_graph[currentRoomID][1].items():
        if any_room not in visited:
            visited.add(any_room)
            traversalPath.append(direction)
            return any_room
    print('No way!!')

# function to get directions
def directionToRoom(currentRoom, room):
    for path, location in room_graph[currentRoom][1].items():
        if location == room:
            return path
    return None

# function to step back to previous rooms
def stepBackToPrev():
    q = Queue()
    visitedRoom = set()
    path = {}
    q.enqueue(currentRoom)
    path[currentRoom] = [currentRoom]
    while q.size() > 0:
        roomID = q.dequeue()
        visitedRoom.add(roomID)
        for traversedRoom in room_graph[roomID][1].values():
            if traversedRoom in visitedRoom:
                continue
            newPath = list(path[roomID])
            newPath.append(traversedRoom)
            path[traversedRoom] = newPath
            if not checkRooms(traversedRoom):
                actualPath = path[traversedRoom]
                direction = []
                for i in range(len(actualPath) - 1):
                    direction.append(directionToRoom(actualPath[i], actualPath[i + 1]))
                return (direction, actualPath[len(actualPath) - 1])
            q.enqueue(traversedRoom)
    return None
# traverse rooms using dft starting from room 0
currentRoom = 0
while True:
    while not checkRooms(currentRoom):
        currentRoom = trackNewRooms(currentRoom)
        # mark every room as seen_room
        # add it to traversal path

    # if no more rooms, loop back to the first room with other unseen rooms
    # use bfs to get from the dead end to the room with unexplored rooms if we can
    # mark every room it went throught as seen
    prevRoom = stepBackToPrev()
    # get (directions it went back through, destination room) or None
    # if can't trace back, don't add to path
    if prevRoom:
        newPath = prevRoom[0]
        traversalPath.extend(newPath)
        currentRoom = prevRoom[1]
    else:
        break


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
