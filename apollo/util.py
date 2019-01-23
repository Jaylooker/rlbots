import math
'''
Vector2 class from pyth_example provided by https://github.com/RLBot/RLBotPythonExample
'''
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
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
    
'''
Vector3 class for storing 3 values
'''
class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, val):
        return Vector3(self.x + val.x, self.y + val.y, self.z + val.z)

    def __sub__(self, val):
        return Vector3(self.x - val.x, self.y - val.y, self.z - val.z)
    
'''
Struct for boostpads
'''
class Boostpad:
    def __init__(self, location=Vector3(0,0,0), is_full_boost=False, is_active=True, timer=float(0)):
        self.location = Vector3(location.x, location.y, location.z)
        self.is_full_boost = bool(is_full_boost)
        self.is_active = bool(is_active)
        self.timer = float(timer)

