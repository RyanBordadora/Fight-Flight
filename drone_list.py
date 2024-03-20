from classes import *

def drone_bank(plane, weapon2):
    gun = Gun('Gun', 1,'sound/GUN.wav', 999, 100)
    plsl = Gun('PLSL', 2,'sound/PLSL.wav', 150, 700)
    if plane == 0:
            IEWS = Self_Duration("IEWS", cooldown= 20000, duration=5)
            return Drone('KR', 100, gun, weapon2, IEWS, "WOC")
    elif plane == 1:
            EC = Self_Duration("EC", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, gun, weapon2, EC, "WOC")
    elif plane == 2:
            ADA = Self_Duration("ADA", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, gun, weapon2, ADA, "WOC")
    elif plane == 3:
            OV = Opp_Duration("OV", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, gun, weapon2, OV, "WOC")
    elif plane == 4:
            DP = Opp_Duration("DP", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, plsl, weapon2, DP, "WOC")
    elif plane == 5:
            EL = Opp_Duration("EL", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, plsl, weapon2, EL, "WOC")
    elif plane == 6:
            ES = Self_Duration("ES", cooldown= 20000, duration=5)
            return Drone('Drone1', 100, gun, weapon2, ES, "WOC")
    elif plane == 7:
            NR = Self_Instant("NR", 20000, 25)
            return Drone('Drone1', 100, gun, weapon2, NR, "WOC")
    
def drone_list(plane):
    if plane == 0:
            return "King Raptor"
    elif plane == 1:
            return "Alpha Aurora"
    elif plane == 2:
            return "Shinden Vindicator"
    elif plane == 3:
            return "Crimson Chimera"
    elif plane == 4:
            return "Falken Viper"
    elif plane == 5:
            return "Avatar Morgan"
    elif plane == 6:
            return "ASX-03 Nosferatu"
    elif plane == 7:
            return "ASX-09 Wyvern"
    
def faction_list(plane):
        if plane == 0 or plane == 1:
                return "Wings of Corona"
        elif plane == 2 or plane == 3:
                return "Steel Talons"
        elif plane == 4 or plane == 5:
                return "Garm Corps"
        elif plane == 6 or plane == 7:
                return "Foehn Wind"
        else: return "ERROR"