class Round(object):
    def __init__(self, attacker, defender):
        self.attacker = {
            'name': attacker.name,
            'power': attacker.power,
            'count': attacker.stack,
        }

        self.defender = {
            'name': defender.name,
            'power': defender.power,
            'count': defender.stack,
        }

    def finish(self, attacker_left, defender_left):
        self.attacker['left'] = attacker_left
        self.defender['left'] = defender_left

    def __repr__(self):
        attacker = "%- 6s %20s % 4d" % (
            "[%d]" % self.attacker['count'],
            self.attacker['name'],
            self.attacker['left'] - self.attacker['count'],
        )

        defender = "%- 4d %-20s % 6s" % (
            self.defender['left'] - self.defender['count'],
            self.defender['name'],
            "[%d]" % self.defender['count'],
        )

        return "%s <-> %s" % (attacker, defender)

class Report(list):
    def __init__(self):
        list.__init__(self)
        self.current_round = None

    def __repr__(self):
        return "\n"+"\n".join([repr(item) for item in self])

    def start_round(self, attacker, defender):
        self.current_round = Round(attacker, defender)

    def end_round(self, attacker_left, defender_left):
        self.current_round.finish(attacker_left, defender_left)
        self.append(self.current_round)
        self.current_round = None

    def leftovers(self):
        lefts = []
        for item in self:
            lefts.append((
                item.attacker['left'],
                item.defender['left'],
            ))
        return lefts
