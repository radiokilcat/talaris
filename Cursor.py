import time
from MovementControl import MovementControl
import easingFunctions

class Cursor(MovementControl):
    def __init__(self, smoothing_factor=0.1, scaling_factor=0.05, friction_coefficient=0.85, easing_function=easingFunctions.ease_in_out_quad):
        super().__init__(smoothing_factor, scaling_factor, friction_coefficient, easing_function)
        self.prev_time = time.time()
        self.prev_position = None
        self.smoothed_position = None
        self.noise_threshold = 50

    def calculate_velocity(self, current_pos):
        current_time = time.time()
        dt = current_time - self.prev_time
        self.prev_time = current_time

        if dt < 1e-6:  # 1e-6 is a small number close to zero
            dt = 1e-6
            
        if self.prev_position is None:
            self.prev_position = current_pos
            self.smoothed_position = current_pos
            return 0, 0

        ### float division by zero
        vx = (current_pos[0] - self.prev_position[0]) / dt
        vy = (current_pos[1] - self.prev_position[1]) / dt

        if abs(vx) < self.noise_threshold:
            vx = 0
        if abs(vy) < self.noise_threshold:
            vy = 0

        vx *= self.scaling_factor
        vy *= self.scaling_factor
        print(f"smoothed1: {self.smoothed_position}")
        # Smoothing: Update smoothed position
        self.smoothed_position = (
            self.smoothed_position[0] * (1 - self.smoothing_factor) + vx * self.smoothing_factor,
            self.smoothed_position[1] * (1 - self.smoothing_factor) + vy * self.smoothing_factor
        )
        print(f"smoothed2: {self.smoothed_position}")
        print(f"vx: {vx}, vy: {vy}")

        smoothed_vx = self.smoothed_position[0]
        smoothed_vy = self.smoothed_position[1]

        self.prev_position = current_pos
        return smoothed_vx, smoothed_vy

    def update_position(self, current_pos):
        vx, vy = self.calculate_velocity(current_pos)

        # self.apply_inertia()

        # smoothed_vx = self.apply_easing(vx)
        # smoothed_vy = self.apply_easing(vy)
        # if self.smoothed_position is None:
        #     self.smoothed_position = current_pos
        # else:
        #     self.smoothed_position = (
        #         self.smoothed_position[0] * (1 - self.smoothing_factor) + current_pos[0] * self.smoothing_factor,
        #         self.smoothed_position[1] * (1 - self.smoothing_factor) + current_pos[1] * self.smoothing_factor
        #     )

        # self.mouse.move(smoothed_vx, smoothed_vy)
        # print(f"smoothed: {self.smoothed_position}")
        print(f"vx set move : {vx}, vy set move: {vy}")
        self.mouse.move(vx, vy)
