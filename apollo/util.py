import math
import networkx as nx

class Vector2:
    """
    Vector2 class from pyth_example provided by https://github.com/RLBot/RLBotPythonExample
    
    Attributes:
        x (float): x coordinate 
        y (float): y coordinate 
    """
    def __init__(self, x=0, y=0):
        """
        The constructor for Vector2 class
        
        Parameters:
            x (float): x coordinate 
            y (float): y coordinate 
        """
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        """Overrides '+' for adding two Vector2s"""
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        """Overrides '-' for adding two Vector2s"""
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        """
        Corrects a Vector2 to another Vector2
        
        Parameters:
            ideal (Vector2): desired Vector2 to correct to
            
        Returns:
            correction (float): correction in radians
        """
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction
    
class Vector3:
    """
    Vector3 class for storing 3 values
    
        Attributes:
        x (float): x coordinate 
        y (float): y coordinate 
        z (float): z coordinate 
    """
    def __init__(self, x=0, y=0, z=0):
        """
        The constructor for Vector# class
        
        Parameters:
            x (float): x coordinate 
            y (float): y coordinate 
            z (float): z coordinate 
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, val):
        """Overrides '+' for adding two Vector3s"""
        return Vector3(self.x + val.x, self.y + val.y, self.z + val.z)

    def __sub__(self, val):
        """Overrides '-' for adding two Vector3s"""
        return Vector3(self.x - val.x, self.y - val.y, self.z - val.z)
    
    def __len__(self):
        """Overrides len(Vector3) to return the magnitude of Vector3"""
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
    
    @staticmethod
    def dot(first_vec3, second_vec3):
        """Returns the dot product between two Vector3 that is a float"""
        return first_vec3.x * second_vec3.x + first_vec3.y * second_vec3.y + first_vec3.z * second_vec3.z
    
    @staticmethod
    def cross(first_vec3, second_vec3):
        """Returns the cross product between two Vector3"""
        return Vector3(first_vec3.y * second_vec3.z - first_vec3.z * second_vec3.y, first_vec3.z * second_vec3.x - first_vec3.x * second_vec3.z, first_vec3.x * second_vec3.y - first_vec3.y * second_vec3.x)
    
    @staticmethod
    def normalize(vec3):
        """Returns normalized Vector3 and makes its magnitude equal to 1"""
        return Vector3(vec3.x/len(vec3), vec3.y/len(vec3), vec3.y/len(vec3))
    
    @staticmethod
    def distance_between(first_vec3, second_vec3):
        """Returns the distance between two Vector3s"""
        return math.sqrt(math.pow((first_vec3self.x - second_vec3.x), 2) + math.pow((first_vec3.y - second_vec3.y), 2) + math.pow((first_vec3.z - second_vec3.z), 2))
    
class Boostpad:
    """
    Struct for boostpads
    
        Attributes:
        location (Vector3): global location 
        is_full_boost (bool): if True, is 100% boost refill with ~10 second cooldown, else 12% boost refill with ~5 second cooldown
        is_active (bool): if True, can get boost, else boost not available
        timer (float): cooldown timer
        id: identification number for building boost graph
    """
    def __init__(self, location=Vector3(0,0,0), is_full_boost=False, is_active=True, timer=float(0), id):
        """
        The constructor for Vector2 class
        
        Parameters:
            location (Vector3): global location 
            is_full_boost (bool): if True, is 100% boost refill with ~10 second cooldown, else 12% boost refill with ~5 second cooldown
            is_active (bool): if True, can get boost, else boost not available
            timer (float): cooldown timer
            id: identification number for building boost graph
        """
        self.location = Vector3(location.x, location.y, location.z)
        self.is_full_boost = bool(is_full_boost)
        self.is_active = bool(is_active)
        self.timer = float(timer)
        self.id = id

def dijkstra_path(starting_location, ending_location, boost_pads):
    """
    Calculates the dot product of itself to another Vector3
        
    Parameters:
        starting_location (Vector3): starting location
        ending_location (Vector3): ending location
        nodes (array): nodes of graph 
            
    Returns:
        array: path of nodes to follow between locations
    """
    #build graph
    graph = nx.Graph()
    start = Boostpad(starting_location, False, False, 0.0,'start')
    end = Boostpad(ending_location, False, False, 0.0,'end')
    boost_pads.insert(0, start)
    boost_pads.append(end)
    #connect all locations with an edge
    for i in range(0, boost_pads.len()):
        for j in range(0, boost_pads.len()):
            if boost_pads[i].id !=  boost_pads[j].id:
                graph.add_edge([boost_pads[i].id, boost_pads[j].id])
    return nx.dijkstra_path(graph, 'start', 'end')