from enum import Enum

type Decision = str
type Solution = list[Decision]

type Score = int
type Result = tuple[Score, Solution]  # Siempre habrá solución, no hace falta añadir None

type SParams = tuple[int, int]  # (m, n)


class RecMode(Enum):
    Classic = 0
    Optimized = 1


def edit_distance(mode: RecMode, s: str, t: str) -> Result:
    def D_classic(m: int, n: int) -> Score:
        # Caso base
        if m == 0 and n == 0: return 0
        # Recursividad memoizada
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
        # Caso base
        if m == 0 and n == 0: return 0
        # Recursividad memoizada
        if (m, n) not in mem:
            if n == 0:
                mem[m, n] = D_optimized(m - 1, n) + 1, (m - 1, n), 'D'
            elif m == 0:
                mem[m, n] = D_optimized(m, n - 1) + 1, (m, n - 1), 'I'
            else:
                if s[m - 1] == t[n - 1]:
                    mem[m, n] = D_optimized(m - 1, n - 1), (m - 1, n - 1), '-'
                else:
                    mem[m, n] = min((D_optimized(m - 1, n) + 1, (m - 1, n), 'D'),
                                    (D_optimized(m, n - 1) + 1, (m, n - 1), 'I'),
                                    (D_optimized(m - 1, n - 1) + 1, (m - 1, n - 1), 'S'))
        return mem[m, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}
    if mode == RecMode.Classic:
        score = D_classic(len(s), len(t))
    else:
        score = D_optimized(len(s), len(t))

    # Recuperamos la solución de mem
    decisions = []
    m, n = len(s), len(t)
    while (m, n) != (0, 0):
        _, (m, n), dec = mem[m, n]
        decisions.append(dec)
    decisions.reverse()

    return score, decisions


# ------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    for mode0 in [RecMode.Classic, RecMode.Optimized]:
        my_source0, my_target0 = 'costa', 'casa'
        print(f'Edit distance fom "{my_source0}" to "{my_target0}":')
        print(f'\tMode: {mode0}')
        result0 = edit_distance(mode0, my_source0, my_target0)
        print(f'\tResult: {result0}\n')
