import math

WEAPON_INFANTRY = 0
WEAPON_CAVALRY = 1
WEAPON_SHOOTER = 2

WEAPON_BONI = {
    WEAPON_INFANTRY: WEAPON_CAVALRY,
    WEAPON_SHOOTER: WEAPON_INFANTRY,
    WEAPON_CAVALRY: WEAPON_SHOOTER,
}

WEAPON_BONUS = 1.5

class Monster(object):
    def __init__(self, stack=0):
        self.stack = stack

    def __repr__(self):
        return "<Monster %r (%d)>" % (self.name, self.stack)

    @property
    def power(self):
        return self.base_power

    def get_bonus_power(self, monster):
        """
        Return the power value with added weapon boni against `monster`.
        """
        if WEAPON_BONI[self.weapon] == monster.weapon:
            return self.power * WEAPON_BONUS
        return self.power

    def new_stack_from_diff(self, diff):
        new_stack = int(math.ceil(diff / float(self.power)))
        if new_stack < self.stack:
            self.stack = new_stack

    def fight_with(self, monster):
        our_power = self.get_bonus_power(monster)
        their_power = monster.get_bonus_power(self)

        our_stack_power = self.stack * our_power
        their_stack_power = monster.stack * their_power

        diff = our_stack_power - their_stack_power

        if diff > 0:
            # we have won
            self.new_stack_from_diff(diff)
            monster.stack = 0
        else:
            # we have lost
            monster.new_stack_from_diff(-diff)
            self.stack = 0

        return (self.stack, monster.stack)
