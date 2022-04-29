def get_L1(dataset, min_sup):
    tids = {}
    for i, trans in enumerate(dataset):
        for x in set(trans):
            tids[x] = tids.get(x, set([])) | {i}

    for x in list(tids.keys()):
        if len(tids[x]) < min_sup:
            tids.pop(x)
    L1 = []
    for x in tids:
        L1.append(([x], tids[x]))
    return L1


def get_L(L, min_sup):
    Lk = []
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            ki, vi = L[i]
            kj, vj = L[j]
            if (ki[:-1] == kj[:-1]):
                key = ki + kj[-1:]
                val = vi & vj
                if len(val) >= min_sup:
                    Lk.append((key, val))
    return Lk


# eclat算法
def Eclat(dataset, min_sup):
    L1 = get_L1(dataset=dataset, min_sup=min_sup)
    Lk = L1
    L = L1
    k = 2
    while len(Lk):
        Lk = get_L(L=Lk, min_sup=min_sup)
        L.extend(Lk)
        k += 1
    return L


if __name__ == '__main__':
    dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'], ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'], ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
               ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'], ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
    L = Eclat(dataset, min_sup=3)
    print(L)
