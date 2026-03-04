# This is just simulated sensor works without hardware
import random 

class BME280Sensor:

    def read(self):
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 70)

        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2)
        }