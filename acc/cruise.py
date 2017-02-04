a_d_min = -3
a_d_max = 5
K_p = 10
K_d = .2

d_front_prev = 100
t_safe = .5 # Safe time to apply brake, .5 s.


def control_to_accbrake(control, accel, brake):
    if control > 0:
        accel_new = control
        brake_new = 0
    if control < 0:
        accel_new = 0
        brake_new = control
    brake = .5 * brake_new + .5 * brake
    accel = .5 * accel_new + .5 * accel

    return accel, brake



def control_car(speed, car_in_front, acceleration, brake, min_gap):
    delta_distance = car_in_front - 2 * min_gap

    if delta_distance < 0:
        control = -K_p * delta_distance - K_d * car_in_front
        if control > a_d_max:
            control = a_d_max
        elif control < a_d_min:
            control = a_d_min
    else:
        # control = K_p*(speed - cruise_speed)
        # There is no logic for doing this. Control should be used to control the cruise
        # speed but we don't have that parameter as of now.
        control = 0.5
    accel, brake = control_to_accbrake(control, acceleration, brake)

    return accel, brake


def control(speed, acceleration, car_in_front, min_gap, steer_torque):
    """Adaptive Cruise Control
    """
    # --- Implement your solution here ---#
    brake = -acceleration
    gas, brake = control_car(speed, car_in_front, acceleration, brake, 10)
    # ------------------------------------#

    return brake, gas
