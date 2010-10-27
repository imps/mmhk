#!/usr/bin/python
from optparse import OptionParser
import simfile
import optimizer

def optimize(path, powermod):
    we, them = simfile.get_army(path)
    we.apply_power_mod(powermod)
    print "Best constellation: %s" % optimizer.optimize(we, them)

def simulate(path, powermod):
    we, them = simfile.get_army(path)
    we.apply_power_mod(powermod)
    result, report = we.attack(them)
    if result:
        print "Victory! Report: %r" % report
    else:
        print "Defeat! Report: %r" % report

def main():
    p = OptionParser(usage="%prog simfile")
    p.add_option('-o', '--optimize', dest="optimize", action='store_true',
                 help="Try to optimize the stacks, so we get the best attack"
                      " (and possibly a victory, too).")
    p.add_option('-b', '--base-power', dest='powermod', type='float',
                 default=1.0, help="Basic power modifier. (default: %default)")
    opts, args = p.parse_args()

    if len(args) < 1:
        p.error("Simulation file missing.")

    if opts.optimize:
        optimize(args[0], opts.powermod)
    else:
        simulate(args[0], opts.powermod)

if __name__ == '__main__':
    main()
