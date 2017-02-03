# acc
[![Build Status](https://travis-ci.org/autti/acc.svg?branch=master)](https://travis-ci.org/autti/acc)
[![Coverage Status](https://coveralls.io/repos/github/autti/acc/badge.svg?branch=master)](https://coveralls.  io/github/autti/acc?branch=master) 

Adaptive Cruise Control. Udacity micro challenge.

# WHAT SHOULD I DO?
Look for `cruise.py` and implement the `control` function.

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

 - [ ] Wire cruise.control in runtracks so that the control function is passed to the Plant on initialization
 - [ ] Remove dependency on live20, capnpn, can messages and other openpilot specific bits
 - [ ] Enable running the maneuvers on TravisCI
 - [ ] Create assertions for reasonable behavior when implementing the maneuver and fail the tests when those do not pass.
