from itertools import combinations


def get_L1(dataset, min_sup):
    cnt = {}
    for trans in dataset:
        for x in set(trans):
            cnt[x] = cnt.get(x, 0) + 1
    L1 = []
    for x in list(cnt.keys()):
        if cnt[x] >= min_sup:
            L1.append([x])
    return L1


def get_sup(p, dataset):
    sup = 0
    for trans in dataset:
        if set(p).issubset(set(trans)):
            sup += 1
    return sup


def get_L(dataset, C, min_sup: int):
    L = []
    for p in C:
        if get_sup(p, dataset) >= min_sup:
            L.append(p)
    return L


def has_infrequent_subset(c, L):
    length = len(c)
    for s in combinations(c, length - 1):
        flag = False
        for p in L:
            if set(s) == set(p):
                flag = True
        if not flag:
            return True
    return False


def get_C(L):
    C = []
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if L[i][:-1] == L[j][:-1]:
                c = L[i] + L[j][-1:]
                if not has_infrequent_subset(c, L):
                    C.append(c)
    return C


def Apriori(dataset, min_sup: int):
    L1 = get_L1(dataset=dataset, min_sup=min_sup)
    Lk = L1
    L = L1
    k = 2
    while len(Lk):
        Ck = get_C(L=Lk)
        # print(Ck)
        Lk = get_L(dataset=dataset, C=Ck, min_sup=min_sup)
        L.extend(Lk)
        k += 1
    return L


if __name__ == '__main__':
    dataset = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]

    print("Apriori:")
    L = Apriori(dataset=dataset, min_sup=2)
    print(L)
