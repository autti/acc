from .plant import Plant
from .visualize import Visualizer
import numpy as np


class Maneuver(object):

    def __init__(self, title, duration, **kwargs):
        # Was tempted to make a builder class
        self.distance_lead = kwargs.get("initial_distance_lead", 200.0)
        self.speed = kwargs.get("initial_speed", 0.0)
        self.lead_relevancy = kwargs.get("lead_relevancy", 0)

        self.grade_values = kwargs.get("grade_values", [0.0, 0.0])
        self.grade_breakpoints = kwargs.get(
            "grade_breakpoints", [0.0, duration])
        self.speed_lead_values = kwargs.get("speed_lead_values", [0.0, 0.0])
        self.speed_lead_breakpoints = kwargs.get(
            "speed_lead_values", [0.0, duration])

        self.cruise_button_presses = kwargs.get("cruise_button_presses", [])

        self.duration = duration
        self.title = title

    def evaluate(self, control=None, verbosity=0, gap=10):
        """runs the plant sim and returns (score, run_data)"""
        plant = Plant(
            lead_relevancy=self.lead_relevancy,
            speed=self.speed,
            distance_lead=self.distance_lead,
            verbosity=verbosity,
        )

        buttons_sorted = sorted(self.cruise_button_presses, key=lambda a: a[1])
        current_button = 0

        brake = 0
        gas = 0
        steer_torque = 0

        previous_state = 0 # 3 possible states(accelerating(1), not accelerating(0), braking(-1))
        neg_score = 0.
        prev_accel = 0.
        # TODO: calibrate this threshold to denote maximum discomfort allowed
        neg_score_threshold = 20.
        # TODO: calibrate this constant for scaling rate of acceleration
        accel_const = 1.

        # Initialize the Visualizer. Set animate = False to only display the plots at the end of the maneuver,
        # this will be faster than showing in real time with animate = True
        # max_speed, max_accel, max_score set the maximum for the y-axis
        # TODO: make this dynamic?
        vis = Visualizer(animate=True, max_speed=100, max_accel=100, max_score=100)

        while plant.current_time() < self.duration:
            while buttons_sorted and plant.current_time() >= buttons_sorted[0][1]:
                current_button = buttons_sorted[0][0]
                buttons_sorted = buttons_sorted[1:]
                if verbosity > 1:
                    print("current button changed to", current_button)

            grade = np.interp(plant.current_time(),
                              self.grade_breakpoints, self.grade_values)
            speed_lead = np.interp(
                plant.current_time(), self.speed_lead_breakpoints, self.speed_lead_values)

            speed, acceleration, car_in_front, steer_torque = plant.step(brake=brake,
                                                                         gas=gas,
                                                                         v_lead=speed_lead,
                                                                         cruise_buttons=current_button,
                                                                         grade=grade)

            # If the car in front reaches zero, that's a crash.
            assert car_in_front <= 0

            # TODO: Assert the gap parameter is respected during all the maneuver.

            # TODO: Assert the desired speed matches the actual speed at the end of the maneuver.

            brake, gas = control(speed, acceleration,
                                 car_in_front, min_gap, steer_torque)

            # TODO: Calculate score, for now it always returns 10.
            # It should be 0 when the car crashes and higher if it doesn't.

            if gas > 0:
                # accelerating
                new_state = 1
            elif brake > 0:
                # braking
                new_state = -1
            else:
                # not accelerating
                new_state = 0

            # getting the rate of change of acceleration
            # TODO: add division by exact time, if relevent(did not delve deep into timekeeping)
            rate_accel = acceleration - prev_accel
            prev_accel = acceleration

            # The higher the value of neg_score, worse the controller.
            # multiplication with rate_accel scales the change based on the speed of change.
            neg_score += abs((new_state - previous_state) * rate_accel * accel_const)
            previous_state = new_state

            # this updates the plots with latest state
            vis.update_data(cur_time=plant.current_time(), speed=speed, acceleration=acceleration, \
                gas_control = gas, brake_control = brake, car_in_front=car_in_front, steer_torque=steer_torque, score=neg_score)

        neg_score /= self.duration
        # this cleans up the plots for this maneuver and pauses until user presses [Enter]
        vis.show_final_plots()
        assert neg_score <= neg_score_threshold

        return
