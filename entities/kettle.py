from loguru import logger
from const import MAX_TEMP, WATER_HEAT_CAPACITY
from enums.states import KettleState
from exceptions.kettle_exceptions import KettleStateException
import time


class Kettle:
    """Class of a Kettle"""
    __slots__ = ('__name', '__volume', '__power', '__state', '__filed_water', '__current_temp')

    def __init__(self, name: str, volume: float, power: int):
        """Initialisation of a kettle object"""
        logger.debug("Initialisation of a kettle object.")
        self.__name = name
        self.__volume = volume
        self.__power = power
        self.__filed_water = 0
        self.__current_temp = 0
        self.__state = KettleState.POWER_OFF
        logger.debug("Initialisation of a kettle object - Success.")

    @property
    def current_temp(self):
        """Return current temperature in a kettle"""
        return self.__current_temp

    def turn_on(self):
        """Turn on a kettle"""
        logger.debug("Turn on a kettle.")
        if self.__state == KettleState.POWER_OFF:
            self.__state = KettleState.POWER_ON
        logger.debug("Turn on a kettle - Success.")

    def turn_off(self):
        """Turn off a kettle"""
        logger.debug("Turn off a kettle.")
        if not self.__state == KettleState.POWER_OFF:
            self.__state = KettleState.POWER_OFF
        logger.debug("Turn off a kettle - Success.")

    def fill_water(self, water_volume):
        """Fill water into a kettle"""
        logger.debug("Fill water.")
        assert 0 < water_volume <= self.__volume
        try:
            if self.__state == KettleState.POWER_OFF:
                self.__filed_water = water_volume
                logger.debug("Fill water - Success.")
            else:
                logger.error("Wrong state of a kettle.")
                raise KettleStateException('The kettle has wrong state')
        except AssertionError:
            logger.error("Volume of water more than kettle's volume.")

    def boil_water(self, start_temp):
        """Start to boil a water"""
        logger.debug("Boil water.")
        if self.__state == KettleState.POWER_ON:
            current_time = 0
            logger.debug("Increase of a temperature.")
            while self.__current_temp <= MAX_TEMP:
                self.__current_temp = start_temp + (
                        (current_time * self.__power) / (self.__volume * WATER_HEAT_CAPACITY))
                time.sleep(1)
                current_time += 1
                yield round(self.__current_temp, 2)
                if self.__state == KettleState.POWER_OFF:
                    logger.debug('Stopping of a boiling.')
                    self.__state = KettleState.STOPPED
                    break
        logger.debug("Boil water - Success.")
