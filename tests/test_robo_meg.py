"""
Набор модульных и сценарных тестов для роботизированного мегалодона RoboMeg.
Составлен в строгом соответствии с ТЗ (SPEC.md) и спецификацией тестов (TEST_CASES.md).
"""

import unittest
from robo_meg import (
    RoboMeg,
    CrazyVehicleError,
    RoboMegError,
    EnergyEmpty,
    RoboMegCannotMoveOnGround,
    AlreadyAirborne,
    JumpTooLong,
    RoboMegNotHungry,
    UnsafeHuntingZone,
    NoFishHere,
)


class TestRoboMegModule(unittest.TestCase):
    """
    Модульные тесты TC-M-001 ... TC-M-027.
    """

    def setUp(self) -> None:
        """
        Инициализация базового мегалодона:
        RoboMeg("RoboMeg", mass_kg=4000, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0, energy=100.0)
        """
        self.base_meg = RoboMeg(
            name="RoboMeg",
            mass_kg=4000.0,
            jump_length_km=4.0,
            bite_force_kn=60.0,
            max_speed_kmh=50.0,
            energy=100.0,
        )

    def test_TC_M_001_init_stores_parameters(self) -> None:
        """
        TC-M-001: Создание RoboMeg с валидными параметрами.
        Проверка сохранения параметров и начальных значений position_km=0.0, is_airborne=False.
        """
        meg = RoboMeg(
            name="AlphaMeg",
            mass_kg=3500.0,
            jump_length_km=5.0,
            bite_force_kn=70.0,
            max_speed_kmh=45.0,
            energy=90.0,
        )
        self.assertEqual(meg.name, "AlphaMeg")
        self.assertEqual(meg.mass_kg, 3500.0)
        self.assertEqual(meg.jump_length_km, 5.0)
        self.assertEqual(meg.bite_force_kn, 70.0)
        self.assertEqual(meg.max_speed_kmh, 45.0)
        self.assertEqual(meg.energy, 90.0)
        self.assertEqual(meg.position_km, 0.0)
        self.assertFalse(meg.is_airborne)

    def test_TC_M_002_init_empty_name_raises(self) -> None:
        """
        TC-M-002: name="" / name="   " вызывает ValueError.
        """
        with self.assertRaises(ValueError):
            RoboMeg("", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("   ", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0)

    def test_TC_M_003_init_nonpositive_params_raise(self) -> None:
        """
        TC-M-003: mass_kg=0, jump_length_km=-1, bite_force_kn=0, max_speed_kmh=-5 вызывают ValueError.
        """
        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=0.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=-100.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=0.0, bite_force_kn=60.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=-1.0, bite_force_kn=60.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=0.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=-5.0, max_speed_kmh=50.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=0.0)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=-5.0)

    def test_TC_M_004_init_energy_bounds(self) -> None:
        """
        TC-M-004: energy=-0.1 и 100.1 -> ValueError; 0 и 100 OK; без energy -> 100.0.
        """
        with self.assertRaises(ValueError):
            RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=-0.1)

        with self.assertRaises(ValueError):
            RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=100.1)

        meg_zero = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=0.0)
        self.assertEqual(meg_zero.energy, 0.0)

        meg_max = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=100.0)
        self.assertEqual(meg_max.energy, 100.0)

        meg_default = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0)
        self.assertEqual(meg_default.energy, 100.0)

    def test_TC_M_005_public_attributes_read_only(self) -> None:
        """
        TC-M-005: Изменение name, mass_kg, jump_length_km, bite_force_kn,
        max_speed_kmh, energy, position_km, is_airborne вызывает AttributeError.
        """
        attributes = [
            ("name", "NewName"),
            ("mass_kg", 5000.0),
            ("jump_length_km", 10.0),
            ("bite_force_kn", 80.0),
            ("max_speed_kmh", 70.0),
            ("energy", 50.0),
            ("position_km", 10.0),
            ("is_airborne", True),
        ]
        for attr_name, dummy_val in attributes:
            with self.subTest(attribute=attr_name):
                with self.assertRaises(AttributeError):
                    setattr(self.base_meg, attr_name, dummy_val)

    def test_TC_M_006_move_water(self) -> None:
        """
        TC-M-006: move(25, "water") -> 0.5; position_km == 25.0, energy == 75.0, is_airborne == False.
        """
        duration = self.base_meg.move(25.0, "water")
        self.assertEqual(duration, 0.5)
        self.assertEqual(self.base_meg.position_km, 25.0)
        self.assertEqual(self.base_meg.energy, 75.0)
        self.assertFalse(self.base_meg.is_airborne)

    def test_TC_M_007_move_air_valid_jump(self) -> None:
        """
        TC-M-007: move(4, "air") при jump_length_km == 4 -> 0.04; position_km == 4.0, energy == 92.0, is_airborne == True.
        """
        duration = self.base_meg.move(4.0, "air")
        # 4.0 / (50.0 * 2) = 0.04; расход 4.0 * 2 = 8.0
        self.assertEqual(duration, 0.04)
        self.assertEqual(self.base_meg.position_km, 4.0)
        self.assertEqual(self.base_meg.energy, 92.0)
        self.assertTrue(self.base_meg.is_airborne)

    def test_TC_M_008a_move_air_exceeds_jump_length_raises(self) -> None:
        """
        TC-M-008a: move(4.1, "air") при jump_length_km == 4 -> JumpTooLong; состояние не меняется.
        """
        with self.assertRaises(JumpTooLong):
            self.base_meg.move(4.1, "air")

        self.assertEqual(self.base_meg.position_km, 0.0)
        self.assertEqual(self.base_meg.energy, 100.0)
        self.assertFalse(self.base_meg.is_airborne)

    def test_TC_M_008b_move_air_already_airborne_raises(self) -> None:
        """
        TC-M-008b: Предусловие: move(2, "air"). Повторный move(1, "air") в воздухе -> AlreadyAirborne;
        состояние не меняется после неудачного вызова.
        """
        self.base_meg.move(2.0, "air")
        self.assertTrue(self.base_meg.is_airborne)
        self.assertEqual(self.base_meg.position_km, 2.0)
        self.assertEqual(self.base_meg.energy, 96.0)

        with self.assertRaises(AlreadyAirborne):
            self.base_meg.move(1.0, "air")

        self.assertTrue(self.base_meg.is_airborne)
        self.assertEqual(self.base_meg.position_km, 2.0)
        self.assertEqual(self.base_meg.energy, 96.0)

    def test_TC_M_009_move_ground_raises(self) -> None:
        """
        TC-M-009: move(1, "ground") -> RoboMegCannotMoveOnGround; состояние не меняется.
        """
        with self.assertRaises(RoboMegCannotMoveOnGround):
            self.base_meg.move(1.0, "ground")

        self.assertEqual(self.base_meg.position_km, 0.0)
        self.assertEqual(self.base_meg.energy, 100.0)
        self.assertFalse(self.base_meg.is_airborne)

    def test_TC_M_010a_move_insufficient_and_exact_energy(self) -> None:
        """
        TC-M-010a: При energy=10:
        move(15, "water") -> EnergyEmpty;
        move(10, "water") -> успешно, energy == 0.0.
        """
        meg1 = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=10.0)
        with self.assertRaises(EnergyEmpty):
            meg1.move(15.0, "water")
        self.assertEqual(meg1.energy, 10.0)
        self.assertEqual(meg1.position_km, 0.0)

        meg2 = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=10.0)
        duration = meg2.move(10.0, "water")
        self.assertEqual(duration, 0.2)
        self.assertEqual(meg2.energy, 0.0)
        self.assertEqual(meg2.position_km, 10.0)

    def test_TC_M_010b_pass_island_insufficient_and_exact_energy(self) -> None:
        """
        TC-M-010b: pass_island при нехватке энергии и точном совпадении.
        Прыжок (pass_island(4), нужно 8 энергии):
        - при energy=5 -> EnergyEmpty
        - при energy=8 -> успешно, energy == 0.0, is_airborne == True
        Обплыв (pass_island(6), дуга 9.0 км, нужно 9 энергии):
        - при energy=5 -> EnergyEmpty
        - при energy=9 -> успешно, energy == 0.0, is_airborne == False
        """
        # Прыжок: нехватка
        meg_jump_fail = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=5.0)
        with self.assertRaises(EnergyEmpty):
            meg_jump_fail.pass_island(4.0)
        self.assertEqual(meg_jump_fail.energy, 5.0)
        self.assertEqual(meg_jump_fail.position_km, 0.0)

        # Прыжок: точный расход
        meg_jump_ok = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=8.0)
        meg_jump_ok.pass_island(4.0)
        self.assertEqual(meg_jump_ok.energy, 0.0)
        self.assertEqual(meg_jump_ok.position_km, 4.0)
        self.assertTrue(meg_jump_ok.is_airborne)

        # Обплыв: нехватка
        meg_swim_fail = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=5.0)
        with self.assertRaises(EnergyEmpty):
            meg_swim_fail.pass_island(6.0)
        self.assertEqual(meg_swim_fail.energy, 5.0)
        self.assertEqual(meg_swim_fail.position_km, 0.0)

        # Обплыв: точный расход
        meg_swim_ok = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=9.0)
        meg_swim_ok.pass_island(6.0)
        self.assertEqual(meg_swim_ok.energy, 0.0)
        self.assertEqual(meg_swim_ok.position_km, 9.0)
        self.assertFalse(meg_swim_ok.is_airborne)

    def test_TC_M_010c_float_energy_depletion_no_false_empty(self) -> None:
        """
        TC-M-010c: При energy=0.3 три вызова move(0.1, "water") завершаются успешно,
        energy == 0.0 без ложного EnergyEmpty из-за погрешности float.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=0.3)
        meg.move(0.1, "water")
        self.assertEqual(meg.energy, 0.2)
        meg.move(0.1, "water")
        self.assertEqual(meg.energy, 0.1)
        meg.move(0.1, "water")
        self.assertEqual(meg.energy, 0.0)
        self.assertEqual(meg.position_km, 0.3)

    def test_TC_M_011_pass_island_jump(self) -> None:
        """
        TC-M-011: pass_island(4) при jump_length_km == 4 -> прыжок: 0.04;
        position_km == 4.0, energy == 92.0, is_airborne == True.
        """
        duration = self.base_meg.pass_island(4.0)
        self.assertEqual(duration, 0.04)
        self.assertEqual(self.base_meg.position_km, 4.0)
        self.assertEqual(self.base_meg.energy, 92.0)
        self.assertTrue(self.base_meg.is_airborne)

    def test_TC_M_012_pass_island_swim_semicircle(self) -> None:
        """
        TC-M-012: pass_island(6) при jump_length_km == 4 -> обплыв: 0.18;
        position_km == 9.0, energy == 91.0, is_airborne == False.
        """
        duration = self.base_meg.pass_island(6.0)
        self.assertEqual(duration, 0.18)
        self.assertEqual(self.base_meg.position_km, 9.0)
        self.assertEqual(self.base_meg.energy, 91.0)
        self.assertFalse(self.base_meg.is_airborne)

    def test_TC_M_013_hunt_fish_success(self) -> None:
        """
        TC-M-013: Предусловие: energy=40, move(5, "water") -> hunt_fish() ->
        energy == 60.0, position_km == 5.0, is_airborne == False.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=45.0)
        meg.move(5.0, "water")
        self.assertEqual(meg.energy, 40.0)
        self.assertEqual(meg.position_km, 5.0)

        meg.hunt_fish()
        self.assertEqual(meg.energy, 60.0)
        self.assertEqual(meg.position_km, 5.0)
        self.assertFalse(meg.is_airborne)

    def test_TC_M_014_hunt_fish_not_hungry_raises(self) -> None:
        """
        TC-M-014: energy=50.0, move(5, "water") -> hunt_fish() -> RoboMegNotHungry; состояние не меняется.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=55.0)
        meg.move(5.0, "water")
        self.assertEqual(meg.energy, 50.0)
        self.assertEqual(meg.position_km, 5.0)

        with self.assertRaises(RoboMegNotHungry):
            meg.hunt_fish()

        self.assertEqual(meg.energy, 50.0)
        self.assertEqual(meg.position_km, 5.0)

    def test_TC_M_015_hunt_fish_unsafe_zone_raises(self) -> None:
        """
        TC-M-015: energy=40 на старте / move(1, "water") -> hunt_fish() -> UnsafeHuntingZone;
        состояние не меняется.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=40.0)
        # На старте проплыто 0 км < 2.0 км
        with self.assertRaises(UnsafeHuntingZone):
            meg.hunt_fish()
        self.assertEqual(meg.energy, 40.0)
        self.assertEqual(meg.position_km, 0.0)

        # После перемещения на 1 км проплыто 1.0 км < 2.0 км
        meg.move(1.0, "water")
        with self.assertRaises(UnsafeHuntingZone):
            meg.hunt_fish()
        self.assertEqual(meg.energy, 39.0)
        self.assertEqual(meg.position_km, 1.0)

    def test_TC_M_016_hunt_fish_twice_same_position_raises(self) -> None:
        """
        TC-M-016: Вызов hunt_fish() успешно -> повторный hunt_fish() на той же позиции ->
        NoFishHere; состояние не меняется.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=30.0)
        meg.move(3.0, "water")
        meg.hunt_fish()
        self.assertEqual(meg.energy, 47.0)
        self.assertEqual(meg.position_km, 3.0)

        with self.assertRaises(NoFishHere):
            meg.hunt_fish()

        self.assertEqual(meg.energy, 47.0)
        self.assertEqual(meg.position_km, 3.0)

    def test_TC_M_017_hunt_fish_exception_priority(self) -> None:
        """
        TC-M-017: Проверка детерминированного приоритета исключений:
        1. UnsafeHuntingZone
        2. NoFishHere
        3. RoboMegNotHungry
        """
        # Приоритет 1 выше 3: energy >= 50, но зона небезопасна (на старте)
        meg_start = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=60.0)
        with self.assertRaises(UnsafeHuntingZone):
            meg_start.hunt_fish()

        # Приоритет 1 выше 3: energy >= 50, но аппарат в воздухе
        meg_air = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=100.0)
        meg_air.move(2.0, "air")
        self.assertTrue(meg_air.is_airborne)
        with self.assertRaises(UnsafeHuntingZone):
            meg_air.hunt_fish()

        # Приоритет 2 выше 3: рыба уже съедена на этой точке, а энергия стала >= 50
        meg_twice = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=40.0)
        meg_twice.move(3.0, "water")
        meg_twice.hunt_fish()  # energy = 37 + 20 = 57.0 (>= 50)
        self.assertGreaterEqual(meg_twice.energy, 50.0)
        with self.assertRaises(NoFishHere):
            meg_twice.hunt_fish()

    def test_TC_M_018_overcome_coral_reef(self) -> None:
        """
        TC-M-018: can_overcome("coral_reef") -> False в воде / True в воздухе.
        """
        # В воде
        self.assertFalse(self.base_meg.is_airborne)
        self.assertFalse(self.base_meg.can_overcome("coral_reef"))

        # В воздухе
        self.base_meg.move(2.0, "air")
        self.assertTrue(self.base_meg.is_airborne)
        self.assertTrue(self.base_meg.can_overcome("coral_reef"))

    def test_TC_M_019_overcome_iceberg_and_steel_net(self) -> None:
        """
        TC-M-019: can_overcome("iceberg"): bite_force_kn=50 / energy=30 -> False;
        bite_force_kn=60 & energy=31 -> True.
        Также проверка steel_net: в воздухе или bite_force_kn > 25.
        """
        # Айсберг
        meg_low_bite = RoboMeg("Meg", 4000, 4.0, 50.0, 50.0, energy=50.0)
        self.assertFalse(meg_low_bite.can_overcome("iceberg"))

        meg_low_energy = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=30.0)
        self.assertFalse(meg_low_energy.can_overcome("iceberg"))

        meg_iceberg_ok = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=31.0)
        self.assertTrue(meg_iceberg_ok.can_overcome("iceberg"))

        # Стальная сеть (SPEC 3.4.4: is_airborne == True ИЛИ bite_force_kn > 25)
        meg_net_low = RoboMeg("Meg", 4000, 4.0, 25.0, 50.0, energy=50.0)
        self.assertFalse(meg_net_low.can_overcome("steel_net"))

        meg_net_ok = RoboMeg("Meg", 4000, 4.0, 26.0, 50.0, energy=50.0)
        self.assertTrue(meg_net_ok.can_overcome("steel_net"))

        meg_net_air = RoboMeg("Meg", 4000, 4.0, 10.0, 50.0, energy=50.0)
        meg_net_air.move(1.0, "air")
        self.assertTrue(meg_net_air.can_overcome("steel_net"))

    def test_TC_M_020_overcome_whirlpool(self) -> None:
        """
        TC-M-020: can_overcome("whirlpool"): max_speed_kmh=59 / energy=40 /
        в воздухе / max_speed_kmh=60 & energy=41 -> False / False / False / True.
        """
        meg_low_speed = RoboMeg("Meg", 4000, 4.0, 60.0, 59.0, energy=50.0)
        self.assertFalse(meg_low_speed.can_overcome("whirlpool"))

        meg_low_energy = RoboMeg("Meg", 4000, 4.0, 60.0, 60.0, energy=40.0)
        self.assertFalse(meg_low_energy.can_overcome("whirlpool"))

        meg_air = RoboMeg("Meg", 4000, 4.0, 60.0, 60.0, energy=50.0)
        meg_air.move(1.0, "air")
        self.assertFalse(meg_air.can_overcome("whirlpool"))

        meg_ok = RoboMeg("Meg", 4000, 4.0, 60.0, 60.0, energy=41.0)
        self.assertTrue(meg_ok.can_overcome("whirlpool"))

    def test_TC_M_021_unknown_obstacle_raises(self) -> None:
        """
        TC-M-021: can_overcome("unknown") -> ValueError.
        """
        with self.assertRaises(ValueError):
            self.base_meg.can_overcome("unknown")

    def test_TC_M_022_calculate_energy(self) -> None:
        """
        TC-M-022: calculate_energy(10, "water") -> 10.0;
        calculate_energy(1, "ground") -> RoboMegCannotMoveOnGround.
        Состояние аппарата не меняется.
        """
        energy_water = self.base_meg.calculate_energy(10.0, "water")
        self.assertEqual(energy_water, 10.0)

        energy_air = self.base_meg.calculate_energy(5.0, "air")
        self.assertEqual(energy_air, 10.0)

        with self.assertRaises(RoboMegCannotMoveOnGround):
            self.base_meg.calculate_energy(1.0, "ground")

        # Состояние не изменилось
        self.assertEqual(self.base_meg.energy, 100.0)
        self.assertEqual(self.base_meg.position_km, 0.0)
        self.assertFalse(self.base_meg.is_airborne)

    def test_TC_M_023_refuel_and_cap(self) -> None:
        """
        TC-M-023: energy=50 -> refuel(30) -> energy == 80.0;
        refuel(1000) -> energy == 100.0; refuel(-5) / refuel(0) -> ValueError.
        """
        meg = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=50.0)
        meg.refuel(30.0)
        self.assertEqual(meg.energy, 80.0)

        meg.refuel(1000.0)
        self.assertEqual(meg.energy, 100.0)

        with self.assertRaises(ValueError):
            meg.refuel(-5.0)

        with self.assertRaises(ValueError):
            meg.refuel(0.0)

    def test_TC_M_024_get_status_snapshot(self) -> None:
        """
        TC-M-024: get_status() -> полный словарь из 8 актуальных ключей,
        независимый от объекта.
        """
        status = self.base_meg.get_status()
        expected_keys = {
            "name",
            "mass_kg",
            "jump_length_km",
            "bite_force_kn",
            "max_speed_kmh",
            "energy",
            "position_km",
            "is_airborne",
        }
        self.assertEqual(set(status.keys()), expected_keys)
        self.assertEqual(status["name"], "RoboMeg")
        self.assertEqual(status["mass_kg"], 4000.0)
        self.assertEqual(status["jump_length_km"], 4.0)
        self.assertEqual(status["bite_force_kn"], 60.0)
        self.assertEqual(status["max_speed_kmh"], 50.0)
        self.assertEqual(status["energy"], 100.0)
        self.assertEqual(status["position_km"], 0.0)
        self.assertFalse(status["is_airborne"])

        # Мутация словаря не влияет на объект
        status["energy"] = 0.0
        self.assertEqual(self.base_meg.energy, 100.0)

    def test_TC_M_025_invalid_parameter_types_raise(self) -> None:
        """
        TC-M-025: name=123, mass_kg="4000", energy=True -> TypeError.
        Проверка типов для конструктора и методов.
        """
        with self.assertRaises(TypeError):
            RoboMeg(123, 4000, 4.0, 60.0, 50.0)  # type: ignore

        with self.assertRaises(TypeError):
            RoboMeg("Meg", "4000", 4.0, 60.0, 50.0)  # type: ignore

        with self.assertRaises(TypeError):
            RoboMeg("Meg", 4000, None, 60.0, 50.0)  # type: ignore

        with self.assertRaises(TypeError):
            RoboMeg("Meg", 4000, 4.0, [], 50.0)  # type: ignore

        with self.assertRaises(TypeError):
            RoboMeg("Meg", 4000, 4.0, 60.0, {})  # type: ignore

        with self.assertRaises(TypeError):
            RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=True)

        with self.assertRaises(TypeError):
            self.base_meg.move("25", "water")  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.move(True, "water")  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.move(25.0, 123)  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.pass_island(True)

        with self.assertRaises(TypeError):
            self.base_meg.pass_island("4")  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.can_overcome(123)  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.calculate_energy(True, "water")

        with self.assertRaises(TypeError):
            self.base_meg.calculate_energy(10.0, 123)  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.refuel("10")  # type: ignore

        with self.assertRaises(TypeError):
            self.base_meg.refuel(False)

    def test_TC_M_026_exception_hierarchy(self) -> None:
        """
        TC-M-026: Проверка наследования:
        RoboMegError -> CrazyVehicleError -> RuntimeError.
        Все доменные ошибки наследуют RoboMegError.
        """
        self.assertTrue(issubclass(CrazyVehicleError, RuntimeError))
        self.assertTrue(issubclass(RoboMegError, CrazyVehicleError))

        domain_exceptions = [
            EnergyEmpty,
            RoboMegCannotMoveOnGround,
            AlreadyAirborne,
            JumpTooLong,
            RoboMegNotHungry,
            UnsafeHuntingZone,
            NoFishHere,
        ]
        for exc_class in domain_exceptions:
            with self.subTest(exception=exc_class.__name__):
                self.assertTrue(issubclass(exc_class, RoboMegError))

    def test_TC_M_027_exception_messages(self) -> None:
        """
        TC-M-027: Проверка соответствия текстов сообщений исключений таблице 6.2 ТЗ.
        """
        # Пустое имя
        with self.assertRaises(ValueError) as ctx:
            RoboMeg("", 4000, 4.0, 60.0, 50.0)
        self.assertIn("name must not be empty", str(ctx.exception))

        # Неположительные числовые параметры
        with self.assertRaises(ValueError) as ctx:
            RoboMeg("Meg", 0, 4.0, 60.0, 50.0)
        self.assertIn("mass_kg must be positive", str(ctx.exception))

        # Некорректная энергия
        with self.assertRaises(ValueError) as ctx:
            RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=101.0)
        self.assertIn("energy must be between 0 and 100", str(ctx.exception))

        # Движение по земле
        with self.assertRaises(RoboMegCannotMoveOnGround) as ctx:
            self.base_meg.move(1.0, "ground")
        self.assertIn("robomeg cannot move on ground", str(ctx.exception))

        # Прыжок из воздуха
        self.base_meg.move(2.0, "air")
        with self.assertRaises(AlreadyAirborne) as ctx:
            self.base_meg.move(1.0, "air")
        self.assertIn("cannot jump while already airborne", str(ctx.exception))

        # Превышение длины прыжка
        meg_jump = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0)
        with self.assertRaises(JumpTooLong) as ctx:
            meg_jump.move(5.0, "air")
        self.assertIn("jump distance exceeds max jump length", str(ctx.exception))

        # Нехватка энергии
        meg_energy = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=5.0)
        with self.assertRaises(EnergyEmpty) as ctx:
            meg_energy.move(10.0, "water")
        self.assertIn("not enough energy", str(ctx.exception))

        # Охота при is_airborne или пути < 2 км
        meg_unsafe = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=40.0)
        with self.assertRaises(UnsafeHuntingZone) as ctx:
            meg_unsafe.hunt_fish()
        self.assertIn("must swim at least 2.0 km in water before hunting", str(ctx.exception))

        # Повторная охота в той же точке
        meg_nofish = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=40.0)
        meg_nofish.move(3.0, "water")
        meg_nofish.hunt_fish()
        with self.assertRaises(NoFishHere) as ctx:
            meg_nofish.hunt_fish()
        self.assertIn("fish already eaten at position", str(ctx.exception))

        # Охота при energy >= 50
        meg_nothungry = RoboMeg("Meg", 4000, 4.0, 60.0, 50.0, energy=60.0)
        meg_nothungry.move(3.0, "water")
        with self.assertRaises(RoboMegNotHungry) as ctx:
            meg_nothungry.hunt_fish()
        self.assertIn("energy is 50 or above, hunting is not needed", str(ctx.exception))


class TestRoboMegScenario(unittest.TestCase):
    """
    Сценарные тесты TC-S-001 ... TC-S-003 (SPEC 4.2).
    """

    def test_TC_S_001_archipelago_and_hunting_after_jump(self) -> None:
        """
        TC-S-001 (SPEC 4.2 Сценарий 1):
        Полный маршрут архипелага и охота после прыжка.
        Итог: position_km == 21.0, energy == 54.0, is_airborne == False.
        """
        # Given: Мегалодон на старте в воде
        meg = RoboMeg("RoboMeg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0, energy=60.0)
        self.assertEqual(meg.position_km, 0.0)
        self.assertFalse(meg.is_airborne)
        self.assertEqual(meg.energy, 60.0)

        # When: pass_island(3)
        # Then: Прыжок по воздуху (3 <= 4). Скорость 100, время 3 / 100 = 0.03
        t1 = meg.pass_island(3.0)
        self.assertEqual(t1, 0.03)
        self.assertEqual(meg.position_km, 3.0)
        self.assertEqual(meg.energy, 54.0)
        self.assertTrue(meg.is_airborne)

        # When: hunt_fish()
        # Then: UnsafeHuntingZone (из-за фазы прыжка is_airborne == True)
        with self.assertRaises(UnsafeHuntingZone):
            meg.hunt_fish()

        # When: move(5, "water")
        # Then: position_km == 8.0, energy == 49.0, is_airborne == False
        t2 = meg.move(5.0, "water")
        self.assertEqual(t2, 0.1)
        self.assertEqual(meg.position_km, 8.0)
        self.assertEqual(meg.energy, 49.0)
        self.assertFalse(meg.is_airborne)

        # When: pass_island(2)
        # Then: Прыжок (2 <= 4). Время 2 / 100 = 0.02
        t3 = meg.pass_island(2.0)
        self.assertEqual(t3, 0.02)
        self.assertEqual(meg.position_km, 10.0)
        self.assertEqual(meg.energy, 45.0)
        self.assertTrue(meg.is_airborne)

        # When: move(1, "water")
        # Then: position_km == 11.0, energy == 44.0, is_airborne == False
        t4 = meg.move(1.0, "water")
        self.assertEqual(t4, 0.02)
        self.assertEqual(meg.position_km, 11.0)
        self.assertEqual(meg.energy, 44.0)
        self.assertFalse(meg.is_airborne)

        # When: hunt_fish()
        # Then: UnsafeHuntingZone (проплыто 1 км по воде после прыжка, нужно >= 2.0 км)
        with self.assertRaises(UnsafeHuntingZone):
            meg.hunt_fish()

        # When: move(1, "water")
        # Then: position_km == 12.0, energy == 43.0, проплыто 2 км по воде
        t5 = meg.move(1.0, "water")
        self.assertEqual(t5, 0.02)
        self.assertEqual(meg.position_km, 12.0)
        self.assertEqual(meg.energy, 43.0)
        self.assertFalse(meg.is_airborne)

        # When: hunt_fish()
        # Then: Успех. energy == 63.0, position_km == 12.0
        meg.hunt_fish()
        self.assertEqual(meg.energy, 63.0)
        self.assertEqual(meg.position_km, 12.0)
        self.assertFalse(meg.is_airborne)

        # When: pass_island(6)
        # Then: Обплыв по полукругу (6 > 4). Дуга 1.5 * 6 = 9.0 км. Время 9 / 50 = 0.18.
        t6 = meg.pass_island(6.0)
        self.assertEqual(t6, 0.18)
        self.assertEqual(meg.position_km, 21.0)
        self.assertEqual(meg.energy, 54.0)
        self.assertFalse(meg.is_airborne)

    def test_TC_S_002_no_double_hunting_at_same_point(self) -> None:
        """
        TC-S-002 (SPEC 4.2 Сценарий 2):
        Запрет повторной охоты при дефиците энергии.
        Итог: NoFishHere на повторном шаге, успех при продвижении на 2.0 км.
        """
        # Given: energy == 25.0, position_km == 0.0
        meg = RoboMeg("RoboMeg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0, energy=25.0)

        # When: move(3, "water") -> hunt_fish()
        meg.move(3.0, "water")
        self.assertEqual(meg.energy, 22.0)
        self.assertEqual(meg.position_km, 3.0)

        meg.hunt_fish()
        # Then: energy == 42.0, position_km == 3.0
        self.assertEqual(meg.energy, 42.0)
        self.assertEqual(meg.position_km, 3.0)

        # When: hunt_fish() повторно
        # Then: NoFishHere
        with self.assertRaises(NoFishHere):
            meg.hunt_fish()
        self.assertEqual(meg.energy, 42.0)
        self.assertEqual(meg.position_km, 3.0)

        # When: move(2, "water") -> hunt_fish()
        meg.move(2.0, "water")
        self.assertEqual(meg.energy, 40.0)
        self.assertEqual(meg.position_km, 5.0)

        meg.hunt_fish()
        # Then: Успех, energy == 60.0, position_km == 5.0
        self.assertEqual(meg.energy, 60.0)
        self.assertEqual(meg.position_km, 5.0)

    def test_TC_S_003_marine_obstacles_and_hunting(self) -> None:
        """
        TC-S-003 (SPEC 4.2 Сценарий 3):
        Штурм препятствий (водоворот, коралловый риф, айсберг).
        Итог: Все проверки can_overcome соответствуют ожиданиям.
        """
        # Given: bite_force_kn == 60.0, max_speed_kmh == 60.0, energy == 70.0
        meg = RoboMeg("RoboMeg", mass_kg=4000.0, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=60.0, energy=70.0)

        # When: move(10, "water")
        meg.move(10.0, "water")
        self.assertEqual(meg.energy, 60.0)
        self.assertEqual(meg.position_km, 10.0)
        self.assertTrue(meg.can_overcome("whirlpool"))
        self.assertFalse(meg.can_overcome("coral_reef"))

        # When: move(4, "air")
        meg.move(4.0, "air")
        self.assertEqual(meg.energy, 52.0)
        self.assertEqual(meg.position_km, 14.0)
        self.assertTrue(meg.can_overcome("coral_reef"))

        # When: move(25, "water")
        meg.move(25.0, "water")
        self.assertEqual(meg.energy, 27.0)
        self.assertEqual(meg.position_km, 39.0)
        self.assertFalse(meg.can_overcome("iceberg"))

        # When: hunt_fish()
        meg.hunt_fish()
        self.assertEqual(meg.energy, 47.0)
        self.assertEqual(meg.position_km, 39.0)
        self.assertTrue(meg.can_overcome("iceberg"))


if __name__ == "__main__":
    unittest.main()
