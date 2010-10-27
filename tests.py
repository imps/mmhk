#!/usr/bin/python
import unittest
import monsters
import simfile

class MonsterTest(unittest.TestCase):
    def test_hard_win(self):
        attacker = monsters.Skeleton(550)
        defender = monsters.ArchDevil(5)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (1, 0))

    def test_hard_win2(self):
        attacker = monsters.Skeleton(555)
        defender = monsters.ArchDevil(5)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (6, 0))

    def test_hard_loss(self):
        attacker = monsters.BoneDragon(2)
        defender = monsters.Cerberus(27)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (0, 1))

    def test_hard_loss(self):
        attacker = monsters.BoneDragon(1)
        defender = monsters.Cerberus(27)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (0, 14))

    def test_bonus_win(self):
        attacker = monsters.Skeleton(24)
        defender = monsters.Cerberus(7)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (1, 0))

    def test_vampire_marksman(self):
        attacker = monsters.Vampire(7)
        defender = monsters.Marksman(21)
        result = attacker.fight_with(defender)
        self.assertEqual(result, (0, 12))

class SimfileTest(unittest.TestCase):
    def test_open_simfile(self):
        army1, army2 = simfile.get_army('test1.sim')
        self.assertEqual(len(army1), 6)
        self.assertEqual(len(army2), 3)

    def test_fight_lose_simfile(self):
        army1, army2 = simfile.get_army('test1.sim')
        result, report = army1.attack(army2)
        self.assertFalse(result)
        self.assertEqual(len(army1), 0)
        # no one harmed, that angel killed them all ;-)
        self.assertEqual(len(army2), 3)
        self.assertEqual(len(filter(lambda x: x == (0, 1), report.leftovers())), 6)

    def test_fight_win_simfile(self):
        army1, army2 = simfile.get_army('test1.sim')
        army1[0].stack += 10 # vampires
        result, report = army1.attack(army2)
        self.assertTrue(result)
        self.assertEqual(len(army1), 2)
        self.assertEqual(len(army2), 0)
        self.assertEqual(army1[0].stack, 4)
        self.assertEqual(
            report.leftovers(),
            [(7, 0), (0, 12), (0, 2), (5, 0), (0, 5), (0, 4), (4, 0)]
        )

    def test_hard_battle(self):
        army1, army2 = simfile.get_army('test1.sim')
        result, report = army1.attack(army2)
        self.assertFalse(result);

if __name__ == '__main__':
    unittest.main()
