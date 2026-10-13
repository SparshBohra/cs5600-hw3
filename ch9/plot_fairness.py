#!/usr/bin/env python3
# ch9 q5
# plot fairness vs job length like the chapter graph
# no matplotlib so we print bars and write a csv

import random


def lottery_unfairness(length, tickets=100, quantum=1, trials=30):
    # run a bunch of trials and average U
    us = []
    for seed in range(trials):
        random.seed(seed)

        # two jobs same length same tickets
        left = [length, length]
        tix = [tickets, tickets]
        time = 0
        done_at = [None, None]

        while left[0] > 0 or left[1] > 0:
            # who is still running
            alive = [i for i in (0, 1) if left[i] > 0]
            total = sum(tix[i] for i in alive)

            # lottery draw
            win = random.randint(0, total - 1)

            # walk tickets until we find the winner
            chosen = None
            acc = 0
            for i in alive:
                acc += tix[i]
                if win < acc:
                    chosen = i
                    break

            # run for one quantum or whatever is left
            run = min(quantum, left[chosen])
            left[chosen] -= run
            time += run

            if left[chosen] == 0 and done_at[chosen] is None:
                done_at[chosen] = time

        # U = first finish / total time (second finishes at 2*length)
        us.append(min(done_at) / (2.0 * length))

    return sum(us) / len(us)


def main():
    # same range as the chapter figure
    lengths = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    fair = [lottery_unfairness(L) for L in lengths]

    # save numbers for the writeup
    with open("fairness.csv", "w") as f:
        f.write("length,U\n")
        for L, u in zip(lengths, fair):
            f.write(f"{L},{u:.4f}\n")

    # ascii graph so we can see the trend
    print("length     U     bar (0.5 .. 1.0)")
    for L, u in zip(lengths, fair):
        width = int((u - 0.5) * 40)
        bar = "#" * max(width, 0)
        print(f"{L:6d}  {u:.3f}  |{bar}")

    print("wrote fairness.csv")


if __name__ == "__main__":
    main()
