import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction,
    ClimateEntityFeature,
)
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE

from .send import send_command

climates = []

async def new_climate_temp(parsed_states):
    if climates:
        for climate in climates:
            if str(climate.get_id) == parsed_states[0] and str(climate.get_pin) == parsed_states[1]:
                result_str = f"{parsed_states[2]}.{parsed_states[3]}"
                await climate.set_new_state(result_str)

async def new_climate_out(parsed_states):
    if climates:
        for climate in climates:
            if str(climate.get_o_id) == parsed_states[0]:
                await climate.update_out(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global climates

    climate_config = discovery_info or []

    for climate in climate_config:
        name = climate.get("name")
        t_id = climate.get("t_id")
        t_pin = climate.get("t_pin")
        o_id = climate.get("t_id")
        o_pin = climate.get("t_pin")
        climates.append(Climate(name, t_id, t_pin, o_id, o_pin))

    async_add_entities(climates)

class Climate(ClimateEntity):
    def __init__(self , name, t_id, t_pin, o_id , o_pin):
        """Inicjalizacja klasy klimatyzacji."""
        self._name = name
        self._temperature = 20
        self._target_temperature = 20
        self._hvac_mode = HVACMode.OFF
        self._min_temp = 5
        self._max_temp = 35
        self._t_pin = t_pin
        self._t_id = t_id
        self._o_pin = o_pin
        self._o_id = o_id
        self._hvac_action = HVACAction.IDLE

    async def set_new_state(self , state):
        self._temperature = state

    async def update_out(self , parsed_states):
        if parsed_states[self._o_pin] == "1":
            self._hvac_action = HVACAction.HEATING
        else:
            self._hvac_action = HVACAction.IDLE

        await self.update()
        self.async_write_ha_state()

    @property
    def hvac_action(self):
        """Zwraca aktualny stan akcji grzania."""
        return self._hvac_action

    @property
    def name(self):
        """Zwraca nazwę urządzenia."""
        return self._name

    @property
    def temperature_unit(self):
        """Zwraca jednostkę temperatury."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        """Zwraca aktualną temperaturę."""
        return self._temperature

    @property
    def target_temperature(self):
        """Zwraca docelową temperaturę."""
        return self._target_temperature

    @property
    def hvac_mode(self):
        """Zwraca aktualny tryb HVAC."""
        return self._hvac_mode

    @property
    def get_id(self):
        return self._t_id

    @property
    def get_pin(self):
        return self._t_pin

    @property
    def get_o_id(self):
        return self._o_id

    @property
    def hvac_modes(self):
        """Lista dostępnych trybów pracy."""
        return [HVACMode.HEAT, HVACMode.OFF, HVACMode.AUTO]

    @property
    def supported_features(self):
        """Zwraca obsługiwane funkcje."""
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF


    @property
    def min_temp(self):
        """Zwraca minimalną dostępną temperaturę."""
        return self._min_temp

    @property
    def max_temp(self):
        """Zwraca maksymalną dostępną temperaturę."""
        return self._max_temp

    async def async_set_temperature(self, **kwargs):
        """Ustawia docelową temperaturę."""
        if ATTR_TEMPERATURE in kwargs:
            self._target_temperature = kwargs[ATTR_TEMPERATURE]
            self.async_write_ha_state()
        await self.update()

    async def async_set_hvac_mode(self, hvac_mode):
        """Ustawia tryb pracy HVAC."""
        if hvac_mode in self.hvac_modes:
            self._hvac_mode = hvac_mode
            self.async_write_ha_state()
        await self.update()

    async def update(self):
        """Aktualizacja logiki klimatyzacji."""
        if self._hvac_mode == HVACMode.HEAT:
            states = ["0"] * (6 if self._o_id < 7 else 8)
            states[self._o_pin - 1] = "1" if self._temperature < self._target_temperature else "2"
            command = f"AT+SetOut={self._o_id},{','.join(states)}"
            send_command(command)
        elif self._hvac_mode == HVACMode.OFF:
            states = ["0"] * (6 if self._o_id < 7 else 8)
            states[self._o_pin - 1] = "2"
            command = f"AT+SetOut={self._o_id},{','.join(states)}"
            send_command(command)
        self.async_write_ha_state()