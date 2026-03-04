# this sensor is for pH monitoring, either Analog or Digital

# This is just simulated sensor works without hardware
import random

class PHSensor:

    def read(self):
        ph_value = random.uniform(5.5, 7.5)

        return {
            "ph": round(ph_value, 2)
        }