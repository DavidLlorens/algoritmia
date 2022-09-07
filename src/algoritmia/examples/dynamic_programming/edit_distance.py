from enum import Enum

LParams = tuple[int, int]
Score = int
Decision = str
Vertex = tuple[int, int]


class RecMode(Enum):
    Classic = 0
    Optimized = 1


def edit_distance(mode: RecMode, s: str, t: str) -> tuple[Score, list[Decision]]:
    def D_classic(m: int, n: int) -> Score:
        if m == 0 and n == 0:
            return 0
        if (m, n) not in mem:
            if n == 0:
                mem[m, n] = D_classic(m - 1, n) + 1, (m - 1, n), 'D'
            elif m == 0:
                mem[m, n] = D_classic(m, n - 1) + 1, (m, n - 1), 'I'
            else:
                c, d = (0, '-') if s[m - 1] == t[n - 1] else (1, 'S')
                mem[m, n] = min((D_classic(m - 1, n) + 1, (m - 1, n), 'D'),
                                (D_classic(m, n - 1) + 1, (m, n - 1), 'I'),
                                (D_classic(m - 1, n - 1) + c, (m - 1, n - 1), d))
        return mem[m, n][0]

    def D_optimized(m: int, n: int) -> Score:
        if m == 0 and n == 0:
            return 0
        if (m, n) not in mem:
            if n == 0:
                mem[m, n] = D_classic(m - 1, n) + 1, (m - 1, n), 'D'
            elif m == 0:
                mem[m, n] = D_classic(m, n - 1) + 1, (m, n - 1), 'I'
            else:
                if s[m - 1] == t[n - 1]:
                    mem[m, n] = D_classic(m - 1, n - 1), (m - 1, n - 1), '-'
                else:
                    mem[m, n] = min((D_classic(m - 1, n) + 1, (m - 1, n), 'D'),
                                    (D_classic(m, n - 1) + 1, (m, n - 1), 'I'),
                                    (D_classic(m - 1, n - 1) + 1, (m - 1, n - 1), 'S'))
        return mem[m, n][0]

    mem: dict[LParams, tuple[Score, LParams, Decision]] = {}
    if mode == RecMode.Classic:
        score = D_classic(len(s), len(t))
    else:
        score = D_optimized(len(s), len(t))

    sol = []
    m, n = len(s), len(t)
    while (m, n) != (0, 0):
        _, (m, n), dec = mem[m, n]
        sol.append(dec)
    sol.reverse()

    return score, sol


# ------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    mode = RecMode.Classic
    my_source, my_target = 'costa', 'casa'
    print(f'Edit distance fom "{my_source}" to "{my_target}":')
    print(f'\tMode: {mode}')
    res_score, res_decisions = edit_distance(mode, my_source, my_target)
    print(f'\tScore: {res_score}\n\tDecisions: {res_decisions}')
