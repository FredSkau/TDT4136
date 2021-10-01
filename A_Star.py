import Map
from scipy.spatial import distance


class Node:
    def __init__(self, pos, parent=None):
        """
        Defines position of the node, and it's parent if it exists.
        Declares f, g and h for later use.
        :param pos: Position of the node on the map
        :param parent: The node this Node moved from,
        used to find the shortest path once we arrive at the end node
        """
        self.pos = pos
        self.parent = parent

        self.f = self.g = self.h = 0

    def equals(self, other):
        """
        Compares positions of two nodes
        :param other: the node to compare this one to
        :return: Boolean value for whether the positions are the same or not
        """
        return self.pos == other.pos


def a_star(start, end, mp):
    """
    The main algorithm function
    :param start: Start position
    :param end: Goal position
    :param mp: The map to navigate through
    :return: The end node with parents making up the shortest path
    """
    open_nodes = []
    closed_nodes = []

    start_node = Node(start)
    end_node = Node(end)

    open_nodes.append(start_node)

    while len(open_nodes):
        """
        Loop for checking nodes in our map
        Keeps running until we either run out of nodes to check (no path can be found),
        or the end node is found and returned.

        Starts by finding the element with the lowest f and setting it as our current node
        """
        current = sorted(open_nodes, key=lambda x: x.f)[0]

        """
        Close the current node so we don't check it again
        """
        open_nodes.remove(current)
        closed_nodes.append(current)

        for move in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            """
            Check the nodes up, down, left and right of our current node
            """
            position = [current.pos[0] + move[0], current.pos[1] + move[1]]
            value = mp.get_cell_value(position)
            """
            Skip node if it isn't traversable
            """
            if value == -1:
                continue

            new_node = Node(position, current)

            """
            If our node has the same position as the end node, we have found our path
            """
            if new_node.equals(end_node):
                return new_node

            """
            Skip if the position of our node has been closed before
            """
            if new_node.pos in [c.pos for c in closed_nodes]:
                continue

            """
            Calculate g,h and f for our node
            """
            new_node.g = current.g + value
            """new_node.h = (position[0] - end_node.pos[0]) ** 2 + (position[1] - end_node.pos[1]) ** 2"""
            new_node.h = (abs(distance.euclidean(position, end_node.pos)))
            new_node.f = new_node.g + new_node.h

            """
            If the node is not already in the open nodes list,
            or is the the open nodes list but has a smaller f than it's matches,
            add it to the open nodes list.

            The position is added to our map to show how the algorithm searches
            """
            if new_node.pos in [o.pos for o in open_nodes]:
                for o in [n for n in open_nodes if n.pos == new_node.pos]:
                    if new_node.f > o.f:
                        break
                else:
                    open_nodes.append(new_node)
                    mp.set_cell_value(new_node.pos, 'p')
            else:
                open_nodes.append(new_node)
                mp.set_cell_value(new_node.pos, 'p')

"""
Loop through all maps
"""
mp = Map.Map_Obj(3)
mp.show_map()
for i in range(1, 6):
    print(i)
    floor = Map.Map_Obj(i)
    st, en, e, path = floor.fill_critical_positions(i)
    finish = a_star(st, en, floor).parent

    """
    When the final node is found, iterate through all its parents and mark them as the shortest path
    """
    while finish.parent:
        floor.set_cell_value(finish.pos, ' p ')
        finish = finish.parent
    floor.show_map()
