from report import Report

class Army(list):
    def __repr__(self):
        return "<Army %s>" % list.__repr__(self)

    @property
    def power(self):
        return sum([m.power * m.stack for m in self])

    def pop_stack(self):
        try:
            return self.pop(0)
        except IndexError:
            return None

    def attack(self, army, report=True):
        if report:
            rep = Report()
        else:
            rep = None

        ours = self.pop_stack()
        theirs = army.pop_stack()

        while ours is not None and theirs is not None:
            if report:
                rep.start_round(ours, theirs)

            left1, left2 = ours.fight_with(theirs)

            if report:
                rep.end_round(left1, left2)

            if left1 == 0:
                ours = self.pop_stack()
            if left2 == 0:
                theirs = army.pop_stack()

        if ours is not None:
            self.insert(0, ours)
        if theirs is not None:
            army.insert(0, theirs)

        return (len(self) > len(army), rep)
