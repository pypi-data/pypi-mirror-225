from cooptools.zones.logger import zoneLogger

class ZoneDoesntExistException(Exception):
    def __init__(self, zone_name: str):
        zoneLogger.error(f"The zone ['{zone_name}'] does not exist...")
        super().__init__()

class ZoneAlreadyExistsException(Exception):
    def __init__(self, zone_name: str):
        zoneLogger.error(f"The zone ['{zone_name}'] already exists...")
        super().__init__()
