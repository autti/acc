import os

import numpy as np


class Conversions:
    MPH_TO_MS = 1.609 / 3.6
    MS_TO_MPH = 3.6 / 1.609
    KPH_TO_MS = 1. / 3.6
    MS_TO_KPH = 3.6
    MPH_TO_KPH = 1.609
    KPH_TO_MPH = 1. / 1.609
    KNOTS_TO_MS = 1 / 1.9438
    MS_TO_KNOTS = 1.9438

    # Car tecode decimal minutes into decimal degrees, can work with numpy
    # arrays as input
    @staticmethod
    def dm2d(dm):
        degs = np.round(dm / 100.)
        mins = dm - degs * 100.
        return degs + mins / 60.

# Car button codes


class CruiseButtons:
    RES_ACCEL = 4
    DECEL_SET = 3
    CANCEL = 2
    MAIN = 1


class ManeuverPlot(object):

    def __init__(self, title=None):
        self.time_array = []

        self.gas_array = []
        self.brake_array = []
        self.steer_torque_array = []

        self.distance_array = []
        self.speed_array = []
        self.acceleration_array = []

        self.up_accel_cmd_array = []
        self.ui_accel_cmd_array = []

        self.d_rel_array = []
        self.v_rel_array = []
        self.v_lead_array = []
        self.v_target_lead_array = []
        self.pid_speed_array = []
        self.cruise_speed_array = []
        self.jerk_factor_array = []

        self.a_target_min_array = []
        self.a_target_max_array = []

        self.v_target_array = []

        self.title = title

    def add_data(self, time, gas, brake, steer_torque, distance, speed,
                 acceleration, up_accel_cmd, ui_accel_cmd, d_rel, v_rel, v_lead,
                 v_target_lead, pid_speed, cruise_speed, jerk_factor, a_target_min,
                 a_target_max):
        self.time_array.append(time)
        self.gas_array.append(gas)
        self.brake_array.append(brake)
        self.steer_torque_array.append(steer_torque)
        self.distance_array.append(distance)
        self.speed_array.append(speed)
        self.acceleration_array.append(acceleration)
        self.up_accel_cmd_array.append(up_accel_cmd)
        self.ui_accel_cmd_array.append(ui_accel_cmd)
        self.d_rel_array.append(d_rel)
        self.v_rel_array.append(v_rel)
        self.v_lead_array.append(v_lead)
        self.v_target_lead_array.append(v_target_lead)
        self.pid_speed_array.append(pid_speed)
        self.cruise_speed_array.append(cruise_speed)
        self.jerk_factor_array.append(jerk_factor)
        self.a_target_min_array.append(a_target_min)
        self.a_target_max_array.append(a_target_max)
