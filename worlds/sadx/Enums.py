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

    def __lt__(self, other):
        if isinstance(other, Area):
            return self.value < other.value
        return NotImplemented


class AreaConnection(Enum):
    # City Hall
    CityHall_to_SSMain = (Area.CityHall, Area.SSMain)
    CityHall_to_Sewers = (Area.CityHall, Area.Sewers)
    CityHall_to_SpeedHighway = (Area.CityHall, Area.SpeedHighway)
    CityHall_to_Chaos0 = (Area.CityHall, Area.Chaos0)

    # Station + Casino
    Station_to_SSMain = (Area.Station, Area.SSMain)
    Station_to_MrMain = (Area.Station, Area.MRMain)
    Station_to_Casinopolis = (Area.Station, Area.Casinopolis)
    Station_to_Hotel = (Area.Station, Area.Hotel)
    Station_to_EggWalker = (Area.Station, Area.EggWalker)

    # Sewers
    Sewers_to_CityHall = (Area.Sewers, Area.CityHall)
    Sewers_to_SSMain = (Area.Sewers, Area.SSMain)

    # SSMain
    SSMain_to_Hotel = (Area.SSMain, Area.Hotel)
    SSMain_to_Station = (Area.SSMain, Area.Station)
    SSMain_to_CityHall = (Area.SSMain, Area.CityHall)
    SSMain_to_TwinkleParkLobby = (Area.SSMain, Area.TPLobby)
    SSMain_to_EcOutside = (Area.SSMain, Area.ECOutside)
    SSMain_to_Bridge = (Area.SSMain, Area.ECBridge)
    SSMain_to_Sewers = (Area.SSMain, Area.Sewers)
    SSMain_to_SpeedHighway = (Area.SSMain, Area.SpeedHighway)

    # Hotel
    Hotel_to_SSMain = (Area.Hotel, Area.SSMain)
    Hotel_to_Station = (Area.Hotel, Area.Station)
    Hotel_to_EmeraldCoast = (Area.Hotel, Area.EmeraldCoast)
    Hotel_to_SsChaoGarden = (Area.Hotel, Area.SSChaoGarden)
    Hotel_to_Chaos2 = (Area.Hotel, Area.Chaos2)

    # Twinkle Park Lobby
    TwinkleParkLobby_to_SSMain = (Area.TPLobby, Area.SSMain)
    TwinkleParkLobby_to_TwinklePark = (Area.TPLobby, Area.TwinklePark)
    TwinkleParkLobby_to_TwinkleCircuit = (Area.TPLobby, Area.TwinkleCircuit)

    # MRMain
    MrMain_to_SSMain = (Area.MRMain, Area.SSMain)
    MrMain_to_EcOutside = (Area.MRMain, Area.ECOutside)
    MrMain_to_Bridge = (Area.MRMain, Area.ECBridge)
    MrMain_to_AngelIsland = (Area.MRMain, Area.AngelIsland)
    MrMain_to_WindyValley = (Area.MRMain, Area.WindyValley)
    MrMain_to_Jungle = (Area.MRMain, Area.Jungle)
    MrMain_to_Chaos4 = (Area.MRMain, Area.Chaos4)
    MrMain_to_EggHornet = (Area.MRMain, Area.EggHornet)
    MrMain_to_MrChaoGarden = (Area.MRMain, Area.MRChaoGarden)
    MrMain_to_SkyChase1 = (Area.MRMain, Area.SkyChase1)

    # Angel Island
    AngelIsland_to_MrMain = (Area.AngelIsland, Area.MRMain)
    AngelIsland_to_IceCap = (Area.AngelIsland, Area.IceCap)
    AngelIsland_to_RedMountain = (Area.AngelIsland, Area.RedMountain)
    AngelIsland_to_PastAltar = (Area.AngelIsland, Area.PastAltar)

    # Past Altar
    PastAltar_to_AngelIsland = (Area.PastAltar, Area.AngelIsland)
    PastAltar_to_PastMain = (Area.PastAltar, Area.PastMain)

    # Past Main
    PastMain_to_PastAltar = (Area.PastMain, Area.PastAltar)
    PastMain_to_Jungle = (Area.PastMain, Area.Jungle)

    # Jungle
    Jungle_to_MrMain = (Area.Jungle, Area.MRMain)
    Jungle_to_LostWorld = (Area.Jungle, Area.LostWorld)
    Jungle_to_LostWorldAlternative = (Area.Jungle, Area.LostWorld)
    Jungle_to_FinalEggTower = (Area.Jungle, Area.FinalEggTower)
    Jungle_to_SandHill = (Area.Jungle, Area.SandHill)
    Jungle_to_PastMain = (Area.Jungle, Area.PastMain)

    # Final Egg Tower
    FinalEggTower_to_Jungle = (Area.FinalEggTower, Area.Jungle)
    FinalEggTower_to_FinalEgg = (Area.FinalEggTower, Area.FinalEgg)
    FinalEggTower_to_FinalEggAlternative = (Area.FinalEggTower, Area.FinalEgg)
    FinalEggTower_to_BetaEggViper = (Area.FinalEggTower, Area.BetaEggViper)
    FinalEggTower_to_EcInside = (Area.FinalEggTower, Area.ECInside)
    # Egg Carrier Outside (Untransformed)
    EcOutside_to_SSMain = (Area.ECOutside, Area.SSMain)
    EcOutside_to_MrMain = (Area.ECOutside, Area.MRMain)
    EcOutside_to_SkyChase2 = (Area.ECOutside, Area.SkyChase2)
    EcOutside_to_Chaos6ZeroBeta = (Area.ECOutside, Area.Chaos6ZeroBeta)
    EcOutside_to_EcInsideMonorail = (Area.ECOutside, Area.ECInside)
    EcOutside_to_EcInsideEggLift = (Area.ECOutside, Area.ECInside)
    EcOutside_to_CaptainRoom = (Area.ECOutside, Area.CaptainRoom)
    EcOutside_to_Pool = (Area.ECOutside, Area.ECPool)

    # Bridge (Transformed)
    Bridge_to_SSMain = (Area.ECBridge, Area.SSMain)
    Bridge_to_MrMain = (Area.ECBridge, Area.MRMain)
    Bridge_to_SkyDeck = (Area.ECBridge, Area.SkyDeck)
    Bridge_to_SkyChase2 = (Area.ECBridge, Area.SkyChase2)
    Bridge_to_Chaos6ZeroBeta = (Area.ECBridge, Area.Chaos6ZeroBeta)
    Bridge_to_EcInsideMonorail = (Area.ECBridge, Area.ECInside)

    # Deck (Transformed)
    Deck_to_Pool = (Area.ECDeck, Area.ECPool)
    Deck_to_CaptainRoom = (Area.ECDeck, Area.CaptainRoom)
    Deck_to_PrivateRoom = (Area.ECDeck, Area.PrivateRoom)
    Deck_to_PrivateRoomAlternative = (Area.ECDeck, Area.PrivateRoom)
    Deck_to_EcInsideEggLift = (Area.ECDeck, Area.ECInside)

    # Captain Room
    CaptainRoom_to_EcOutside = (Area.CaptainRoom, Area.ECOutside)
    CaptainRoom_to_Deck = (Area.CaptainRoom, Area.ECDeck)
    CaptainRoom_to_PrivateRoom = (Area.CaptainRoom, Area.PrivateRoom)

    # Private Room
    PrivateRoom_to_CaptainRoom = (Area.PrivateRoom, Area.CaptainRoom)
    PrivateRoom_to_Deck = (Area.PrivateRoom, Area.ECDeck)
    PrivateRoom_to_DeckAlternative = (Area.PrivateRoom, Area.ECDeck)

    # Pool
    Pool_to_EcOutside = (Area.ECPool, Area.ECOutside)
    Pool_to_Deck = (Area.ECPool, Area.ECDeck)
    Pool_to_SkyDeck = (Area.ECPool, Area.SkyDeck)

    # Arsenal
    Arsenal_to_EcInside = (Area.Arsenal, Area.ECInside)

    # Egg Carrier Inside
    EcInside_to_EcOutsideEggLift = (Area.ECInside, Area.ECOutside)
    EcInside_to_EcOutsideMonorail = (Area.ECInside, Area.ECOutside)
    EcInside_to_DeckEggLift = (Area.ECInside, Area.ECDeck)
    EcInside_to_BridgeMonorail = (Area.ECInside, Area.ECBridge)
    EcInside_to_HotShelter = (Area.ECInside, Area.HotShelter)
    EcInside_to_HedgehogHammer = (Area.ECInside, Area.HedgehogHammer)
    EcInside_to_FinalEggTower = (Area.ECInside, Area.FinalEggTower)
    EcInside_to_WarpHall = (Area.ECInside, Area.WarpHall)
    EcInside_to_Arsenal = (Area.ECInside, Area.Arsenal)
    EcInside_to_WaterTank = (Area.ECInside, Area.WaterTank)

    # Hedgehog Hammer
    HedgehogHammer_to_EcInside = (Area.HedgehogHammer, Area.ECInside)
    HedgehogHammer_to_PrisonHall = (Area.HedgehogHammer, Area.PrisonHall)

    # Prison Hall
    PrisonHall_to_HedgehogHammer = (Area.PrisonHall, Area.HedgehogHammer)

    # Water Tank
    WaterTank_to_EcInside = (Area.WaterTank, Area.ECInside)

    # Warp Hall
    WarpHall_to_EcInside = (Area.WarpHall, Area.ECInside)
    WarpHall_to_EcChaoGarden = (Area.WarpHall, Area.ECChaoGarden)

    def __init__(self, area1, area2):
        self.area1 = area1
        self.area2 = area2

    @classmethod
    def from_areas(cls, area1, area2):
        for connection in cls:
            if {connection.area1, connection.area2} == {area1, area2}:
                return connection
        return None

    def get_index(self):
        return list(self.__class__.__members__).index(self.name)


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
