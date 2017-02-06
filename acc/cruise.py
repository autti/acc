

class CruiseControl(object):
    def __init__(self):
        self.K_p = 0.15
        self.K_d = 0.
        self.K_i = 0.0003

        self.d_front_prev = 100
        self.t_safe = .5 # Safe time to apply brake, .5 s.
        self.prev_setpoint = 0.
        self.integral_setpoint = 0.
        self.maintaining_distance = False

    def distance_to_zero(self, speed):
        # max_accel = 8.7
        return speed**2 / (2 * 5)

    def control(self, speed=0, acceleration=0, car_in_front=200, gap=5, cruise_speed=None):
        """Adaptive Cruise Control

           speed: Current car speed (m/s)
           acceleration: Current car acceleration (m/s^2)
           gas: last signal sent. Real number.
           brake: last signal sent. Real number.
           car_in_front: distance in meters to the car in front. (m)
           gap: maximum distance to the car in front (m)
        """

        delta_distance = car_in_front - 2 * gap - self.distance_to_zero(speed)
        # print(delta_distance, self.distance_to_zero(speed))

        # if the car ahead does not allow to get to cruise speed
        # use safe following distance as a measure until cruise speed is reached again
        if delta_distance < 0:
            self.maintaining_distance = True
        elif speed >= cruise_speed:
            self.maintaining_distance = False

        if self.maintaining_distance:
            # But override it if we are too close to the car in front.
            set_point = delta_distance
        else:
            # if the distance is not too close maintain cruise speed
            set_point = cruise_speed - speed


        control = self.K_p * set_point + self.K_d * (set_point - self.prev_setpoint) + self.K_i * self.integral_setpoint
        # print(set_point, control)
        
        if control > 1:
            control = 1.
        elif control < -1:
            control = -1.

        if control >= 0:
            gas = control
            brake = 0
        if control < 0:
            gas = 0
            brake = -control

        # print(gas, brake)
        #------set variables from previous value-----
        self.prev_setpoint = set_point
        self.integral_setpoint += set_point

        return brake, gas
