from .devices import devices
from . import Motor
import time



class Linear(Motor):
    
    def __init__(self, controller, address='0', debug=True, inverted=False):
        # Patch parent object - elliptec.Motor(port, baud, bytesize, parity)
        super().__init__(controller=controller, address=address, debug=debug)
        
    
    ## Setting and getting positions
    def get_distance(self):
        ''' Finds at which distance the stage is at the moment. '''
        status = self.get('position')
        distance = self.extract_distance_from_status(status)
        return distance
    
    def set_distance(self, distance):
        ''' Moves to a particular distance. '''
        distance = distance+0.0047
        position = self.dist_to_pos(distance)
        status,t1 = self.move('absolute', (position))
        distance = self.extract_distance_from_status(status)
        return distance,t1

    def shift_distance(self, distance):
        if distance < 0 and abs(distance)<0.03:
            distance = (distance - 0.002)
        elif distance < 0:
            distance = (distance - 0.002)
        elif distance > 0 and abs(distance)<1:
            distance = (distance + 0.005)

        position = self.dist_to_pos(distance)
        status,t1 = self.move('relative', position)
        distance = self.extract_distance_from_status(status)
        return distance,t1

    def jog(self, direction="forward"):
        if direction in ["backward", "forward"]:
            status,t1 = self.move(direction)
            position = self.extract_distance_from_status(status)
            return position
        else:
            return None

    # Home set/get
    def get_home_offset(self):
        status = self.get('home_offset')
        distance = self.extract_distance_from_status(status)
        return distance

    def set_home_offset(self, offset):
        position = self.dist_to_pos(offset)
        status = self.set('home_offset', position)
        return status

    # Jog step
    def get_jog_step(self):
        status = self.get('stepsize')
        distance = self.extract_distance_from_status(status)
        return distance

    def set_jog_step(self, distance):
        ''' Sets jog step to a particular distance (in millimeters). '''
        position = self.dist_to_pos(distance)
        status = self.set('stepsize', position)
        return status

    def set_velocity(self,velocity):
        velocity *= 16**6
        status = self.set('velocity',velocity)
        return status
    
    def get_velocity(self):
        status = int(self.get('velocity')[2],16)
        return status
    
    # TODO: clean(self)
    # TODO: clean_and_optimize(self)

    # Helper functions
    def extract_distance_from_status(self, status):
        # If status is telling us current position
        if status:
            if status[1] in ['PO', 'HO', 'GJ']:
                position = status[2]
                distance = self.pos_to_dist(position)
                return distance
       
        return None

    def pos_to_dist(self, position):
        ''' Converts position in pulses to distance in millimeters. '''
        pulse_range = self.pulse_per_rev * self.range
        distance = position/pulse_range * self.range
        distance_rounded = round(distance, 4)
        return distance_rounded
        
    def dist_to_pos(self, distance):
        ''' Converts distance in millimeters to position in pulses. '''
        pulse_range = self.pulse_per_rev * self.range
        position = int(distance/self.range * pulse_range)
        return position
