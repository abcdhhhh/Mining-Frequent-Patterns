class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, dep=1):
        print(dep, ' ' * dep, self.name, self.count)
        for child in self.children.values():
            child.disp(dep + 1)

    # def __lt__(self, other):# 定义 "<"用于sorted()
    # return self.count < other.count


def createTree(dataSet: dict, min_sup=1):  # create FP-tree from dataset but don't mine
    headerTable = {}
    # go over dataSet twice
    for trans in dataSet:  # first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    for k in list(headerTable.keys()):  # remove items not meeting min_sup
        if headerTable[k] < min_sup:
            headerTable.pop(k)
    # print('headerTable:', headerTable)
    bigL = [k for k, v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)]
    # print('bigL:', bigL)

    # print('freqItemSet: ',freqItemSet)
    if len(bigL) == 0:
        return None, None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    # print 'headerTable: ',headerTable
    retTree = treeNode('root', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        orderedItems = []
        for item in bigL:
            if item in tranSet:
                orderedItems.append(item)
        if len(orderedItems) > 0:
            # print(tranSet, count, orderedItems, sep='\t')
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
    return retTree, headerTable, bigL  # return tree and header table


def updateTree(items, inTree, headerTable, count):
    for item in items:
        if item in inTree.children:  # check if orderedItems[i] in children
            inTree.children[item].inc(count)  # incrament count
        else:  # add item to inTree.children
            inTree.children[item] = treeNode(item, count, inTree)
            if headerTable[item][1] is None:  # update header table
                headerTable[item][1] = inTree.children[item]
            else:
                updateHeader(headerTable[item][1], inTree.children[item])
        inTree = inTree.children[item]


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink is not None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    while (leafNode.parent is not None):
        prefixPath.append(leafNode.name)
        leafNode = leafNode.parent


def findPrefixPath(basePat, node):  # node comes from header table
    assert (node.name == basePat)
    condPats = {}
    while node is not None:
        prefixPath = []
        ascendTree(node, prefixPath)
        assert (prefixPath[0] == basePat)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = node.count
        node = node.nodeLink
    return condPats


def mineTree(inTree, headerTable, bigL, min_sup, preFix, freqItemList):
    for basePat in bigL[::-1]:  # start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        # print('finalFrequent Item: ', newFreqSet)  # append to set
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print('condPattBases :',basePat, condPattBases)
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead, myBigL = createTree(condPattBases, min_sup)
        # print 'head from conditional tree: ', myHead
        if myHead is not None:  # 3. mine cond. FP-tree
            # print 'conditional tree for: ',newFreqSet
            # myCondTree.disp(1)
            mineTree(myCondTree, myHead, myBigL, min_sup, newFreqSet, freqItemList)  # 递归


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
    return retDict


def FPGrowth(dataSet, min_sup):
    initSet = createInitSet(dataSet)
    # print('initSet:', initSet)
    myFPtree, myHeaderTab, bigL = createTree(initSet, min_sup)
    myFreqList = []
    if myFPtree is not None:
        # myFPtree.disp()
        mineTree(myFPtree, myHeaderTab, bigL, min_sup, set(), myFreqList)
    return myFreqList
