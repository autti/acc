from .plant import Plant
from .visualize import Visualizer
import numpy as np


class CV:
    MPH_TO_MS = 1.609 / 3.6
    MS_TO_MPH = 3.6 / 1.609
    KPH_TO_MS = 1. / 3.6
    MS_TO_KPH = 3.6
    MPH_TO_KPH = 1.609
    KPH_TO_MPH = 1. / 1.609
    KNOTS_TO_MS = 1 / 1.9438
    MS_TO_KNOTS = 1.9438


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

        self.cruise_speeds = kwargs.get("cruise_speeds", [])

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

        speeds_sorted = sorted(self.cruise_speeds, key=lambda a: a[1])
        cruise_speed = 0

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
        vis = Visualizer(animate=False, max_speed=100, max_accel=100, max_score=100)

        while plant.current_time() < self.duration:
            while speeds_sorted and plant.current_time() >= speeds_sorted[0][1]:
                # getting the current cruise speed
                cruise_speed = speeds_sorted[0][0]
                speeds_sorted = speeds_sorted[1:]
                if verbosity > 1:
                    print("current cruise speed changed to", cruise_speed)

            grade = np.interp(plant.current_time(),
                              self.grade_breakpoints, self.grade_values)
            speed_lead = np.interp(
                plant.current_time(), self.speed_lead_breakpoints, self.speed_lead_values)

            speed, acceleration, car_in_front, steer_torque = plant.step(brake=brake,
                                                                         gas=gas,
                                                                         v_lead=speed_lead,
                                                                         grade=grade)

            # If the car in front reaches zero, that's a crash.
            assert car_in_front >= 0

            # TODO: Assert the gap parameter is respected during all the maneuver.

            # TODO: Assert the desired speed matches the actual speed at the end of the maneuver.

            brake, gas = control.control(speed=speed,
                                 acceleration=acceleration,
                                 car_in_front=car_in_front,
                                 gap=gap,
                                 cruise_speed=cruise_speed)


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
