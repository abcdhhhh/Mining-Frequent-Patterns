from Apriori import Apriori
from FPGrowth import FPGrowth
from Eclat import Eclat
import time
import random


def load_data():
    # dataset = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
    # dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'], ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'], ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
    #            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'], ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
    # dataset = [['r', 'z', 'h', 'j', 'p'], ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'], ['z', 'p', 'x'], ['r', 'x', 'n', 'o', 's'], ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # dataset = [[0], [0, 1], [0, 1]]
    dataset = []
    for i in range(100):
        tmp = []
        for j in range(100):
            if random.random() < 0.1:
                tmp.append(j)
        dataset.append(tmp)
    return dataset


if __name__ == '__main__':
    dataset = load_data()

    methods = [Apriori, FPGrowth, Eclat]

    for method in methods:
        print(method.__name__)
        start = time.time()
        L = method(dataset=dataset, min_sup=5)
        # print(L)
        # print(len(L))
        print("time cost:", time.time() - start)
