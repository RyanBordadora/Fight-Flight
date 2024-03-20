from classes import *

def weapon_bank(plane, weapon):
    if plane == 0:
        if weapon == 0:
            return Projectile("QAAM", 30, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 1:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 2:
            return Hitscan('EPL', 4, 'sound/EML.wav', 200, cooldown=1000, leech=500)
        elif weapon == 3:
            return Beam('HPME', 3, 'sound/TLS.wav', 500, cooldown=5000, time=1000, drain = 100, leech = 10)
        elif weapon == 4:
            return Projectile("LRBM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
    elif plane == 1:
        if weapon == 0:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 1:
            return Hitscan('EPL', 4, 'Missle.mp3', 200, cooldown=1000, leech=500)
        elif weapon == 2:
            return Beam('HPME', 3, 'sound/TLS.wav', 500, cooldown=5000, time=1000, drain = 100, leech = 10)
        elif weapon == 3:
            return Projectile("LRBM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
    elif plane == 2:
        if weapon == 0:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 1:
            return Projectile("HCAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 2:
            return Projectile("HPAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 3:
            return Projectile("HVAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 4:
            return Gun('MGP', 10,'sound/GUN.wav', 500)
        elif weapon == 5:
            return Projectile("SAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
    elif plane == 3:
        if weapon == 0:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 1:
            return Projectile("HCAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 2:
            return Projectile("HPAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 3:
            return Projectile("HVAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
        elif weapon == 4:
            return Gun('MGP', 10,'sound/GUN.wav', 500)
        elif weapon == 5:
            return Projectile("SAAM", 10, 'Missle.mp3', 10, cooldown=4000, precision=90, time=1000, drain=2000)
    elif plane == 4:
        if weapon == 0:
            return Gun('SPB', 10,'sound/GUN.wav', 500)
        elif weapon == 1:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 2:
            return Beam("HLC", 7.5, 'sound/TLS.wav', 30, cooldown=5000, time=2000, drain=0, leech=1000)
        elif weapon == 3:
            return Beam("IIC", 7.5, 'sound/TLS.wav', 10, cooldown=5000, time=2000, drain=0, leech=1000)
    elif plane == 5:
        if weapon == 0:
            return Beam("TLS", 7.5, 'sound/TLS.wav', 10, cooldown=5000, time=2000, drain=0, leech=1000)
        elif weapon == 1:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 2:
            return Beam("HLC", 7.5, 'sound/TLS.wav', 30, cooldown=5000, time=2000, drain=0, leech=1000)
        elif weapon == 3:
            return Beam("IIC", 7.5, 'sound/TLS.wav', 10, cooldown=5000, time=2000, drain=0, leech=1000)
    elif plane == 6:
        if weapon == 0:
            return Hitscan('UAV', 4, 'Missle.mp3', 200, cooldown=1000, leech=500)
        elif weapon == 1:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 2:
            return Beam("CPC", 7.5, 'sound/TLS.wav', 10, cooldown=5000, time=2000, drain=0, leech=1000) 
        elif weapon == 3:
            return Hitscan('PEML', 4, 'Missle.mp3', 200, cooldown=1000, leech=500)
    elif plane == 7:
        if weapon == 0:
            return Hitscan('EML', 4, 'sound/EML.wav', 200, cooldown=1000, leech=500)
        elif weapon == 1:
            return Projectile("AAM", 20, 'Missle.mp3', 20, cooldown=4000, precision=50, time=2000, drain=1000)
        elif weapon == 2:
            return Beam("CPC", 7.5, 'sound/TLS.wav', 10, cooldown=5000, time=2000, drain=0, leech=1000) 
        elif weapon == 3:
            return Hitscan('PEML', 4, 'sound/EML.wav', 200, cooldown=1000, leech=500)
        
from classes import *

def weapon_list(plane, weapon):
    if plane == 0:
        if weapon == 0:
            return "QAAM"
        elif weapon == 1:
            return "AAM"
        elif weapon == 2:
            return "EPL"
        elif weapon == 3:
            return "HPME"
        elif weapon == 4:
            return "LRBM"
    elif plane == 1:
        if weapon == 0:
            return "AAM"
        elif weapon == 1:
            return "EPL"
        elif weapon == 2:
            return "HPME"
        elif weapon == 3:
            return "LRBM"
    elif plane == 2:
        if weapon == 0:
            return "AAM"
        elif weapon == 1:
            return "HCAAM"
        elif weapon == 2:
            return "HPAAM"
        elif weapon == 3:
            return "HVAAM"
        elif weapon == 4:
            return "MGP"
        elif weapon == 5:
            return "SAAM"
    elif plane == 3:
        if weapon == 0:
            return "AAM"
        elif weapon == 1:
            return "HCAAM"
        elif weapon == 2:
            return "HPAAM"
        elif weapon == 3:
            return "HVAAM"
        elif weapon == 4:
            return "MGP"
        elif weapon == 5:
            return "SAAM"
    elif plane == 4:
        if weapon == 0:
            return "SPB"
        elif weapon == 1:
            return "AAM"
        elif weapon == 2:
            return "HLC"
        elif weapon == 3:
            return "IIC"
    elif plane == 5:
        if weapon == 0:
            return "TLS"
        elif weapon == 1:
            return "AAM"
        elif weapon == 2:
            return "HLC"
        elif weapon == 3:
            return "IIC"
    elif plane == 6:
        if weapon == 0:
            return "UAV"
        elif weapon == 1:
            return "AAM"
        elif weapon == 2:
            return "CPC"
        elif weapon == 3:
            return "PEML"
    elif plane == 7:
        if weapon == 0:
            return "EML"
        elif weapon == 1:
            return "AAM"
        elif weapon == 2:
            return "CPC"
        elif weapon == 3:
            return "PEML"