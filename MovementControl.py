from pynput.mouse import Controller
import easingFunctions

class MovementControl:
    def __init__(self, smoothing_factor=0.1, scaling_factor=0.1, friction_coefficient=0.85, easing_function=easingFunctions.ease_in_out_quad):
        self.mouse = Controller()
        self.velocity = 0
        self.smoothing_factor = smoothing_factor
        self.scaling_factor = scaling_factor
        self.friction_coefficient = friction_coefficient
        self.easing_function = easing_function

    def apply_inertia(self):
        self.velocity *= self.friction_coefficient

    def apply_easing(self, value):
        return self.easing_function(value * self.smoothing_factor)

    def reset(self):
        self.velocity = 0
