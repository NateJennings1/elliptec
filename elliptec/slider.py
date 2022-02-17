from .cmd import get_, set_, mov_
from .devices import devices
from .tools import int_to_padded_hex, parse, error_check, move_check
from . import Motor

class Slider(Motor):
    
    def __init__(self, port, address='0', debug=True, inverted=False):
        # Patch parent object - elliptec.Motor(port, baud, bytesize, parity)
        super().__init__(port, address=address, debug=debug)

    ## Setting and getting slots
    def get_slot(self):
        ''' Finds at which slot the slider is at the moment. '''
        status = self.get('position')
        slot = self.extract_slot_from_status(status)
        return slot
    
    def set_slot(self, slot):
        ''' Moves the slider to a particular slot. 
        '''
        position = self.slot_to_pos(slot)
        status = self.move('absolute', (position))
        slot = self.extract_slot_from_status(status)
        return slot

    def jog(self, direction="forward"):
        if direction in ["backward", "forward"]:
            status = self.move(direction)
            slot = self.extract_slot_from_status(status)
            return slot
        else:
            return None

    # Helper functions
    def extract_slot_from_status(self, status):
        # If status is telling us current position
        if status:
            if status[0]=='PO':
                position = status[1]
                slot = self.pos_to_slot(position)
                return slot
        
        return None
        
    def pos_to_slot(self, posval):
        positions = devices[self.motor_type]['positions'] 
        if posval not in positions:
            return None
        else:    
            slot = positions.index(posval) + 1
        
    def slot_to_pos(self, slot):
        positions = devices[self.motor_type]['positions'] 
        # If slot within range
        if (slot - 1) in list(range(len(positions))):
            return positions[slot-1]


    



    










