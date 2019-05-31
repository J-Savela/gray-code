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
        if isCanonical(code): yield code
        allowed = allowedElems(K)
        #print(f"K: {K}\nStack: {stack}\nCode: {code}\nDiff: {diff}\nOdds: {odds}\nAllowed: {allowed}")
        if len(allowed) == 0 or K == length or not isCanonical(code):
            if len(stack) == 0:
                break
            K, code = backtrack()
        else:
            elem = allowed.pop()
            code.append(elem)
            updateStack(allowed)
            updateDiffAndOdds(K, elem)
            K += 1

# Enumerate all codes up to length, keep track of forbidden set
def enumerateCodes_set(length, dim):
    # stack contains tuples (<index>, <dim_number>)
    stack = []

    # cumulative sum mod 2 of each dim_number
    forb = [set(), set()]
    forb[0].add(tuple(map(lambda x: False, range(dim))))
    forb[1].add(tuple(map(lambda x: False, range(dim))))
    for d in range(dim):
        e = list(map(lambda x: False, range(dim)))
        e[d] = not e[d]
        e = tuple(e)
        forb[1].add(e)

    first = tuple(map(lambda x: False, range(dim)))
    cumsum = [first]
    code = []

    # state contains i, stack, forb, newforb, cumsum
    state = dict({"code":code, "index":0, "stack":stack, "forb": forb, "cumsum":cumsum})

    inds = list(range(dim))
    inds.reverse()
    for d in inds:
        state["stack"].append((0, d))

    def canAdd(state, elem):
        testvector = list(state["cumsum"][state["index"]])
        testvector[elem] = not testvector[elem]
        testvector = tuple(testvector)
        if len(state["code"]) >= length: return False
        if testvector in state["forb"][state["index"]]: return False
        if state["index"] <= dim and not isCanonical(state["code"] + [e]): return False
        return True

    def backtrack(state, i):
        state["index"] = i
        state["code"] = state["code"][:i]
        state["forb"] = state["forb"][:(i + 2)]
        state["cumsum"] = state["cumsum"][:(i + 1)]

    def updateState(state, elem):
        state["code"].append(elem)

        i = state["index"]
        newcumsum = list(state["cumsum"][i])
        newcumsum[elem] = not newcumsum[elem]
        state["cumsum"].append(tuple(newcumsum))

        state["forb"].append(state["forb"][i + 1].copy())
        for d in range(dim):
            e = list(state["cumsum"][i + 1])
            e[d] = not e[d]
            state["forb"][i + 2].add(tuple(e))

        inds = list(range(dim))
        inds.reverse()
        for d in inds:
            state["stack"].append((i + 1, d))

        state["index"] += 1

    while len(state["stack"]) != 0:
        j, e = state["stack"].pop()
        if state["index"] != j:
            backtrack(state, j)
        if canAdd(state, e):
            updateState(state, e)
            yield state["code"]

# Combine codes to form longer ones
def combineCodes(left, right, dim):
    for lCode in left:
        for rCode in right:
            code = lCode + rCode
            length = len(code)
            diff = list(map(lambda row: list(map(lambda col: list(map(lambda x: 0, range(dim))), range(length + 1))), range(length + 1)))
            failed = False
            for j in range(length):
                for i in range(j + 1):
                    for k in range(dim):
                        diff[i][j + 1][k] = diff[i][j][k]
                    diff[i][j + 1][code[j]] = 1 - diff[i][j][code[j]]
                    if j - i > 1 and sum(diff[i][j + 1]) < 2:
                        failed = True
                        break
                if failed: break
            if failed:
                continue
            else:
                yield code

def groupCodes(codes, dim):
    def groupOf(code):
        name = list(map(lambda x: 0, range(dim)))
        for e in code:
            name[e] = 1 - name[e]
        return tuple(name)

    names = [[0],[1]]
    for i in range(dim-1):
        newnames = []
        for n in names:
            newnames.append([0] + n)
            newnames.append([1] + n)
        names = newnames
    names = set(map(lambda x: tuple(x), names))
    groups = dict(map(lambda x: (x,[]), names))

    for c in codes:
        groups[groupOf(c)].append(c)

    return groups

def isCanonical(code):
    expecting = 0
    for i in range(len(code)):
        if code[i] == expecting: expecting += 1
        elif code[i] > expecting: return False
    return True