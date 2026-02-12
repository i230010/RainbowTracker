from skyfield.api import load, GREGORIAN_START, wgs84, N, E

def opposite_alt(deg):
    return deg - 90

def opposite_az(deg):
    return deg - 180

def main():
    lat: float = 3.14
    lon: float = 101.6

    print("RainbowTracker App Log(s):")

    eph = load("de421.bsp")

    ts = load.timescale()
    ts.julian_calendar_cutoff = GREGORIAN_START
    t = ts.now()

    earth, sun, moon = eph["earth"], eph["sun"], eph["moon"]
    observer = earth + wgs84.latlon(lat * N, lon * E)

    sradec = earth.at(t).observe(sun).radec()
    mradec = earth.at(t).observe(moon).radec()

    saltaz = observer.at(t).observe(sun).apparent().altaz()
    maltaz = observer.at(t).observe(moon).apparent().altaz()

    print(f"Sun RaDec Skyfield: {sradec}")
    print(f"Moon RaDec Skyfield: {mradec}")

    print(f"Sun AltAz Skyfield: {saltaz}")
    print(f"Moon AltAz Skyfield: {maltaz}")

    ra_sun: float = sradec[0].degrees
    dec_sun: float = sradec[1].degrees
    ra_moon: float = mradec[0].degrees
    dec_moon: float = mradec[1].degrees

    print(f"RaDec Sun (deg): {ra_sun}, {dec_sun}")
    print(f"RaDec Moon (deg): {ra_moon}, {dec_moon}")

    alt_sun: float = saltaz[0].degrees
    az_sun: float = saltaz[1].degrees
    alt_moon: float = saltaz[0].degrees
    az_moon: float = saltaz[1].degrees

    print(f"AltAz Sun (deg): {alt_sun}, {az_sun}")
    print(f"AltAz Moon (deg): {alt_moon}, {az_moon}")

if __name__ == "__main__":
    main()
