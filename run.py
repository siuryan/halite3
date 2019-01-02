import json
from subprocess import check_output
import sys
import statistics

def get_scores(bots, width, height):
    output = check_output(["./halite", "-vvv", "--results-as-json", "--width", str(width), "--height", str(height), "-i", "replays"] + [ "python3 {}".format(bot) for bot in bots ])
    stats = json.loads(output)['stats']
    scores = []
    for i in range(len(bots)):
        scores.append(stats[str(i)]['score'])
    return scores

def run_test(bots, size, n):
    scores = []
    for i in range(n):
        scores.append(get_scores(bots, size, size))
    return scores

def main(bots, n, l):
    scores = {}

    for i in l:
        scores[i] = run_test(bots, int(i), n)

    for size in scores:

        bots_tally = [0] * len(bots)

        for match in scores[size]:
            bots_tally[match.index(max(match))] += 1

        bot_scores = [ [ i[j] for i in scores[size] ] for j in range(len(bots)) ]

        print ("Size {}".format(size))
        for i in range(len(bots)):
            print ("Bot{} wins \t {}/{} rounds".format(i, bots_tally[i], n))
            print ("Avg score \t {}".format(sum(bot_scores[i]) / len(scores[size])))
            print ("Median score \t {}".format(statistics.median(bot_scores[i])))
        print ()

if __name__ == "__main__":
    bots = []
    n = ""
    l = ""
    if sys.argv[1] == "2":
        bots.append(sys.argv[2])
        bots.append(sys.argv[3])
        n = sys.argv[4]
        l = sys.argv[5]
    elif sys.argv[1] == "4":
        for i in range(2, 6):
            bots.append(sys.argv[i])
        n = sys.argv[6]
        l = sys.argv[7]
    else:
        print ("Error in arguments")
        exit

    l = l.split(',')

    print (sys.argv)
    main(bots, int(n), l)
