import re
import monsters
import army

class ParseError(Exception):
    pass

class Simfile(object):
    stack_re = re.compile(r'\s*(#?)([a-zA-Z]+)\s*\((\d+)\)\s*')

    def __init__(self, path):
        self.simfile = open(path, 'r')

    def monstify(self, string):
        match = self.stack_re.match(string)
        if match is None:
            raise ParseError("Could not parse %r." % string)
        if len(match.group(1)) > 0:
            return None # ignore monster
        cls = getattr(monsters, match.group(2))
        count = match.group(3)
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

        remover = lambda x: x is not None
        our_army = filter(remover, our_army)
        their_army = filter(remover, their_army)

        return (army.Army(our_army), army.Army(their_army))

def get_army(path):
    sim = Simfile(path)
    return sim.parse()
