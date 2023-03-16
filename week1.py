class QuickFind:
    def __init__(self, n):
        self.list = [a for a in range(n)]

    def union(self, a: int, b: int):
        aid = self.list[a]
        bid = self.list[b]
        for i in range(len(self.list)):
            if self.list[i] == aid:
                self.list[i] = bid

    def connected(self, a: int, b: int):
        return self.list[a] == self.list[b]

    def show(self):
        print(self.list)


def qf_demo():
    print('Demo of Quick Find')
    QF = QuickFind(10)

    QF.union(4, 3)
    QF.union(3, 8)
    QF.union(6, 5)
    QF.union(9, 4)
    QF.union(2, 1)

    print(QF.connected(8, 9))
    print(QF.connected(5, 0))

    QF.union(5, 0)
    QF.union(7, 2)
    QF.union(6, 1)

    QF.show()


class QuickUnion:
    def __init__(self, n: int):
        self.list = [a for a in range(n)]

    def root(self, i: int):
        while i != self.list[i]:
            i = self.list[i]
        return i

    def union(self, a: int, b: int):
        aid = self.root(a)
        bid = self.root(b)
        self.list[aid] = bid

    def connected(self, a: int, b: int):
        return self.root(a) == self.root(b)

    def show(self):
        print(self.list)


def qu_demo():
    print('Demo of Quick Union')
    UF = QuickUnion(10)

    UF.union(4, 3)
    UF.union(3, 8)
    UF.union(6, 5)
    UF.union(9, 4)
    UF.union(2, 1)

    print(UF.connected(8, 9))
    print(UF.connected(5, 4))

    UF.union(5, 0)
    UF.union(7, 2)
    UF.union(6, 1)
    UF.union(7, 3)

    UF.show()


class WeightedQuickUnion:
    def __init__(self, n: int, pathcompersion: bool):
        self.list = [a for a in range(n)]
        self.weight = [1]*n
        self.pathcompresion = pathcompersion

    def root(self, i: int):
        while i != self.list[i]:
            if self.pathcompresion:
                self.list[i] = self.list[self.list[i]]
            i = self.list[i]
        return i

    def union(self, a: int, b: int):
        aid = self.root(a)
        bid = self.root(b)

        # Link the smaller tree to the larger tree
        if self.weight[aid] < self.weight[bid]:
            self.list[aid] = bid
            self.weight[bid] += self.weight[aid]
        else:
            self.list[bid] = aid
            self.weight[aid] += self.weight[bid]

    def connected(self, a: int, b: int):
        return self.root(a) == self.root(b)

    def show(self):
        print(f'List: {self.list}')
        print(f'Weights: {self.weight}')


def wqu_demo(pathcompression: bool):
    print('Demo of Quick Union')
    UF = WeightedQuickUnion(10, pathcompression)

    UF.show()

    UF.union(4, 3)
    UF.union(3, 8)
    UF.union(6, 5)
    UF.union(9, 4)
    UF.union(2, 1)

    print(UF.connected(8, 9))
    print(UF.connected(5, 4))

    UF.union(5, 0)
    UF.union(7, 2)
    UF.union(6, 1)
    UF.union(7, 3)

    UF.show()


class Percolation:
    def __init__(self, n):
        self.n = n
        self.n2 = n * n
        self.list = [a for a in range(self.n2 + 2)]  # list of roots with two virtual sites - top (0) and bottom (n*n + 1)
        self.weights = [1] * (self.n2 + 2)

        # open status of a site
        self.open = [0] * (self.n2 + 2)
        self.open[0] = 1
        self.open[self.n2 + 1] = 1

        # connecting top and bottom row to virtual sites
#        for i in range(1, self.n + 2):
#            self.list[i] = 0
#            self.list[-i] = self.n2 + 1

    def _root(self, i: int):
        while i != self.list[i]:
            self.list[i] = self.list[self.list[i]]
            i = self.list[i]
        return i

    def is_open(self, row, col):
        return self.open[(row - 1) * self.n + col] == 1

    def _union(self, a_row: int, a_col:int, b_row: int, b_col: int):
        if self.is_open(b_row, b_col) and self.is_open(a_row, a_col):
            a = ((a_row - 1) * self.n + a_col)
            b = ((b_row - 1) * self.n + b_col)
            aid = self._root(a)
            bid = self._root(b)

            # Link the smaller tree to the larger tree
            if self.weights[aid] < self.weights[bid]:
                self.list[aid] = bid
                self.weights[bid] += self.weights[aid]
            else:
                self.list[bid] = aid
                self.weights[aid] += self.weights[bid]

    def _connected(self, a: int, b: int):
        return self._root(a) == self._root(b)

    def open_site(self, row, col):
        '''
        Opens a site at the location row x col. It creates a connection with the neighbouring sites.
        '''
        self.open[((row - 1) * self.n + col)] = 1
        if row != 1:  # set connection to site on top
            self._union(row - 1, col, row - 2, col)
        if col != 1:  # set connection to site on left
            self._union(row - 1, col, row - 1, col - 1)
        if row != self.n:  # set connection to site bellow
            self._union(row - 1, col, row, col)
        if col != self.n:  # set connection to site on right
            self._union(row - 1, col, row - 1, col + 1)

    def is_full(self, row, col):
        '''
        The site is full if it is connected to the top row (virtual top site), i.e. its root is 0.
        '''
        return self._root((row - 1) * self.n + col) == 0

    def percolates(self):
        '''
        If there is a full site in the bottom row (virtual bottom site), the system percolates.
        '''
        return self.is_full(self.n + 1, 1)
        
    def show(self):
        print('Roots:')
        for i in range(1,self.n + 1):
            print(f'{self.list[self.n*(i - 1) + 1 : self.n*i + 1]}')
        print('Open sites: ')
        for i in range(1,self.n + 1):
            print(f'{self.open[self.n*(i - 1) + 1 : self.n*i + 1]}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Demo of Quick Find
    #qf_demo()
    #print('')

    #Demo of Quick Union
    #qu_demo()
    #print('')

    #Demo of Weighted Quick Union
    #wqu_demo(False)
    #print('')

    #demo of Weithed Quick Union with path Compression
    #wqu_demo(True)

    # Percolation example for 5x5
    p = Percolation(5)
    print(p.list[26])
    for i,j in [[1,2],[1,3],[1,5],[2,3],[2,4],[2,5],[3,1],[3,2],[3,4],[3,5],[4,1],[4,5],[5,2],[5,3],[5,4],[5,5]]:
        p.open_site(i,j)
    p.show()
    print(p.list[26])
    print(p.percolates())