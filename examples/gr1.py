#!/usr/bin/env python
"""Example of direct GR(1) specification, using only boolean variables.

This example illustrates the use of TuLiP to synthesize a reactive
controller for a GR(1) specification.  We code the specification
directly in GR(1) form and then use TuLiP to synthesize a reactive
controller.

The system is modeled as a discrete transition system in which the
robot can be located anyplace on a 2x3 grid of cells:

    +----+----+----+
    | X3 | X4 | X5 |
    +----+----+----+
    | X0 | X1 | X2 |
    +----+----+----+

The robot is allowed to transition between any two adjacent cells;
diagonal motions are not allowed.  The robot should continuously
revisit the cell X5.

The environment consists of a single state called 'park' that
indicates that the robot should move to cell X0.

The system specification in its simplest form is given by

  []<>park -> []<>X5 && [](park -> <>X0)

We must convert this specification into GR(1) form:

  env_init && []env_safe && []<>env_prog_1 && ... && []<>env_prog_m ->
      sys_init && []sys_safe && []<>sys_prog_1 && ... && []<>sys_prog_n
"""
# 21 Jul 2013, Richard M. Murray (murray@cds.caltech.edu)
# Import the packages that we need
from __future__ import print_function

import logging

from tulip import spec
from tulip import synth
from tulip.transys import machines


logging.basicConfig(level=logging.WARNING)


#
# Environment specification
#
# The environment can issue a park signal that the robot must respond
# to by moving to the lower left corner of the grid.  We assume that
# the park signal is turned off infinitely often.
#
env_vars = {'park'}
env_init = set()                # empty set
env_safe = set()                # empty set
env_prog = '!park'              # []<>(!park)

#
# System dynamics
#
# The system specification describes how the system is allowed to move
# and what the system is required to do in response to an environmental
# action.
#
sys_vars = {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'}
sys_init = {'X0'}
sys_safe = {
    'X0 -> X (X1 || X3)',
    'X1 -> X (X0 || X4 || X2)',
    'X2 -> X (X1 || X5)',
    'X3 -> X (X0 || X4)',
    'X4 -> X (X3 || X1 || X5)',
    'X5 -> X (X4 || X2)',
}

sys_safe.add(synth.exactly_one({'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})[0])

sys_prog = set()                # empty set

#
# System specification
#
# The system specification is that the robot should repeatedly revisit
# the upper right corner of the grid while at the same time responding
# to the park signal by visiting the lower left corner.  The LTL
# specification is given by
#
#     []<> X5 && [](park -> <>X0)
#
# Since this specification is not in GR(1) form, we introduce an
# environment variable X0reach that is initialized to True and the
# specification [](park -> <>X0) becomes
#
#     [](X (X0reach) <-> X0 || (X0reach && !park))
#

# Augment the system description to make it GR(1)
sys_vars |= {'X0reach'}
sys_init |= {'X0reach'}
sys_safe |= {'(X (X0reach) <-> X0) || (X0reach && !park)'}
sys_prog |= {'X0reach', 'X5'}

# Create a GR(1) specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)

#
# Controller synthesis
#
# The controller decides based on current variable values only,
# without knowing yet the next values that environment variables take.
# A controller with this information flow is known as Moore.
specs.moore = True
# Ask the synthesizer to find initial values for system variables
# that, for each initial values that environment variables can
# take and satisfy `env_init`, the initial state satisfies
# `env_init /\ sys_init`.
specs.qinit = r'\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

# At this point we can synthesize the controller
# using one of the available methods.
strategy = synth.synthesize(specs)
assert strategy is not None, 'unrealizable'

# Generate a graphical representation of the controller for viewing,
# or a textual representation if pydot is missing.
if not strategy.save('gr1.png'):
    print(strategy)

# simulate
print(strategy)
machines.random_run(strategy, N=10)
