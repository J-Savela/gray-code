# Enumerates all codes up to a specified length and dimension
def enumerateCodes(length, dim):
    # stack contains pairs (<index>, <dim_number>)
    stack = []

    # cumulative sum mod 2 of each dim_number
    diff = list(map(lambda row: list(map(lambda col: list(map(lambda x: 0, range(dim))), range(length + 1))), range(length + 1)))
    odds = list(map(lambda row: list(map(lambda col: 0, range(length + 1))), range(length + 1)))

    code = []

    def allowedElems(j):
        allowed = set(range(dim))
        prohibited = set()
        for i in range(j+1):
            if odds[i][j] < 3:
                for x in range(dim):
                    if diff[i][j][x] == 1:
                        prohibited.add(x)
        return allowed.difference(prohibited)

    def backtrack():
        i, x = stack.pop()
        updateDiffAndOdds(i, x)
        newcode = code[:i]
        newcode.append(x)
        return i + 1, newcode

    def updateDiffAndOdds(j, elem):
        for i in range(j + 1):
            if diff[i][j][elem] == 1:
                odds[i][j + 1] = odds[i][j] - 1
            else:
                odds[i][j + 1] = odds[i][j] + 1
            for k in range(dim):
                diff[i][j + 1][k] = diff[i][j][k]
            diff[i][j + 1][elem] = 1 - diff[i][j][elem]

    def updateStack(elems):
        for e in elems:
            stack.append((K, e))

    K = 0
    while True:
        # check allowed elems
        # If none is allowed or code == length:
        #   output code
        #   backtrack
        # else: add element
        #       update diff and odds
        #       AND stack!!!
        allowed = allowedElems(K)
        #print(f"K: {K}\nStack: {stack}\nCode: {code}\nDiff: {diff}\nOdds: {odds}\nAllowed: {allowed}")
        if len(allowed) == 0 or K == length:
            yield code
            if len(stack) == 0:
                break
            K, code = backtrack()
        else:
            elem = allowed.pop()
            code.append(elem)
            updateStack(allowed)
            updateDiffAndOdds(K, elem)
            K += 1
