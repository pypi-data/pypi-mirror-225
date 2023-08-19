# PHAL Fan Plugin
Enables fan speed control based on CPU temperature. The fan should remain off
for CPU temps below 60C and scale linearly to 100% at 80C (RPi thermal throttle temp).
The temperature is checked every 30 seconds while the plugin is active.