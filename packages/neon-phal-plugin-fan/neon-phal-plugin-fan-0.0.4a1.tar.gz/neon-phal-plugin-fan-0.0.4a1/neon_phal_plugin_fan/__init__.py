# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from threading import Thread, Event
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.log import LOG
from ovos_plugin_manager.hardware.fan import AbstractFan

from sj201_interface.revisions import detect_sj201_revision
from sj201_interface.fan import get_fan


class FanValidator:
    @staticmethod
    def validate(_=None):
        # TODO: Handle support for other Fan configurations here
        return detect_sj201_revision() is not None


class FanControls(PHALPlugin):
    validator = FanValidator

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="neon-phal-plugin-fan", config=config)
        self.fan = get_fan(detect_sj201_revision())
        self.fan_thread = FanControlThread(self.fan)
        self.fan_thread.start()
        if self.config.get("min_fan_temp"):
            self.fan_thread.set_min_fan_temp(
                float(self.config.get("min_fan_temp")))

    def shutdown(self):
        self.fan_thread.exit_flag.set()
        self.fan_thread.join(5)
        self.fan.shutdown()
        try:
            # Turn on Mark2 fan to prevent thermal throttling
            import RPi.GPIO as GPIO
            GPIO.output(self.fan.fan_pin, 0)
        except Exception as e:
            LOG.debug(e)


class FanControlThread(Thread):
    def __init__(self, fan_obj: AbstractFan):
        self.fan_obj = fan_obj
        self.exit_flag = Event()
        self._max_fanless_temp = 60.0  # Highest fan-less temp allowed
        self._max_fan_temp = 80.0      # Thermal throttle temp max fan
        Thread.__init__(self)

    def set_min_fan_temp(self, new_temp: float):
        """
        Set the temperature at which the fan will turn on.
        @param new_temp: Float temperature in degrees Celsius at which the fan
            will start running. Recommended values are 30.0-60.0
        """
        if new_temp > 80.0:
            LOG.error("Fan will run at maximum speed at 80C; "
                      "min temp must be lower. Setting unchanged.")
            return
        if new_temp < 0.0:
            LOG.error("Requested temperature is below operating range; "
                      "min temp must be more than 0C. Setting unchanged.")
            return
        LOG.info(f"Set fan to turn on at {new_temp}C")
        self._max_fanless_temp = new_temp

    def run(self):
        LOG.debug("temperature monitor thread started")
        while not self.exit_flag.wait(30):
            LOG.debug(f"CPU temperature is {self.fan_obj.get_cpu_temp()}")

            current_temp = self.fan_obj.get_cpu_temp()
            if current_temp < self._max_fanless_temp:
                # Below specified fanless temperature
                fan_speed = 0
                LOG.debug(f"Temp below {self._max_fanless_temp}")
            elif current_temp > self._max_fan_temp:
                LOG.warning(f"Thermal Throttling, temp={current_temp}C")
                fan_speed = 100
            else:
                # Specify linear fan curve inside normal operating temp range
                speed_const = 100/(self._max_fan_temp - self._max_fanless_temp)
                fan_speed = speed_const * (current_temp -
                                           self._max_fanless_temp)
                LOG.debug(f"temp={current_temp}")

            LOG.debug(f"Setting fan speed to: {fan_speed}")
            self.fan_obj.set_fan_speed(fan_speed)
        LOG.debug("Fan thread received exit signal")
