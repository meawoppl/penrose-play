def roll(seq, n):
    if len(seq) == 0:
        return seq

    n = n % len(seq)
    return seq[n:] + seq[:n]


def rolled_loop_iterator(iterable, roll_dist=1):
    rolled = roll(iterable, roll_dist)
    return zip(iterable, rolled)
