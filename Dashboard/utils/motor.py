motor_state = False

def change_motor_state(state):
    global motor_state
    if motor_state != state:
        motor_state = state