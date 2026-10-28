# ТЗ: Роботизированный мегалодон "RoboMeg"

Автор: Полякова Арина Витальевна
Стихия: вода
Проект: Роботизированный мегалодон "RoboMeg"

## 1. Назначение

Роботизированный мегалодон «RoboMeg» — автономный биомеханический подводный аппарат чёрного цвета с бронированной капсулой управления для одного пилота внутри корпуса. Предназначен для скоростного перемещения в водной среде, преодоления морских препятствий и совершения баллистических прыжков по воздуху через небольшие острова и преграды. Оснащён челюстным биореактором, позволяющим разрушать преграды и восполнять запас энергии за счёт охоты на рыбу в открытой воде.

![RoboMeg Concept](RoboMeg.png)

## 2. Стихия и конструкционный элемент

Стихия: вода

Конструкционный элемент: гидрореактивный хвостовой плавник и челюстной механизм с биореактором.

Как реализован элемент:
- Гидрореактивный хвостовой плавник определяет максимальную длину баллистического прыжка над водой за один импульс (атрибут `jump_length_km`). Прыжок выполняется толчком из воды; совершение повторного прыжка прямо из воздуха невозможно (`AlreadyAirborne`).
- Челюстной механизм с биореактором определяет силу укуса (атрибут `bite_force_kn`) для разрушения препятствий (айсбергов, стальных сетей) и позволяет восполнять энергию путём поедания рыбы (метод `hunt_fish`).

Ограничения стихии:
- Основной режим — движение в воде (индекс расхода энергии 1).
- Способен кратковременно переходить в воздушную среду при прыжке на расстояние не более `jump_length_km` (индекс расхода энергии 2). Повторный прыжок из воздуха без предварительного погружения в воду запрещён (`is_airborne == True`).
- Не предназначен для передвижения по суше (земле).

## 3. Публичный интерфейс

### 3.1. Класс
Имя класса: `RoboMeg`
Модуль: `robo_meg.py`

Константы класса:
- `HUNT_CIRCLE_DIAMETER_KM: float = 2.0` — фиксированный диаметр манёвра (круга) для охоты на рыбу, км.
- `HUNT_ENERGY_GAIN: float = 20.0` — чистый прирост энергии за один цикл охоты, условные единицы.
- `EPSILON: float = 1e-6` — допустимая погрешность при сравнении вещественных чисел (расход энергии).

### 3.2. Конструктор
```python
def __init__(
    self,
    name: str,
    mass_kg: float,
    jump_length_km: float,
    bite_force_kn: float,
    max_speed_kmh: float,
    energy: float = 100.0,
) -> None:
```

| Параметр | Тип | Единица | Допустимый диапазон | Значение по умолчанию |
|----------|-----|---------|---------------------|-----------------------|
| `name` | str | — | непустая строка | — |
| `mass_kg` | float | кг | > 0 | — |
| `jump_length_km` | float | км | > 0 | — |
| `bite_force_kn` | float | кН | > 0 | — |
| `max_speed_kmh` | float | км/ч | > 0 | — |
| `energy` | float | условные единицы | 0 ... 100 | 100.0 |

Исключения из конструктора:
- `TypeError` — если `name` не является строкой (`str`), либо числовые параметры не являются `int` или `float` (`bool` не допускается).
- `ValueError` — если `name` пустой или состоит только из пробелов.
- `ValueError` — если `mass_kg`, `jump_length_km`, `bite_force_kn` или `max_speed_kmh` <= 0.
- `ValueError` — если `energy` вне диапазона 0 ... 100.

### 3.3. Атрибуты

| Атрибут | Тип | Единица | Доступ | Описание |
|---------|-----|---------|--------|----------|
| `name` | str | — | чтение | Имя транспорта |
| `mass_kg` | float | кг | чтение | Масса аппарата |
| `jump_length_km` | float | км | чтение | Максимальная длина одного прыжка по воздуху |
| `bite_force_kn` | float | кН | чтение | Сила сжатия челюстей |
| `max_speed_kmh` | float | км/ч | чтение | Максимальная скорость в воде |
| `energy` | float | условные единицы | чтение | Текущий запас энергии |
| `position_km` | float | км | чтение | Пройденное расстояние по маршруту (по умолчанию 0.0) |
| `is_airborne` | bool | — | чтение | Находится ли аппарат в фазе прыжка в воздухе (по умолчанию False) |

### 3.4. Методы

#### 3.4.1. move
```python
def move(self, distance_km: float, terrain: str) -> float:
```
Назначение: перемещает мегалодон на заданное расстояние в указанной среде.
Параметры:
- `distance_km` — расстояние в км, > 0.
- `terrain` — среда: `"water"`, `"air"`, `"ground"`.
Возвращает: время перемещения в часах (`float`), округлённое до 6 знаков (`round(val, 6)`).
Изменяет: `position_km`, `energy`, `is_airborne`, а также счётчик проплытого расстояния в воде после прыжка.
Исключения:
- `TypeError` — при передаче параметров неверного типа (включая `bool`).
- `ValueError` — если `distance_km` <= 0 или `terrain` не из списка.
- `RoboMegCannotMoveOnGround` — при попытке движения по земле (`terrain == "ground"`).
- `AlreadyAirborne` — при попытке совершить прыжок (`terrain == "air"`), если аппарат уже находится в воздухе (`is_airborne == True`).
- `JumpTooLong` — при попытке прыжка по воздуху (`terrain == "air"`) на расстояние `distance_km > jump_length_km`.
- `EnergyEmpty` — если `energy + EPSILON` меньше затрат энергии на заданное расстояние.
Правила:
- В воде (`"water"`): скорость = `max_speed_kmh`, расход энергии = `distance_km * 1`. Сбрасывает `is_airborne = False`. Увеличивает счётчик проплытой в воде дистанции.
- В воздухе (`"air"`): прыжок возможен только из воды (`is_airborne == False`). Скорость = `max_speed_kmh * 2`, расход энергии = `distance_km * 2`. Устанавливает `is_airborne = True`. Сбрасывает счётчик проплытой воды в `0.0`.
- Вычисления `energy`, `position_km` и времени округляются до 6 знаков после запятой (`round(val, 6)`).
- При любом исключении состояние объекта не меняется.

#### 3.4.2. pass_island
```python
def pass_island(self, diameter_km: float) -> float:
```
Назначение: преодолевает встреченный на пути остров оптимальным способом.
Параметры:
- `diameter_km` — диаметр острова в км, > 0.
Возвращает: время преодоления острова в часах (`float`), округлённое до 6 знаков.
Изменяет: `position_km`, `energy`, `is_airborne`.
Исключения:
- `TypeError` — если `diameter_km` не число (`int`/`float`, `bool` запрещён).
- `ValueError` — если `diameter_km` <= 0.
- `AlreadyAirborne` — при попытке совершить перелёт, если `is_airborne == True`.
- `EnergyEmpty` — если текущего запаса `energy` недостаточно для выбранного манёвра.
Правила:
- Если `diameter_km <= jump_length_km`: мегалодон перепрыгивает остров по воздуху (`move(diameter_km, "air")`).
- Если `diameter_km > jump_length_km`: мегалодон обплывает остров по полукругу в воде на расстояние `arc_km = 1.5 * diameter_km` (`move(arc_km, "water")`). Время рассчитывается по формуле $t = \frac{1.5 \cdot \text{diameter\_km}}{\text{max\_speed\_kmh}}$.

#### 3.4.3. hunt_fish
```python
def hunt_fish(self) -> None:
```
Назначение: восполняет энергию на 20 единиц путём совершения кормового круга.
Параметры: нет.
Возвращает: `None`.
Изменяет: `energy` ($+20.0$, но не выше `100.0`), фиксирует текущую точку `position_km` как выловленную.
Детерминированный порядок проверок исключений (строгий приоритет):
1. `UnsafeHuntingZone` — если мегалодон находится в воздухе (`is_airborne == True`) или проплыл по воде после старта/последнего прыжка расстояние меньше `2.0` км.
2. `NoFishHere` — если на текущей координате `position_km` охота уже проводилась.
3. `RoboMegNotHungry` — если `energy >= 50.0`.

#### 3.4.4. can_overcome
```python
def can_overcome(self, obstacle: str) -> bool:
```
Назначение: проверяет возможность преодоления морского препятствия без изменения состояния объекта.
Параметры:
- `obstacle` — тип препятствия: `"coral_reef"`, `"iceberg"`, `"steel_net"`, `"whirlpool"`.
Правила:
- `"coral_reef"` — только если `is_airborne == True`.
- `"iceberg"` — только если `bite_force_kn > 50` и `energy > 30`.
- `"steel_net"` — если `is_airborne == True` ИЛИ `bite_force_kn > 25`.
- `"whirlpool"` — только если `is_airborne == False`, `max_speed_kmh >= 60` и `energy > 40`.

#### 3.4.5. calculate_energy
```python
def calculate_energy(self, distance_km: float, terrain: str) -> float:
```
Назначение: расчёт затрат энергии без изменения состояния.
Правила:
- Возвращает `round(distance_km * 1, 6)` для `"water"`, `round(distance_km * 2, 6)` для `"air"`.
- Для `"ground"` выбрасывает `RoboMegCannotMoveOnGround`.

#### 3.4.6. refuel
```python
def refuel(self, amount: float) -> None:
```
Назначение: пополнение энергии до максимума `100.0`. `amount` должен быть `> 0`.

#### 3.4.7. get_status
```python
def get_status(self) -> dict:
```
Возвращает снимок всех публичных атрибутов в виде словаря: `name`, `mass_kg`, `jump_length_km`, `bite_force_kn`, `max_speed_kmh`, `energy`, `position_km`, `is_airborne`.

## 4. Сценарии

### 4.1. Модульные тесты

#### Сценарий 1. Обычный заплыв в воде
Дано: мегалодон с `energy = 100`, `max_speed_kmh = 50`. Когда: `move(25, "water")`. Тогда:
- возвращается `0.5`;
- `position_km == 25.0`;
- `energy == 75.0`;
- `is_airborne == False`.

#### Сценарий 2. Прыжок через небольшой остров
Дано: мегалодон с `energy = 80`, `jump_length_km = 5`, `max_speed_kmh = 50`. Когда: `pass_island(3)`. Тогда:
- так как $3 \le 5$, остров преодолевается прыжком по воздуху;
- возвращается `0.03` (3 / (50 * 2));
- `position_km == 3.0`;
- `energy == 74.0` (80 - 3 * 2);
- `is_airborne == True`.

#### Сценарий 3. Обплыв крупного острова по полукругу
Дано: мегалодон с `energy = 80`, `jump_length_km = 5`, `max_speed_kmh = 50`. Когда: `pass_island(6)`. Тогда:
- так как $6 > 5$, мегалодон обплывает остров по полукругу длины `9.0` км ($1.5 \times 6$);
- возвращается `0.18` (9 / 50);
- `position_km == 9.0`;
- `energy == 71.0` (80 - 9 * 1);
- `is_airborne == False`.

#### Сценарий 4. Успешная охота на рыбу
Дано: мегалодон с `energy = 40`, проплывший по воде 5 км (`position_km == 5.0`, `is_airborne == False`). Когда: `hunt_fish()`. Тогда:
- `energy == 60.0` (40 + 20);
- `position_km == 5.0` (возврат в исходную точку после круга);
- `is_airborne == False`.

### 4.2. Функциональные тесты

#### Сценарий 1. Полный маршрут архипелага и охота после прыжка
- Given: Мегалодон на старте в воде: `position_km == 0.0`, `is_airborne == False`, `energy == 60.0`.
- When: Вызов `pass_island(3)`.
- Then: Прыжок по воздуху. `position_km == 3.0`, `energy == 54.0`, `is_airborne == True`.
- When: Вызов `hunt_fish()`.
- Then: `UnsafeHuntingZone` (из-за фазы прыжка `is_airborne == True`).
- When: `move(5, "water")`.
- Then: `position_km == 8.0`, `energy == 49.0`, `is_airborne == False`.
- When: `pass_island(2)`.
- Then: Прыжок. `position_km == 10.0`, `energy == 45.0`, `is_airborne == True`.
- When: `move(1, "water")`.
- Then: `position_km == 11.0`, `energy == 44.0`, `is_airborne == False`.
- When: `hunt_fish()`.
- Then: `UnsafeHuntingZone` (проплыто 1 км по воде после прыжка, нужно >= 2.0 км).
- When: `move(1, "water")`.
- Then: `position_km == 12.0`, `energy == 43.0`, проплыто 2 км по воде.
- When: `hunt_fish()`.
- Then: Успех. `energy == 63.0`, `position_km == 12.0`.
- When: `pass_island(6)`.
- Then: Обплыв по полукругу ($6 > 4$). Путь $1.5 \times 6 = 9.0$ км. Итог: `position_km == 21.0`, `energy == 54.0`, `is_airborne == False`.

#### Сценарий 2. Запрет повторной охоты
- Given: `energy == 25.0`, `position_km == 0.0`.
- When: `move(3, "water")` -> `hunt_fish()`.
- Then: `energy == 42.0`, `position_km == 3.0`.
- When: `hunt_fish()` повторно.
- Then: `NoFishHere`.
- When: `move(2, "water")` -> `hunt_fish()`.
- Then: Успех, `energy == 60.0`, `position_km == 5.0`.

#### Сценарий 3. Штурм препятствий
- Given: `bite_force_kn == 60.0`, `max_speed_kmh == 60.0`, `energy == 70.0`.
- When: `move(10, "water")`. `can_overcome("whirlpool")` -> `True`, `can_overcome("coral_reef")` -> `False`.
- When: `move(4, "air")`. `can_overcome("coral_reef")` -> `True`.
- When: `move(25, "water")`. `energy == 27.0`, `can_overcome("iceberg")` -> `False` ($27 \le 30$).
- When: `hunt_fish()`. `energy == 47.0`, `can_overcome("iceberg")` -> `True` ($47 > 30$).

## 5. Граничные случаи
- `move(0, "water")` или `pass_island(0)` -> `ValueError`.
- `move(4, "air")` при `jump_length_km == 4` -> Успешно.
- `move(4.1, "air")` при `jump_length_km == 4` -> `JumpTooLong`.
- `move(1, "air")` при `is_airborne == True` -> `AlreadyAirborne`.
- `hunt_fish()` при `energy == 50.0` -> `RoboMegNotHungry` (требуется строго `< 50.0`).
- Округление значений `round(val, 6)` исключает ложное выбрасывание `EnergyEmpty` при вычислениях с плавающей точкой.

## 6. Исключения и иерархия

### 6.1. Иерархия
```text
Exception
├── TypeError
├── ValueError
└── RuntimeError
    └── CrazyVehicleError
        └── RoboMegError
            ├── EnergyEmpty
            ├── RoboMegCannotMoveOnGround
            ├── AlreadyAirborne
            ├── JumpTooLong
            ├── RoboMegNotHungry
            ├── UnsafeHuntingZone
            └── NoFishHere
```

### 6.2. Таблица проверок и текстов ошибок
| Ситуация | Исключение | Сообщение |
|---|---|---|
| Неверный тип параметров | TypeError | `<parameter> must be a string / number` |
| Пустое имя | ValueError | `name must not be empty` |
| Неположительные числовые параметры | ValueError | `<parameter> must be positive` |
| Некорректная энергия | ValueError | `energy must be between 0 and 100` |
| Движение по земле | RoboMegCannotMoveOnGround | `robomeg cannot move on ground` |
| Прыжок из воздуха | AlreadyAirborne | `cannot jump while already airborne` |
| Превышение длины прыжка | JumpTooLong | `jump distance exceeds max jump length` |
| Нехватка энергии | EnergyEmpty | `not enough energy` |
| Охота при `is_airborne` или пути < 2 км | UnsafeHuntingZone | `must swim at least 2.0 km in water before hunting` |
| Повторная охота в той же точке | NoFishHere | `fish already eaten at position` |
| Охота при `energy >= 50` | RoboMegNotHungry | `energy is 50 or above, hunting is not needed` |