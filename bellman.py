def bellman(arcs, s, n):
    k = 0

    while True:
        k += 1
        c = False

        for i, j, q in arcs:
            if s[j] < s[i] + q:
                s[j] = s[i] + q
                c = True

        if not c or k == n:
            break

    if c:
        raise ValueError("Dépendances circulaires")

    return s