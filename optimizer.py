import itertools
import copy

import progressbar

import army

class Optimizer(object):
    def __init__(self, attacker, defender, show_pbar=False):
        self.attacker = copy.deepcopy(attacker)
        self.defender = copy.deepcopy(defender)
        self.show_pbar = show_pbar

    def get_attack_power(self, variation):
        attacker = army.Army(copy.deepcopy(variation))
        power = attacker.power
        defender = copy.deepcopy(self.defender)
        result, report = attacker.attack(defender, report=False)
        if not result:
            return 0
        return power

    def try_attack(self, variation):
        if self.get_attack_power(variation) > 0:
            return True
        else:
            return False

    def brute_units(self, variation, currval, maxval):
        if self.show_pbar:
            widgets = ["Optimizing variation %d of %d: " % (currval, maxval),
                       progressbar.Percentage(), ' ',
                       progressbar.Bar(left='[', right=']'),
                       ' ', progressbar.ETA()]

        current = copy.deepcopy(variation)
        numbers = tuple(range(monster.stack, -1, -1) for monster in variation)

        if self.show_pbar:
            max_combs = reduce(lambda x, y: x * y, [len(n) for n in numbers])
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=max_combs)
            pbar.start()

        results = []
        for i, counts in enumerate(itertools.product(*numbers)):
            if self.show_pbar:
                pbar.update(i)

            for n, unit in enumerate(current):
                unit.stack = counts[n]

            power = self.get_attack_power(current)
            if power > 0:
                results.append((power, counts))

        if self.show_pbar:
            pbar.finish()
        return min(results, key=lambda x: x[0])

    def brute(self):
        stack_variations = []
        for variation in itertools.permutations(self.attacker):
            if self.try_attack(variation):
                stack_variations.append(variation)

        unit_variations = []
        for n, variation in enumerate(stack_variations):
            result = self.brute_units(variation, n+1, len(stack_variations))
            unit_variations.append((result, variation))

        best = min(unit_variations, key=lambda x: x[0])
        best_var = best[0][1]
        best_basevar = best[1]
        for n, var in enumerate(best_var):
            best_basevar[n].stack = var

        return army.Army(best_basevar)

def optimize(attacker, defender, show_pbar=True):
    o = Optimizer(attacker, defender, show_pbar)
    return o.brute()
