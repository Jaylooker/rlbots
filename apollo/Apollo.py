from util import Vector2, Vector3, Boostpad, dijkstra_path
import math

#RLBOT framework verison 4
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

START_BOOST = 33.0
MAX_SPEED = 2300


class Apollo(BaseAgent):
    """
    Bot class that controls all bot action and inherits from BaseAgent
    """

    def initialize_agent(self):
        """Runs once before bots starts up"""
        #Agent
        self.controller_state = SimpleControllerState()
        self.agent_location = Vector3(0,0,0)
        self.agent_rotation = Vector3(0,0,0)
        self.agent_velocity = Vector3(0,0,0)
        self.agent_angular_velocity = Vector3(0,0,0)
        self.boost = START_BOOST
        #Ball
        self.ball_location = Vector3(0,0,0)
        self.ball_rotation = Vector3(0,0,0)
        self.ball_velocity = Vector3(0,0,0)
        self.ball_angular_velocity = Vector3(0,0,0)
        #Field Info
        self.agent_team_num = 0
        self.opponent_team_num = 0
        self.agent_goal_location = Vector3(0,0,0)
        self.opponent_goal_location = Vector3(0,0,0)
        self.boost_pads = [] 
        for i in range (self.get_field_info().num_boosts):
            boostpad = Boostpad(Vector3(self.get_field_info().boost_pads[i].location.x, self.get_field_info().boost_pads[i].location.y, self.get_field_info().boost_pads[i].location.z), self.get_field_info().boost_pads[i].is_full_boost, True, 0.0, i)
            self.boost_pads.append(boostpad)
        
    def preprocess(self, packet):
        """
        Encodes packet information into local variables and objects
        
        Parameters:
            packet (GameTickPacket): object that contains game information every tick
        """
        #Agent
        self.agent_location = Vector3(packet.game_cars[self.index].physics.location.x, packet.game_cars[self.index].physics.location.y, packet.game_cars[self.index].physics.location.z)
        self.agent_rotation = Vector3(packet.game_cars[self.index].physics.rotation.pitch, packet.game_cars[self.index].physics.rotation.yaw, packet.game_cars[self.index].physics.rotation.roll)
        self.agent_velocity = Vector3(packet.game_cars[self.index].physics.velocity.x, packet.game_cars[self.index].physics.velocity.y, packet.game_cars[self.index].physics.velocity.z)
        self.agent_angular_velocity = Vector3(packet.game_cars[self.index].physics.angular_velocity.x, packet.game_cars[self.index].physics.angular_velocity.y, packet.game_cars[self.index].physics.angular_velocity.z)
        self.boost = packet.game_cars[self.index].boost
        #Ball
        self.ball_location = Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y, packet.game_ball.physics.location.z)
        self.ball_rotation = Vector3(packet.game_ball.physics.rotation.pitch, packet.game_ball.physics.rotation.yaw, packet.game_ball.physics.rotation.roll)
        self.ball_velocity = Vector3(packet.game_ball.physics.velocity.x, packet.game_ball.physics.velocity.y, packet.packet.game_ball.physics.velocity.z)
        self.ball_angular_velocity = Vector3(packet.game_ball.physics.angular_velocity.x, packet.game_ball.physics.angular_velocity.y, packet.game_ball.physics.angular_velocity.z)
        #Field Info
        self.agent_team_num = self.team
        #opponent team
        for i in range(packet.num_cars):
            car = packet.game_cars[i]
            if car.team != self.agent_team_num:
                self.opponent_team_num = car.team
        #own goal 
        for i in range(self.field_info.num_goals):
            goal = self.field_info.goals[i]
            if goal.team_num == self.agent_team_num:
                self.agent_goal_location = Vector3(goal.location.x, goal.location.y, goal.location.z)
            elif goal.team_num == self.opponent_team_num:
                self.opponent_goal_location = Vector3(goal.location.x, goal.location.y, goal.location.z)
        
    def get_outout(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        Recieves game packet and controls what action the bot will take
        
        Parameters:
            packet (GameTickPacket): object that contains game information every tick
        
        Returns:
            state the bot should be in
        """
        self.preprocess(self, packet)
      
        #Agent details 
        # agent_vector2 = self.get_car_facing_vector(my_car)

        #actions
        self.ball_chase()
        
        #debug
        #draw_debug(self.renderer, my_car, packet.game_ball, action_taken)
        
        return self.controller_state
    
    def get_car_facing_vector(self):
        """Determines the Vector2 the car is facing"""
        pitch = self.rotation.x
        yaw = self.rotation.y

        facing_x = math.cos(pitch) * math.cos(yaw)
        facing_y = math.cos(pitch) * math.sin(yaw)

        return Vector2(facing_x, facing_y)
    
    def ball_chase(self):
        """Makes the agent chase the ball"""
        car_to_ball = self.ball_location - self.agent_location
        steer_correction_radians = self.agent_location.correction_to(car_to_ball)
        # Point towards ball
        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
        else:
            turn = 1.0
        # Go towards ball 
        self.controller.throttle = 1.0
        self.controller.steer = turn
        
    def draw_debug(renderer, car, ball, action_display):
        """Draws lines for debug purposes"""
        renderer.begin_rendering()
        # draw a line from the car to the ball
        renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
        # print the action that the bot is taking
        renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
        renderer.end_rendering()