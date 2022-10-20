Interval = tuple[int, int]  # (start, end)  both are >=0

# Devuelve una lista con el máximo de actividades posibles sin solapes
def select(activities: list[Interval]) -> list[Interval]:
    # Ordenamos los índices por hora de finalización de la tarea
    sorted_indices = sorted(range(len(activities)), key=lambda i: activities[i][1])

    res: list[Interval] = []
    last_task_end = 0
    for i in sorted_indices:
        start, end = activities[i]
        if last_task_end <= start:
            res.append(activities[i])
            last_task_end = end
    return res


if __name__ == '__main__':
    activities0 = [(1, 5), (1, 2), (3, 6), (4, 7), (6, 7)]
    print(select(activities0))
