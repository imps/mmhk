#!/usr/bin/python
import re
import csv

from optparse import OptionParser

HEADER = """\
from monster import *
"""

TEMPLATE = """
class %(class)s(Monster):
    name = %(name)r
    weapon = %(weapon)s
    base_power = %(power)d
"""

classify_re = re.compile(r'(?:[^a-zA-Z]+|^)([a-zA-Z])')
def classify(name):
    return classify_re.sub(lambda m: m.group(1).upper(), name)

def weapon_constant(name):
    if name == 'cavalry':
        return 'WEAPON_CAVALRY'
    elif name == 'infantry':
        return 'WEAPON_INFANTRY'
    elif 'shooter' in name:
        return 'WEAPON_SHOOTER'
    else:
        raise ValueError("Weapon constant not found for %s." % name)

def parse_csv(infile, outfile):
    csvfile = open(infile, 'r')

    outfile = open(outfile, 'w')
    outfile.write(HEADER)

    for row in csv.reader(sorted(csvfile), dialect='excel-tab'):
        (
            name,
            aspect,
            weapon,
            rank,
            faction,
            power,
            cost,
            upgrade,
            profitability,
            experience
        ) = row

        context = {
            'class': classify(name),
            'name': name,
            'weapon': weapon_constant(weapon),
            'power': int(power.replace(',', ''))
        }

        outfile.write(TEMPLATE % context)

def main():
    p = OptionParser(usage="%prog csvfile outfile")
    opts, args = p.parse_args()
    if len(args) < 2:
        p.error("Not enough arguments.")

    parse_csv(args[0], args[1])

if __name__ == '__main__':
    main()
