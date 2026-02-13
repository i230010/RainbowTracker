"""
main.py file for the RainbowTracker
-----------------------------------
This file includes the calculations for the position of the rainbow, 3d rendering and the program to run the app (ursina)
I'll try to best document this code
"""

# Required modules
import math
from skyfield.api import load, GREGORIAN_START, wgs84, N, E
import ursina as u
import datetime


def fmap(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """
    Map's value from a range to another range

    Parameters
    ----------

    X, Min of X, Max of X, Out min, Out Max

    Returns
    -------
    The range thats mapped
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


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


def sunmoon_positions(lat: float, lon: float, dt):
    """
    Computes the Local AltAz for Sun and Moon's AltAz, Angular Diameter and 'Bows

    Parameters
    ----------
    Lat, Lon, datetime object in UTC

    Returns
    -------
    alt of sun, az of sun, alt of moon, az of moon, alt rainbow, az rainbow, alt moonbow, az moonbow, sun angular diameter, moons angular diameter
    """

    # Load Epehemerides
    eph = load("de421.bsp")

    # Load Timescale
    ts = load.timescale()
    ts.julian_calendar_cutoff = GREGORIAN_START
    t = ts.from_datetime(dt)

    # Object positions in Geocentric and Localized
    earth, sun, moon = eph["earth"], eph["sun"], eph["moon"]  # Geocentric
    observer = earth + wgs84.latlon(lat * N, lon * E)  # Localized

    # Apparent diameter
    sang = math.degrees(
        math.asin(695700 / observer.at(t).observe(sun).apparent().distance().km)
    )
    mang = math.degrees(
        math.asin(1737.4 / observer.at(t).observe(moon).apparent().distance().km)
    )

    # Moon's RaDec
    saltaz = observer.at(t).observe(sun).apparent().altaz()
    maltaz = observer.at(t).observe(moon).apparent().altaz()

    # Alt Az of Sun
    alt_sun: float = saltaz[0].degrees
    az_sun: float = saltaz[1].degrees

    # Alt Az of Moon
    alt_moon: float = maltaz[0].degrees
    az_moon: float = maltaz[1].degrees

    # The position of rainbow and moonbow
    opposite_alt_sun: float = opposite_alt(alt_sun)
    opposite_az_sun: float = opposite_az(az_sun)
    opposite_alt_moon: float = opposite_alt(alt_moon)
    opposite_az_moon: float = opposite_az(az_moon)

    return (
        alt_sun,
        az_sun,
        alt_moon,
        az_moon,
        opposite_alt_sun,
        opposite_az_sun,
        opposite_alt_moon,
        opposite_az_moon,
        sang,
        mang,
    )


stop = 1


def main():
    """
    Main function
    """
    
    global now
    now = datetime.datetime.now(datetime.UTC)

    global sun
    global moon
    global gndrad  # Ground Radius
    global datetime_text
    global rainbow1
    global rainbow2
    global moonbow1
    global moonbow2
    global lat_input
    global lon_input

    print("RainbowTracker App Log(s):")

    # Ursina app
    app = u.Ursina("RainbowTracker", "icon.ico")

    # Ground scale
    k = 50

    # The ground
    ground1 = u.Entity(  # noqa: F841
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(0, 255, 0),
        rotation_x=90,
        y=0,
    )
    ground2 = u.Entity(  # noqa: F841
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(0, 255, 0),
        rotation_x=-90,
        y=0,
    )
    gndrad = k / 2

    # sun
    sun = u.Entity(model="sphere", color=u.rgb(255, 255, 0), scale=k - (k - 1))

    # moon
    moon = u.Entity(model="sphere", color=u.rgb(100, 100, 100), scale=k - (k - 1))

    # rainbow
    rainbow1 = u.Entity(
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(0, 255, 128),
        rotation_x=0,
        y=0,
    )  # noqa: F841
    rainbow2 = u.Entity(
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(0, 255, 128),
        rotation_x=180,
        y=0,
    )  # noqa: F841

    # moonbow
    moonbow1 = u.Entity(
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(128, 128, 128),
        rotation_x=0,
        y=0,
    )  # noqa: F841
    moonbow2 = u.Entity(
        model=u.Circle(100, thickness=10),
        scale=k,
        color=u.rgb(128, 128, 128),
        rotation_x=180,
        y=0,
    )  # noqa: F841

    # ui
    u.Text.default_resolution = 1080 * u.Text.size
    datetime_text = u.Text(
        text="Datetime",
        wordwrap=30,
        color=u.rgb(0, 0, 0),
        origin=(-0.5, -0.5),
        position=(-0.88, -0.49),
    )

    u.Button(
        text="+ Sec", position=(-0.8, 0.45), scale=(0.15, 0.08), on_click=add_second
    )
    u.Button(
        text="- Sec", position=(-0.8, 0.35), scale=(0.15, 0.08), on_click=sub_second
    )
    u.Button(
        text="+ Min", position=(-0.8, 0.25), scale=(0.15, 0.08), on_click=add_minute
    )
    u.Button(
        text="- Min", position=(-0.8, 0.15), scale=(0.15, 0.08), on_click=sub_minute
    )
    u.Button(
        text="+ Hour", position=(-0.8, 0.05), scale=(0.15, 0.08), on_click=add_hour
    )
    u.Button(
        text="- Hour", position=(-0.8, -0.05), scale=(0.15, 0.08), on_click=sub_hour
    )
    u.Button(
        text="Now", position=(-0.8, -0.15), scale=(0.15, 0.08), on_click=now_datetime
    )
    u.Button(
        text="Stop", position=(-0.8, -0.25), scale=(0.15, 0.08), on_click=stop_datetime
    )
    lat_input = u.InputField(
        default_value="0.000", label="", position=(-0.8, -0.35), scale=(0.15, 0.05)
    )
    lon_input = u.InputField(
        default_value="0.000", label="", position=(-0.8, -0.42), scale=(0.15, 0.05)
    )

    ec = u.EditorCamera(  # noqa: F841
        rotation_speed=200, panning_speed=0
    )  # disable normal panning

    app.run()  # ty:ignore[missing-argument]


def add_second():
    global now
    now += datetime.timedelta(seconds=1)


def add_minute():
    global now
    now += datetime.timedelta(seconds=60)


def add_hour():
    global now
    now += datetime.timedelta(hours=1)


def sub_second():
    global now
    now -= datetime.timedelta(seconds=1)


def sub_minute():
    global now
    now -= datetime.timedelta(seconds=60)


def sub_hour():
    global now
    now -= datetime.timedelta(hours=1)


def now_datetime():
    global now
    now = datetime.datetime.now(datetime.UTC)


def stop_datetime():
    global stop
    stop = not (stop)


lat_value = 0
lon_value = 0


def update():
    global now
    global lat_value
    global lon_value

    if u.held_keys["enter"]:
        lat_value = float(lat_input.text)
        lon_value = float(lon_input.text)

    salt, saz, malt, maz, osalt, osaz, omalt, omaz, sang, sang = sunmoon_positions(
        lat_value, lon_value, now
    )
    sun.scale = (gndrad * 0.25) * sang
    moon.scale = (gndrad * 0.25) * sang
    now += datetime.timedelta(seconds=1) * u.time.dt * stop  # smooth tick

    datetime_text.text = (
        f"{now.strftime('%Y-%m-%dT%H:%M:%SZ')} Lat: {lat_value}, Lon: {lon_value}"
    )

    # Sun AltAz
    r = gndrad

    alt_rad = math.radians(salt)
    az_rad = math.radians(saz)

    sun.x = r * math.cos(alt_rad) * math.sin(az_rad)
    sun.y = r * math.sin(alt_rad)
    sun.z = r * math.cos(alt_rad) * math.cos(az_rad)

    # Moon AltAz
    alt_rad = math.radians(malt)
    az_rad = math.radians(maz)

    moon.x = r * math.cos(alt_rad) * math.sin(az_rad)
    moon.y = r * math.sin(alt_rad)
    moon.z = r * math.cos(alt_rad) * math.cos(az_rad)

    # Rainbow AltAz
    r = gndrad

    alt_rad = math.radians(osalt)
    az_rad = math.radians(osaz)

    rainbow1.x = r * math.cos(alt_rad) * math.sin(az_rad)
    rainbow1.y = r * math.sin(alt_rad)
    rainbow1.z = r * math.cos(alt_rad) * math.cos(az_rad)

    rainbow1.rotation_y = osaz
    rainbow1.rotation_x = -osalt
    rainbow1.rotation_z = 0

    rainbow2.x = r * math.cos(alt_rad) * math.sin(az_rad)
    rainbow2.y = r * math.sin(alt_rad)
    rainbow2.z = r * math.cos(alt_rad) * math.cos(az_rad)

    rainbow2.rotation_y = osaz
    rainbow2.rotation_x = -osalt + 180
    rainbow2.rotation_z = 0

    # Moonbow AltAz
    r = gndrad

    alt_rad = math.radians(omalt)
    az_rad = math.radians(omaz)

    moonbow1.x = r * math.cos(alt_rad) * math.sin(az_rad)
    moonbow1.y = r * math.sin(alt_rad)
    moonbow1.z = r * math.cos(alt_rad) * math.cos(az_rad)

    moonbow1.rotation_y = omaz
    moonbow1.rotation_x = -omalt
    moonbow1.rotation_z = 0

    moonbow2.x = r * math.cos(alt_rad) * math.sin(az_rad)
    moonbow2.y = r * math.sin(alt_rad)
    moonbow2.z = r * math.cos(alt_rad) * math.cos(az_rad)

    moonbow2.rotation_y = omaz
    moonbow2.rotation_x = -omalt + 180
    moonbow2.rotation_z = 0


if __name__ == "__main__":
    main()
