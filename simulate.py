#!/usr/bin/python
from optparse import OptionParser
import simfile
import optimizer

def optimize(path):
    we, them = simfile.get_army(path)
    print "Best constellation: %s" % optimizer.optimize(we, them)

def simulate(path):
    we, them = simfile.get_army(path)
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
    opts, args = p.parse_args()

    if len(args) < 1:
        p.error("Simulation file missing.")

    if opts.optimize:
        optimize(args[0])
    else:
        simulate(args[0])

if __name__ == '__main__':
    main()
