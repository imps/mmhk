#!/usr/bin/python
from optparse import OptionParser
import simfile

def simulate(path):
    we, them = simfile.get_army(path)
    result, report = we.attack(them)
    if result:
        print "Victory! Report:\n%r" % report
    else:
        print "Defeat! Report:\n%r" % report

def main():
    p = OptionParser(usage="%prog simfile")
    opts, args = p.parse_args()

    if len(args) < 1:
        p.error("Simulation file missing.")

    simulate(args[0])

if __name__ == '__main__':
    main()
