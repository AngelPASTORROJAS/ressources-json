from operator import itemgetter
import sys

def count_words():
    running_word = None
    running_total = 0
    count = None

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            w, cnt = line.split('\t', 1)
            count = int(cnt)
        except ValueError:
            # Ignore lines that can't be converted to integers
            continue
        
        if running_word == w:
            running_total += count
        else:
            if running_word is not None:
                print(f'{running_word}\t{running_total}')
            running_word = w
            running_total = count
    
    # Print the last word's count after loop ends
    if running_word is not None:
        print(f'{running_word}\t{running_total}')

count_words()
