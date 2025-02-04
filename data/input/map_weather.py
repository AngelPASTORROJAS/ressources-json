
import sys

for line in sys.stdin:
    # Nettoyage de la ligne et séparation par tabulation
    line = line.strip()
    city, temperature = line.split(' ', 1)
    print("%s  %s"%(city,temperature))
