from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant

binary_sensor = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global binary_sensor
    
    doors_config = discovery_info[0] or []
    windows_config = discovery_info[1] or []

    for door in doors_config:
        name = door.get("name")
        door_id = door.get("id")
        pin = door.get("pin")
        binary_sensor.append(DoorSensor(hass, name, door_id, pin, "door"))

    for window in windows_config:
        name = window.get("name")
        door_id = window.get("id")
        pin = window.get("pin")
        binary_sensor.append(DoorSensor(hass, name, door_id, pin, "window"))

    async_add_entities(binary_sensor)

async def updateAllStates(array):
    """Aktualizuje stany wszystkich czujników."""
    if binary_sensor:
        for i in range(len(binary_sensor)):
            binary_sensor[i].change_state(array)


class DoorSensor(BinarySensorEntity):
    """Reprezentuje prosty czujnik drzwi."""

    def __init__(self, hass , name: str , door_id , pin , sensorClass):
        """Inicjalizuje czujnik drzwi."""
        self._name = name
        self._is_open = False
        self._pin = 1
        self._id = 1
        self._hass = hass
        self._class = sensorClass

    @property
    def name(self):
        """Zwraca nazwę czujnika."""
        return self._name

    @property
    def is_on(self):
        """Zwraca True, jeśli drzwi są otwarte."""
        return self._is_open

    @property
    def device_class(self):
        """Zwraca typ czujnika jako 'door'."""
        return self._class

    def change_state(self, array):
        """Aktualizuje stan czujnika na podstawie nowego stanu."""

        if array[0] == str(self._id):

            if(array[self._pin] == str(1)):
                self.open_door()
            else:
                self.close_door()

    def open_door(self):
        """Symuluje otwarcie drzwi."""
        self._is_open = True
        self.schedule_update_ha_state()

    def close_door(self):
        """Symuluje zamknięcie drzwi."""
        self._is_open = False
        self.schedule_update_ha_state()
