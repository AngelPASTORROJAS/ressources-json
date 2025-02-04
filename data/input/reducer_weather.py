
import sys

current_city = None
max_temperature = None

for line in sys.stdin:
    line = line.strip()
    city, temperature = line.split('  ', 1)
    temperature = int(temperature)
    
    if current_city == city:
        if max_temperature is None or temperature > max_temperature:
            max_temperature = temperature
    else:
        if current_city is not None:
            print("%s  %s"%(current_city,max_temperature))
        current_city = city
        max_temperature = temperature

# N'oubliez pas d'imprimer la dernière ville
if current_city == city:
    print("%s  %s"%(current_city,max_temperature))
