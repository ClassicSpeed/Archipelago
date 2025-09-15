import re
from enum import Enum, auto
from typing import List

SADX_BASE_ID = 543800000


def pascal_to_space(s):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', ' ', s)


class Character(Enum):
    Sonic = 1
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


def remove_character_suffix(string: str) -> str:
    for character in Character:
        if string.endswith(f" ({character.name})"):
            return re.sub(rf" \({character.name}\)$", "", string)
    return string


EVERYONE: List[Character] = [Character.Sonic, Character.Tails, Character.Knuckles,
                             Character.Amy, Character.Big, Character.Gamma]
SONIC_TAILS: List[Character] = [Character.Sonic, Character.Tails]
FLYERS: List[Character] = [Character.Tails, Character.Knuckles]


class Upgrade(Enum):
    LightShoes = auto()
    CrystalRing = auto()
    AncientLight = auto()
    JetAnkle = auto()
    RhythmBadge = auto()
    ShovelClaw = auto()
    FightingGloves = auto()
    LongHammer = auto()
    WarriorFeather = auto()
    JetBooster = auto()
    LaserBlaster = auto()
    LifeBelt = auto()
    PowerRod = auto()
    Lure1 = auto()
    Lure2 = auto()
    Lure3 = auto()
    Lure4 = auto()


class Enemy(Enum):
    BoaBoa = 1
    Buyon = auto()
    CopSpeeder = auto()
    ElectroSpinner = auto()
    EggKeeper = auto()
    Gola = auto()
    IceBall = auto()
    KartKiki = auto()
    Kiki = auto()
    Leon = auto()
    Rhinotank = auto()
    Spinner = auto()
    Sweep = auto()
    SpikySpinner = auto()


class Capsule(Enum):
    ExtraLife = 1
    Shield = auto()
    MagneticShield = auto()
    SpeedUp = auto()
    Invincibility = auto()
    Bomb = auto()
    FiveRings = auto()
    TenRings = auto()
    RandomRings = auto()


class Fish(Enum):
    AnglerFish = 0
    Hammerhead = auto()
    StripedBeakfish = auto()
    BlueMarlin = auto()
    MechaFish = auto()
    LargemouthBass = auto()
    Piranha = auto()
    Oarfish = auto()
    Salmon = auto()
    Shark = auto()
    SeaBass = auto()
    Coelacanth = auto()
    RedSeaBream = auto()
    JapaneseEel = auto()
    MorayEel = auto()


class SubLevelMission(Enum):
    B = 0
    A = auto()
    Sonic = auto()
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


class LevelMission(Enum):
    C = 0
    B = auto()
    A = auto()
    S = auto()


class SubLevel(Enum):
    SandHill = auto()
    TwinkleCircuit = auto()
    SkyChaseAct1 = auto()
    SkyChaseAct2 = auto()


class AdventureField(Enum):
    StationSquare = auto()
    MysticRuins = auto()
    EggCarrier = auto()
    Past = auto()


class Area(Enum):
    CityHall = 0
    Station = auto()
    Casino = auto()
    Sewers = auto()
    SSMain = auto()
    TPTunnel = auto()
    Hotel = auto()
    HotelPool = auto()
    TPLobby = auto()
    MRMain = auto()
    AngelIsland = auto()
    IceCave = auto()
    PastAltar = auto()
    PastMain = auto()
    Jungle = auto()
    FinalEggTower = auto()
    ECOutside = auto()
    ECBridge = auto()
    ECDeck = auto()
    CaptainRoom = auto()
    PrivateRoom = auto()
    ECPool = auto()
    Arsenal = auto()
    ECInside = auto()
    HedgehogHammer = auto()
    PrisonHall = auto()
    WaterTank = auto()
    WarpHall = auto()
    SSChaoGarden = auto()
    MRChaoGarden = auto()
    ECChaoGarden = auto()
    EmeraldCoast = auto()
    WindyValley = auto()
    Casinopolis = auto()
    IceCap = auto()
    TwinklePark = auto()
    SpeedHighway = auto()
    RedMountain = auto()
    SkyDeck = auto()
    LostWorld = auto()
    FinalEgg = auto()
    HotShelter = auto()
    Chaos0 = auto()
    EggWalker = auto()
    Chaos2 = auto()
    TwinkleCircuit = auto()
    Chaos4 = auto()
    EggHornet = auto()
    SkyChase1 = auto()
    SandHill = auto()
    BetaEggViper = auto()
    SkyChase2 = auto()
    Chaos6ZeroBeta = auto()


level_areas = [
    Area.EmeraldCoast,
    Area.WindyValley,
    Area.Casinopolis,
    Area.IceCap,
    Area.TwinklePark,
    Area.SpeedHighway,
    Area.RedMountain,
    Area.SkyDeck,
    Area.LostWorld,
    Area.FinalEgg,
    Area.HotShelter
]
