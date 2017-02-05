

class CruiseControl(object):
    def __init__(self):
        self.K_p = 1000.
        self.K_d = 0.

        self.d_front_prev = 100
        self.t_safe = .5 # Safe time to apply brake, .5 s.
        self.prev_setpoint = 0.

    def distance_to_zero(self, speed):
        return speed**2 / (2 * 8.7)

    def control(self, speed=0, acceleration=0, car_in_front=200, gap=5, cruise_speed=None):
        """Adaptive Cruise Control

           speed: Current car speed (m/s)
           acceleration: Current car acceleration (m/s^2)
           gas: last signal sent. Real number.
           brake: last signal sent. Real number.
           car_in_front: distance in meters to the car in front. (m)
           gap: maximum distance to the car in front (m)
        """
        gas = 0.
        brake = 0.

        # If the cruise control speed is not set, let's give the variable a sensible setting.
        if cruise_speed is None:
            cruise_speed = speed


        delta_distance = car_in_front - gap - self.distance_to_zero(speed)

        if delta_distance > 0:
            # if the distance is not too close maintain cruise speed
            set_point = cruise_speed - speed
        else:
            # But override it if we are too close to the car in front.
            set_point = delta_distance

        control = self.K_p * set_point + self.K_d * (set_point - self.prev_setpoint)
        
        if control > 1:
            control = 1.
        elif control < -1:
            control = -1.

        if control >= 0:
            gas = control
        if control < 0:
            brake = -control

        # print(gas, brake)
        #------set variables from previous value-----
        self.prev_setpoint = set_point

        return brake, gas
