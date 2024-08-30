from MovementControl import MovementControl
import easingFunctions


class Scroll(MovementControl):
    def __init__(self, smoothing_factor=0.1, scroll_scaling=5, friction_coefficient=0.85, easing_function=easingFunctions.ease_in_out_quad):
        super().__init__(smoothing_factor, scroll_scaling, friction_coefficient, easing_function)

    def update_scroll(self, scroll_amount):
        self.velocity += scroll_amount * self.scaling_factor
        self.apply_inertia()
        smoothed_scroll = self.apply_easing(self.velocity)
        self.mouse.scroll(0, -smoothed_scroll)
