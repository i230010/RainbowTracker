"""
main.py file for the RainbowTracker 
-----------------------------------
This file includes the calculations for the position of the rainbow, 3d rendering and the program to run the app
"""

#Required modules
from skyfield.api import load, GREGORIAN_START, wgs84, N, E

def opposite_alt(deg: float) -> float:
    """
    The Opposite of an Altitude

    Parameters
    ----------
    Altitude in degrees

    Returns
    -------
    Opposite of Altitude in degrees
    """
    return deg * -1

def opposite_az(deg: float) -> float:
    """
    The Opposite of an Azimuth

    Parameters
    ----------
    Azimuth in degrees

    Returns
    -------
    Opposite of Azimuth in degrees
    """
    return (deg - 180) % 360

def main():
    #Observers coordinates
    lat: float = 3.14
    lon: float = 101.6

    print("RainbowTracker App Log(s):")

    #Load Epehemerides
    eph = load("de421.bsp")

    #Load Timescale
    ts = load.timescale()
    ts.julian_calendar_cutoff = GREGORIAN_START
    t = ts.now()

    #Object positions in Geocentric and Localized
    earth, sun, moon = eph["earth"], eph["sun"], eph["moon"] #Geocentric
    observer = earth + wgs84.latlon(lat * N, lon * E) #Localized

    #Sun's RaDec
    sradec = earth.at(t).observe(sun).radec()
    mradec = earth.at(t).observe(moon).radec()

    #Moon's RaDec
    saltaz = observer.at(t).observe(sun).apparent().altaz()
    maltaz = observer.at(t).observe(moon).apparent().altaz()

    print(f"Sun RaDec Skyfield: {sradec}")
    print(f"Moon RaDec Skyfield: {mradec}")

    print(f"Sun AltAz Skyfield: {saltaz}")
    print(f"Moon AltAz Skyfield: {maltaz}")

    #Sun's RaDec into Ra Dec Components
    ra_sun: float = sradec[0].degrees
    dec_sun: float = sradec[1].degrees

    #Moon's RaDec into Ra Dec Components
    ra_moon: float = mradec[0].degrees
    dec_moon: float = mradec[1].degrees

    print(f"RaDec Sun (deg): {ra_sun}, {dec_sun}")
    print(f"RaDec Moon (deg): {ra_moon}, {dec_moon}")

    #Alt Az of Sun
    alt_sun: float = saltaz[0].degrees
    az_sun: float = saltaz[1].degrees

    #Alt Az of Moon
    alt_moon: float = maltaz[0].degrees
    az_moon: float = maltaz[1].degrees

    print(f"AltAz Sun (deg): {alt_sun}, {az_sun}")
    print(f"AltAz Moon (deg): {alt_moon}, {az_moon}")

    #The position of rainbow and moonbow
    opposite_alt_sun: float = opposite_alt(alt_sun)
    opposite_az_sun: float = opposite_az(az_sun)
    opposite_alt_moon: float = opposite_alt(alt_moon)
    opposite_az_moon: float = opposite_az(az_moon)

    print(f"Opposite of AltAz Sun (deg): {opposite_alt_sun}, {opposite_az_sun}")
    print(f"Opposite of AltAz Moon (deg): {opposite_alt_moon}, {opposite_az_moon}")

if __name__ == "__main__":
    main()
