from report import Report

def advance_iter(iterator):
    try:
        return iterator.next()
    except StopIteration:
        return None

class Army(list):
    def __repr__(self):
        return "<Army %s>" % list.__repr__(self)

    @property
    def power(self):
        return sum([m.power * m.stack for m in self])

    def apply_power_mod(self, modifier):
        for monster in self:
            monster.powermod = modifier

    def remove_empty(self):
        """
        Remove monsters that have an empty stack size.
        """
        self[:] = filter(lambda x: x.stack > 0, self)

    def attack(self, army, report=True):
        if report:
            rep = Report()
        else:
            rep = None

        selfiter = iter(self)
        armyiter = iter(army)

        ours = advance_iter(selfiter)
        theirs = advance_iter(armyiter)

        while ours is not None and theirs is not None:
            if report:
                rep.start_round(ours, theirs)

            left1, left2 = ours.fight_with(theirs)

            if report:
                rep.end_round(left1, left2)

            if left1 == 0:
                ours = advance_iter(selfiter)
            if left2 == 0:
                theirs = advance_iter(armyiter)

        self.remove_empty()
        army.remove_empty()

        return (len(self) > len(army), rep)
