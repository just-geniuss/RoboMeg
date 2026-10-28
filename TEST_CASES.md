# Test Case Specification: Роботизированный мегалодон «RoboMeg»

Базовый мегалодон (если не сказано иное): `RoboMeg("RoboMeg", mass_kg=4000, jump_length_km=4.0, bite_force_kn=60.0, max_speed_kmh=50.0, energy=100.0)`.

Соотношение: 29 модульных / 3 сценарных (\~91% / 9%).

## Модульные тесты

| ID | Тип | Источник | Предусловие | Вход | Ожидание | Приоритет | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| TC-M-001 | module | SPEC 3.1, 3.2, 3.3 | — | создание `RoboMeg` с валидными параметрами | атрибуты сохранены; `position_km == 0.0`, `is_airborne == False` | high | 
| TC-M-002 | module | SPEC 3.2, 6.2 | — | `name=""` / `name="   "` | `ValueError` | high | 
| TC-M-003 | module | SPEC 3.2, 6.2 | — | `mass_kg=0`, `jump_length_km=-1`, `bite_force_kn=0`, `max_speed_kmh=-5` | `ValueError` | high | 
| TC-M-004 | module | SPEC 3.2, 6.2 | — | `energy=-0.1` / `100.1`; `energy=0` / `100`; без `energy` | `-0.1` и `100.1` → `ValueError`; `0` и `100` OK; без energy → `100.0` | high | 
| TC-M-005 | module | SPEC 3.3 | — | изменение `name`, `mass_kg`, `jump_length_km`, `bite_force_kn`, `max_speed_kmh`, `energy`, `position_km`, `is_airborne` | `AttributeError` для всех 8 атрибутов | high | 
| TC-M-006 | module | SPEC 3.4.1 | — | `move(25, "water")` | `0.5`; `position_km == 25.0`, `energy == 75.0`, `is_airborne == False` | high | 
| TC-M-007 | module | SPEC 3.4.1 | — | `move(4, "air")` при `jump_length_km == 4` | `0.04`; `position_km == 4.0`, `energy == 92.0`, `is_airborne == True` | high | 
| TC-M-008a | module | SPEC 3.4.1 | — | `move(4.1, "air")` при `jump_length_km == 4` | `JumpTooLong`; состояние не меняется | high | 
| TC-M-008b | module | SPEC 3.4.1 | `move(2, "air")` | повторный `move(1, "air")` в воздухе | `AlreadyAirborne`; состояние не меняется | high | 
| TC-M-009 | module | SPEC 3.4.1 | — | `move(1, "ground")` | `RoboMegCannotMoveOnGround`; состояние не меняется | high | 
| TC-M-010a | module | SPEC 3.4.1 | `energy=10` | `move(15, "water")` / `move(10, "water")` | `EnergyEmpty`; / успешно, `energy == 0.0` | high | 
| TC-M-010b | module | SPEC 3.4.2 | `energy=5` / `energy=8` / `energy=9` | `pass_island(4)` прыжок (нужно 8) / `pass_island(6)` обплыв (нужно 9) | `EnergyEmpty` / успешно `energy == 0.0` (прыжок) / успешно `energy == 0.0` (обплыв) | high | 
| TC-M-010c | module | SPEC 3.4.1, 3.5 | `energy=0.3` | `move(0.1, "water")` ×3 | все 3 движения успешны, `energy == 0.0` без ложного `EnergyEmpty` из-за float | medium | 
| TC-M-011 | module | SPEC 3.4.2 | — | `pass_island(4)` при `jump_length_km == 4` | прыжок: `0.04`; `position_km == 4.0`, `energy == 92.0`, `is_airborne == True` | high | 
| TC-M-012 | module | SPEC 3.4.2 | — | `pass_island(6)` при `jump_length_km == 4` | обплыв: `0.18`; `position_km == 9.0`, `energy == 91.0`, `is_airborne == False` | high | 
| TC-M-013 | module | SPEC 3.4.3 | `energy=40`, `move(5, "water")` | `hunt_fish()` | `energy == 60.0`, `position_km == 5.0`, `is_airborne == False` | high | 
| TC-M-014 | module | SPEC 3.4.3 | `energy=50.0`, `move(5, "water")` | `hunt_fish()` | `RoboMegNotHungry`; состояние не меняется | high | 
| TC-M-015 | module | SPEC 3.4.3 | `energy=40` на старте / `move(1, "water")` | `hunt_fish()` | `UnsafeHuntingZone`; состояние не меняется | high | 
| TC-M-016 | module | SPEC 3.4.3 | вызов `hunt_fish()` успешно | повторный `hunt_fish()` на той же позиции | `NoFishHere`; состояние не меняется | high | 
| TC-M-017 | module | SPEC 3.4.3 | `energy=60`, в воздухе, на старте | `hunt_fish()` | `UnsafeHuntingZone` (проверка детерминированного приоритета исключений) | high | 
| TC-M-018 | module | SPEC 3.4.4 | в воде / в воздухе | `can_overcome("coral_reef")` | `False` / `True` | medium | 
| TC-M-019 | module | SPEC 3.4.4 | `bite_force_kn=50` / `energy=30` / `bite_force_kn=60` & `energy=31` | `can_overcome("iceberg")` | `False` / `False` / `True` | medium | 
| TC-M-020 | module | SPEC 3.4.4 | `max_speed_kmh=59` / `energy=40` / в воздухе / `max_speed_kmh=60` & `energy=41` | `can_overcome("whirlpool")` | `False` / `False` / `False` / `True` | medium | 
| TC-M-021 | module | SPEC 3.4.4 | — | `can_overcome("unknown")` | `ValueError` | medium | 
| TC-M-022 | module | SPEC 3.4.5 | — | `calculate_energy(10, "water")` / `calculate_energy(1, "ground")` | `10.0` / `RoboMegCannotMoveOnGround` | high | 
| TC-M-023 | module | SPEC 3.4.6 | `energy=50` | `refuel(30)` / `refuel(1000)` / `refuel(-5)` | `energy == 80.0` / `energy == 100.0` / `ValueError` | high | 
| TC-M-024 | module | SPEC 3.4.7 | — | `get_status()` | полный словарь из 8 актуальных ключей | medium | 
| TC-M-025 | module | SPEC 3.2, 6.2 | — | `name=123`, `mass_kg="4000"`, `energy=True` | `TypeError` | medium | 
| TC-M-026 | module | SPEC 4.1 | — | проверка наследования | `RoboMegError -> CrazyVehicleError -> RuntimeError` | medium | 
| TC-M-027 | module | SPEC 6.2 | — | вызов исключений | сообщение соответствует шаблонам из 6.2 | medium | 

## Сценарные тесты

| ID | Тип | Источник | Вход | Ожидание | Приоритет | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| TC-S-001 | scenario | SPEC 4.2 Сценарий 1 | Полный маршрут архипелага и охота после прыжка | `position_km == 21.0`, `energy == 54.0`, `is_airborne == False` | high | 
| TC-S-002 | scenario | SPEC 4.2 Сценарий 2 | Проверка запрета двойной охоты при дефиците энергии | `NoFishHere` на повторном шаге, успех при продвижении на `2.0` км | high | 
| TC-S-003 | scenario | SPEC 4.2 Сценарий 3 | Штурм водоворота, кораллового рифа и айсберга | Все проверки `can_overcome` соответствуют ожиданиям | high | 
