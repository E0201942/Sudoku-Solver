import sys
import copy
import heapq

  
allNeighbors = [[None for x in range(9)]for y in range(9)]
def identifyNeighbors(i, j):
        neighbors = []
        square = int(j/3) + int(i/3) *3
        for x in range(9):
            if x != i:
                neighbors.append((x, j))
        for x in range(9):
            if x !=j:
                neighbors.append((i,x))
        c = int(square/3) * 3
        d = (square % 3) * 3 
        for a in range(c, c+3):
            for b in range(d, d+3):
                if a!=i and b!=j:
                    neighbors.append((a,b))
        
        return neighbors

for i in range(9):
            for j in range(9):
                allNeighbors[i][j] = identifyNeighbors(i,j)
def chooseValue(i, j, nums, assigned):
    global allNeighbors
    neighbors = allNeighbors[i][j]
    toCheck = [21 ,21, 21, 21, 21, 21, 21, 21, 21, 21]
    for x in range(1 , 10):
        if nums[i][j][x] == 0:
            c = 0
            for a ,b in neighbors:
                if nums[a][b][x]!=0 and assigned[a][b] == 0:
                    c +=1
            toCheck[x] = -1* c
    return toCheck

def updateNeighbors(i, j, value, nums, assigned, unassigned):
    global numBacktracks
    global allNeighbors
    numBacktracks +=1
    neighbors = allNeighbors[i][j]
    q=[]
    assigned[i][j] = value   
    unassigned -=1
    ans = None
    toBreak = False
    needCheck = True
    mrv = (9, -1, -1,-1)
    if unassigned == 0:
        return 1
    for a, b in neighbors:
        if assigned[a][b] == 0:
            nums[a][b][10] -=1
            nums[a][b][value] += 1
            if nums[a][b][value] == 1:
                nums[a][b][0] -=1
            if nums[a][b][0] == 0 and assigned[a][b] == 0:
                toBreak = True
            if nums[a][b][0] == 1 and assigned[a][b] == 0 and nums[a][b][10]>mrv[1]:
                mrv = (nums[a][b][0] , nums[a][b][10], a, b)
                needCheck = False

    if toBreak == True:
        assigned[i][j] = 0
        for a, b in neighbors:
            if assigned[a][b] == 0:
                nums[a][b][10] +=1
                nums[a][b][value] -= 1
                if nums[a][b][value] == 0:
                    nums[a][b][0] +=1
        return None
    if needCheck == True:
        for a in range(9):
                for b in range(9):
                    if assigned[a][b] == 0 and nums[a][b][0] < mrv[0]:
                        mrv = (nums[a][b][0], nums[a][b][10], a, b)
                    elif assigned[a][b] == 0 and nums[a][b][0] == mrv[0] and nums[a][b][10] > mrv[1]:
                        mrv = (nums[a][b][0], nums[a][b][10], a, b)

    if nums[mrv[2]][mrv[3]][0]< 3:   
        for x in range(1, 10):
            if nums[mrv[2]][mrv[3]][x]==0:
                ans = updateNeighbors(mrv[2],mrv[3],x , nums, assigned, unassigned)
                if ans !=None:
                    return 1

    else:
            q = []
            order = chooseValue(mrv[2], mrv[3], nums, assigned)
            for x in range (1 ,10):
                if order[x] != 21:
                    heapq.heappush(q, (order[x], x))
            while len(q) != 0:
                ind = heapq.heappop(q)
                if order[ind] == 21:
                        break
                ans = updateNeighbors(mrv[2],mrv[3],ind[1] , nums, assigned, unassigned)
                #order[ind] = 21
                #ind = order.index(min(order))
                if ans !=None:
                    return 1
                    
    assigned[i][j] = 0
    for a, b in neighbors:
        if assigned[a][b] == 0:
            nums[a][b][10] +=1
            nums[a][b][value] -= 1
            if nums[a][b][value] == 0:
                nums[a][b][0] +=1
    return None
                    
                

                
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        global allNeighbors
        #TODO: Your code here
        nums = [[[9, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 20]for x in range(9)]for y in range(9)]
        assigned =[[0 for x in range(9)] for y in range(9)]
        q =[]
        toBreak = False
        unassigned = 81
        for i in range(9):
            for j in range (9):
                if self.puzzle[i][j] !=0:
                    value = self.puzzle[i][j]
                    assigned[i][j] = value
                    unassigned -=1
                    neighbors = allNeighbors[i][j]
                    for a, b in neighbors:
                        allNeighbors[a][b].remove((i, j))
                        if assigned[a][b] == 0:
                            nums[a][b][10] -=1
                            nums[a][b][value] += 1
                            if nums[a][b][value] == 1:
                                nums[a][b][0] -=1
        
        for i in range(9):
                for j in range(9):
                    if assigned[i][j] == 0:
                        heapq.heappush(q, (nums[i][j][0],  -1*nums[i][j][10], i, j))
                    
        mrv = heapq.heappop(q)
        
        while(len(q)!=0):
                if assigned[mrv[2]][mrv[3]] !=0:
                            mrv = heapq.heappop(q)
                            continue
                if nums[mrv[2]][mrv[3]][0]>1:
                    order = chooseValue(mrv[2], mrv[3], nums, assigned)
                    ind = order.index(min(order))
                    while order[ind] != 21:
                                if order[ind] == 21:
                                    break
                                ans = updateNeighbors(mrv[2],mrv[3],ind , nums, assigned, unassigned)
                                order[ind] = 21
                                ind = order.index(min(order))
                                if ans != None:
                                    self.ans = assigned
                                    toBreak = True
                                    break
                else:
                    for x in range(1, 10):
                        if nums[mrv[2]][mrv[3]][x]==0:
                                ans = updateNeighbors(mrv[2],mrv[3], x, nums, assigned, unassigned)
                                if ans !=None:
                                    self.ans = assigned
                                    toBreak = True
                                    break
                if toBreak == True:
                    break
                mrv = heapq.heappop(q)    
        if toBreak == False and nums[mrv[2]][mrv[3]][0]>1:
                order = chooseValue(mrv[2], mrv[3], nums, assigned)
                ind = order.index(min(order))
                while order[ind] != 21:
                    if order[ind] == 21:
                            break
                    ans = updateNeighbors(mrv[2],mrv[3],ind , nums, assigned, unassigned)
                    order[ind] = 21
                    ind = order.index(min(order))
                    if ans !=None:
                        self.ans = assigned
                        break
        elif toBreak == False:
                 for x in range(1, 10):
                    if nums[mrv[2]][mrv[3]][x]==0:
                        ans = updateNeighbors(mrv[2],mrv[3],x , nums, assigned, unassigned)
                        if ans !=None:
                            self.ans = assigned
                            break
            # don't print anything here. just resturn the answer
            # self.ans is a list of lists
        return self.ans
    

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
