import os
from enum import Enum
from .plant import Plant
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

    def evaluate(self, control=None, verbosity=0):
        """runs the plant sim and returns (score, run_data)"""
        plant = Plant(
            lead_relevancy=self.lead_relevancy,
            speed=self.speed,
            distance_lead=self.distance_lead,
            verbosity=verbosity,
        )

        event_queue = sorted(self.cruise_button_presses,
                             key=lambda a: a[1])[::-1]

        buttons_sorted = sorted(self.cruise_button_presses, key=lambda a: a[1])
        current_button = 0

        brake = 0
        gas = 0
        steer_torque = 0

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

            brake, gas = control(speed, acceleration,
                                 car_in_front, steer_torque)

            v_rel = speed_lead - speed if self.lead_relevancy else 0.

        return None
