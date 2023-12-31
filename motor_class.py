#!/usr/bin/python3
from gpiozero import OutputDevice
import time


class StepperMotor():
    def __init__(self, motor_pins: list, step_sleep = 0.002) -> None:
        '''
        Class for controlling a stepper motor
        
        Parameters:
        - motor_pins (gpiozero.OutputDevice list): A list containing the 4 output pins to the stepper motor. Example: [in1, in2, in3, in4]
        - step_sleep (int): The time, in seconds, to sleep between motor steps. Be careful lowering this too much, at some point you run into the mechanical limitation of how quick the motor can move. Default = 0.002
        '''
        
        self.motor_pins = motor_pins
        self.step_sleep = step_sleep
        
        # Defining stepper motor sequence (Found in documentation <http://www.4tronix.co.uk/arduino/Stepper-Motors.php>)
        self.step_sequence = [[0,0,0,1],
                              [0,0,1,1],
                              [0,0,1,0],
                              [0,1,1,0],
                              [0,1,0,0],
                              [1,1,0,0],
                              [1,0,0,0],
                              [1,0,0,1]]
        self.motor_step_counter = 0 # Used to keep count of where the motor is located in the step_sequence


    def stop(self) -> None:
        ''' Helper function for turning all pins off'''
        for pin in self.motor_pins:
            pin.off()


    def step_motor(self, step_count: int, direction: bool) -> None:
        '''
        Step motor the given number of steps in the given direction
        
        Parameters:
        - step_count (int): Number of steps the motor should perform
        - direction (bool): True for clockwise rotation, false for counter-clockwise rotation
        '''
        
        try:
            for _ in range(step_count):
                for pin, value in zip(self.motor_pins, self.step_sequence[self.motor_step_counter]):
                    pin.value = value
                if direction:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                else:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                time.sleep(self.step_sleep)
                
        except KeyboardInterrupt:
            self.stop()
            exit(1)


def main():
    # Define motor output pins
    in1 = OutputDevice(16)
    in2 = OutputDevice(19)
    in3 = OutputDevice(20)
    in4 = OutputDevice(26)
    
    # Initialize motor
    motor = StepperMotor([in1, in2, in3, in4])
    
    # Run motor half a rotation 
    motor.step_motor(int(4096/2), True)
    time.sleep(1)
    motor.step_motor(int(4096/2), False)
    
    
    motor.stop()
    print("Execution finished, exiting...")
    exit()



if __name__ == "__main__":
    main()