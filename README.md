# acc
[![Build Status](https://travis-ci.org/autti/acc.svg?branch=master)](https://travis-ci.org/autti/acc)
[![Coverage Status](https://coveralls.io/repos/github/autti/acc/badge.svg?branch=master)](https://coveralls.io/github/autti/acc?branch=master) 

Adaptive Cruise Control. Udacity micro challenge.

# WHAT SHOULD I DO?
Look for `cruise.py` and implement the `control` function, make the unit tests be more strict with what they check (lower tolerance to differences for example) and submit a pull request.

Here is an example control function that does nothing:

```python
def control(speed=0, acceleration=0, car_in_front=200, gap=5, cruise_speed=None, state=None):
        """Adaptive Cruise Control
           speed: Current car speed (m/s)
           acceleration: Current car acceleration (m/s^2)
           gas: last signal sent. Real number.
           brake: last signal sent. Real number.
           car_in_front: distance in meters to the car in front. (m)
           gap: maximum distance to the car in front (m)
           cruise_speed: desired speed, set via the cruise control buttons. (m/s)
           status: a convenience dictionary to keep state between runs.
        """
        if state is None:
            state = {}
        
        brake = 0
        gas = 0
        
        return gas, brake, state
```

### Unit tests.

There are tests that assert you have not hit the car in front, that you are reasonably close to the desired speed at the end of the maneuver and that there hasn't been a lot of accel/brake so that it's uncomfortable for the user.

You can run them by doing:

```
pytest
```

If you want to see textual information for each of the variables you can increase the verbosity level to:

```
pytest -vvv
```
If you want to see a plot at the end of each maneuver, then add another `v` and one more if you want to see it animated (a lot slower).


### Debugging

When debugging, it is recommended to use the test_verbose_run with the maneuver you want to debug and run it using the `-k` option pytest provides.

```python
def test_verbose_run():
    """Runs tests in verbose mode with plotting and all.
    """
    # assertions in evaluate will make tests fail if needed.
    maneuvers[2].evaluate(control=control, verbosity=5, animate=True, plot=True)
```
    
Like this:
```
pytest -s -l -k test_verbose_run
```


# More information

Join the #acc-challenge channel on the ND013 Slack and ask away.

Here are some reference links shared by Mac:

  - https://www.codeproject.com/articles/36459/pid-process-control-a-cruise-control-example
  - http://itech.fgcu.edu/faculty/zalewski/cda4170/files/pidcontrol.pdf 
  - https://github.com/slater1/AdaptiveCruiseControl 
  - https://github.com/commaai/openpilot/blob/master/selfdrive/controls/lib/adaptivecruise.py

# TESTING

```
python setup.py test
```

# TODO

 - [X] Create assertions for reasonable behavior when implementing the maneuver and fail the tests when those do not pass. For example, distance to car in front is 0, or target speed is different to actual speed.
 - [X] Implement plotting of PID curves to compare solutions.
 - [X] Replace `gas=0` and `brake=0` for a simple solution that passes the tests.
 - [X] Tune PID parameters to pass tests
 - [X] Speed up tests
 - [ ] Reduce the score threshold back to a small number (10, right now it is 200).
 - [ ] Reduce tolerance in the speed check to a small number (1e-2, right now it is 2e0).
 - [ ] Find optimal values of max acceleration, max deceleration and max jerk.
