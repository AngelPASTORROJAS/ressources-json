import sys

def count_words():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        for word in words:
            print(f'{word}\t1')

count_words()
