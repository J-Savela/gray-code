# Create a collection of permutation trees out of lists of codes
def allPermTrees(ls, rs, dim):
    inds = [(i, j) for i in range(len(ls)) for j in range(len(rs))]
    trees = dict(map(lambda k: (k, 0), inds))
    for i, j in inds:
        trees[i, j] = getPermTree(ls[i], rs[j], dim)
    return trees

# Create a permutation tree out of two codes
def getPermTree(left, right, dim):
    cs_r = [tuple(map(lambda x: 0, range(dim)))]
    for i in range(len(right)):
        e = list(cs_r[i])
        e[right[i]] = 1 - e[right[i]]
        cs_r.append(tuple(e))
    cs_r = cs_r[1:]

    cs_l = [tuple(map(lambda x: 0, range(dim)))]
    for i in range(len(left)):
        e = list(cs_l[i])
        e[left[i]] = 1 - e[left[i]]
        cs_l.append(tuple(e))
    for i in range(len(left) + 1):
        a = list(cs_l[i])
        for j in range(dim):
            a[j] = (a[j] + e[j]) % 2
        cs_l[i] = tuple(a)

    root = createRoot()
    for i in range(len(cs_l)):
        for j in range(len(cs_r)):
            if i == len(cs_l) - 1 and j == 0: continue
            l = cs_l[i]
            r = cs_r[j]
            initRoot(root, l, r)
            augmentTree(root, [], l, r, dim)
    return root

def augmentTree(root, permSoFar, left, right, dim):
    if root[0][0] >= 2: return
    if root[0][2]: return
    choices = set(range(dim)).difference(set(permSoFar))
    for c in choices:
        newPerm = permSoFar + [c]
        if left[c] + right[len(permSoFar)] == 1:
            newOnes = root[0][0] + 1
        else:
            newOnes = root[0][0]
        newMaxOnes = maxOnes(newPerm, left, right)
        if newOnes + newMaxOnes < 2:
            newEarlyExit = True
        else:
            newEarlyExit = False

        if c in root[1].keys() and root[1][c][0][2]:
            continue

        if c in root[1].keys():
            payload = root[1][c][0]
            payload[0] = newOnes
            payload[1] = newMaxOnes
            payload[2] = newEarlyExit
            if newEarlyExit:
                root[1][c][1].clear()
        else:
            root[1].update({c:([newOnes, newMaxOnes, newEarlyExit], {})})

        augmentTree(root[1][c], newPerm, left, right, dim)
    return

def createRoot():
    return ([0,0,0], dict())

def initRoot(root, left, right):
    root[0][0] = 0
    root[0][1] = maxOnes([], left, right)
    root[0][2] = False
    return


def maxOnes(permSoFar, left, right):
    dim = len(left)
    l_1 = 0
    r_1 = 0
    for i in range(dim):
        if i not in set(permSoFar):
            l_1 += left[i]
        if i >= len(permSoFar):
            r_1 += right[i]
    l_0 = dim - len(permSoFar) - l_1
    r_0 = dim - len(permSoFar) - r_1
    return min([l_0, r_1]) + min([l_1, r_0])