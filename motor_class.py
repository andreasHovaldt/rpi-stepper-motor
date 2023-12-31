#import RPi.GPIO as GPIO
from gpiozero import OutputDevice
import time

in1 = OutputDevice(16)
in2 = OutputDevice(19)
in3 = OutputDevice(20)
in4 = OutputDevice(26)
motor_pins = [in1,in2,in3,in4]

# careful lowering this, at some point you run into the mechanical limitation o>
step_sleep = 0.002

#step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360 degrees

#direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co>
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
motor_step_counter = 0

def cleanup():
    for pin in motor_pins:
        pin.off()


def step_motor(step_count: int, direction: bool):
    '''
    Step motor the given number of steps in the given direction
    
    Parameters:
    - step_count (int): Number of steps the motor should perform
    - direction (bool): True for clockwise rotation, false for counter-clockwise rotation
    '''
    
    global motor_pins, step_sleep, step_sequence, motor_step_counter
    
    try:
        for _ in range(step_count):
            for pin, value in zip(motor_pins, step_sequence[motor_step_counter]):
                pin.value = value
            if direction:
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(step_sleep)
            
    except KeyboardInterrupt:
        cleanup()
        exit(1)


def main():
    # motor_step_counter = 0
    cleanup()

    step_motor(int(4096/2), True)

    cleanup()
    exit( 0 )





if __name__ == "__main__":
    main()