import re
import monsters
import army

class ParseError(Exception):
    pass

class Simfile(object):
    stack_re = re.compile(r'\s*([a-zA-Z]+)\s*\((\d+)\)\s*')

    def __init__(self, path):
        self.simfile = open(path, 'r')

    def monstify(self, string):
        match = self.stack_re.match(string)
        if match is None:
            raise ParseError("Could not parse %r." % string)
        cls = getattr(monsters, match.group(1))
        count = match.group(2)
        return cls(int(count))

    def parse(self):
        our_army = []
        their_army = []

        for line in self.simfile:
            splitted = line.split('->', 1)
            if len(splitted[0].strip()) > 0:
                our_army.append(self.monstify(splitted[0]))
            if len(splitted) > 1:
                their_army.append(self.monstify(splitted[1]))

        return (army.Army(our_army), army.Army(their_army))

def get_army(path):
    sim = Simfile(path)
    return sim.parse()
