import Vector2
import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

rlbotversion = 0

'''
Bot class that controls all bot action and inherits from BaseAgent
'''
class Apollo(BaseAgent):
    
    #Runs once before bots starts up
    def intialize_agent:
        self.controller_state = SimpleControllerState()
        
    '''
    Recieves game packet and controls what action the bot will take
    Returns what state the bot shoulf be in
    '''
    def get_outout(self, packet: GameTickPacket) -> SimpleControllerState:
        
        #Ball details
        ball_location = Vector2(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)
        
        #My car details 
        my_car = packet.game_cars[self.index]
        my_car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        my_direction = get_car_facing_vector(my_car)
        
        car_to_ball = my_car_location - ball_location
        
        #actions
        ball_chase(self, my_car_location, ball_location)
        
        #debug
        draw_debug(self.renderer, my_car, packet.game_ball, action_display)
        
        return self.controller_state
    
    
    #helper functions
    
    #Ball chase
    def ball_chase(self, my_location, ball_location):
        # Point towards ball
        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
            action_display = "turn left"
        else:
            turn = 1.0
            action_display = "turn right"
        self.controller.steer = turn
        
        # Go towards ball
        
        #throttle at %100 
        self.controller.state.throttle = 1.0
        
    
    #Returns vector of car
    def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)

    #Draws lines for debug purposes
    def draw_debug(renderer, car, ball, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.end_rendering()

        