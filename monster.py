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
        self.powermod = 1.0

    def __repr__(self):
        return "<Monster %r (%d)>" % (self.name, self.stack)

    @property
    def power(self):
        return self.base_power * self.powermod

    def get_bonus_power(self, monster):
        """
        Return the power value with added weapon boni against `monster`.
        """
        if WEAPON_BONI[self.weapon] == monster.weapon:
            return self.power * WEAPON_BONUS
        return self.power

    def get_stack_from_diff(self, diff):
        new_stack = int(math.ceil(diff / float(self.power)))
        if new_stack < self.stack:
            return new_stack
        else:
            return self.stack

    def save_stack(self):
        """
        Temporarily save the current stack value.
        """
        self._temp_stack = self.stack

    def restore_stack(self):
        """
        Restore temporarily saved stack value.
        """
        self.stack = self._temp_stack

    def fight_with(self, monster, dry_run=False):
        our_power = self.get_bonus_power(monster)
        their_power = monster.get_bonus_power(self)

        our_stack_power = self.stack * our_power
        their_stack_power = monster.stack * their_power

        diff = our_stack_power - their_stack_power

        if diff > 0:
            # we have won
            our_stack = self.get_stack_from_diff(diff)
            their_stack = 0
        else:
            # we have lost
            their_stack = monster.get_stack_from_diff(-diff)
            our_stack = 0

        if not dry_run:
            self.stack = our_stack
            monster.stack = their_stack

        return (our_stack, their_stack)
