# This class is for BME680 sensor
# Use this sensor for Temp, Humidity, Pressure, Gas (VOC) monitoring

# This is just simulated sensor works without hardware
import random

class BME680Sensor:

    def read(self):
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 70)
        pressure = random.uniform(980, 1020)
        gas_resistance = random.uniform(100, 500)

        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2),
            "gas_resistance": round(gas_resistance, 2)
        }