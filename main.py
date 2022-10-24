#project.py
#Tania Regina Ramírez Vázquez, Miguel Chávez Silva and Denisse Anayeli Avendaño Sánchez
#Gives, analizes and prints valid chess board with the white King (K), white Rook (R) and black king (k), it will print the possible black king's moves and if it is in check or Checkmate. 

import random 

#Parameters: b, the board
#Returns: nothing
#Prints the 8x8 chess board
def printBoard(b):
  rows = len(b)
  cols = len(b[0])
  for r in range(rows):
    for c in range(cols):
      print(b[r][c], end = " ")
    print()

#Parameters: nothing
#Returns: the empty chess board
#Creates and returns an 8x8 list with the board
def makeBoard():
  b = []
  for r in range(8):
    row = []
    if r % 2 == 0:
      for c in range(8):
        if c % 2 == 0:
          row.append("@")
        else: 
          row.append("#")
    else: 
      for c in range(8):
        if c % 2 == 0:
          row.append("#")
        else: 
          row.append("@")
    b.append(row)
  return b

#Parameters: b, the board
#Returns: updated board, including K
#Places the white king K, randomly
def placeK(b):
  row = random.randint(0,7)
  col = random.randint(0,7)
  b[row][col] = "K" 
  return b

#Parameters: b, the board
#Returns: updated board, including R
#Places the white rook R, randomly
def placeR(b):
  row = random.randint(0,7)
  col = random.randint(0,7)
  while b[row][col] == "K":
    row = random.randint(0,7)
    col = random.randint(0,7)
  b[row][col] = "R" 
  return b

#Parameters: b, the board. p, the piece to search for
#Returns: a 2-element list, containing [row,col] where the piece was found, or None if it was not found 
#Searches for p inside b. Returns [row,col] or None
def findPiece(b,p):
  for r in range(len(b)):
    for c in range(len(b[0])):
      if b[r][c] == p:
        return [r,c]
  return None

#Parameters: b, the board
#Returns: updated board, including k, the black king
#Places k, the black king, in a valid position
def placek(b):
  posK = findPiece(b,"K")
  row = random.randint(0,7)
  col = random.randint(0,7)
  diffR = abs(row - posK[0])
  diffC = abs(col - posK[1])
  while b[row][col] == "K" or b[row][col] == "R" or (diffR < 2 and diffC < 2):
    row = random.randint(0,7)
    col = random.randint(0,7)
    #Update distance between the kings because you now have new positions
    diffR = abs(row - posK[0])
    diffC = abs(col - posK[1])
  b[row][col] = "k" 
  return b

#Parameters: pos, possible postions of k, R and K
#Returns: boolean values
#Take out the possitions that are outisde the board.
def inBounds(pos):
  r = pos[0]
  c = pos[1]
  if r < 0 or c < 0 or r > 7 or c > 7:
    return False
  else:
    return True

#Parameters: b, the board
#Returns: a list of 3 elements: validk, inCheck, inCheckmate
#Stablish the possible options for k and analize if k is in check and checkmate according to the chess rules. 
def getMovesFork(b):
  inCheck = False
  inCheckmate = False
  k = findPiece(b,"k")
  K = findPiece(b,"K")
  R = findPiece(b,"R")
  
  #Check around K:
  rK = K[0]
  cK = K[1]
  possibleK = [[rK, cK + 1],
            [rK - 1,cK + 1],
            [rK - 1,cK],
            [rK - 1,cK - 1],
            [rK,cK - 1],
            [rK + 1,cK - 1],
            [rK + 1,cK],
            [rK + 1,cK + 1]]
  validK = []
  for p in possibleK:
      if inBounds(p):
        validK.append(p) #valid positions for K
      
  #Check around k:
  rk = k[0]
  ck = k[1]
  possiblek = [[rk,ck + 1],
            [rk - 1,ck + 1],
            [rk - 1,ck],
            [rk - 1,ck - 1],
            [rk,  ck - 1],
            [rk + 1,ck - 1],
            [rk + 1,ck],
            [rk + 1,ck + 1]]
  validk = []
  
  #Check around R:
  rR = R[0]
  cR = R[1]
  possibleR = [[rR - 1,cR],
    [rR - 2,cR],
    [rR - 3,cR],
    [rR - 4,cR],
    [rR - 5,cR],
    [rR - 6,cR],
    [rR - 7,cR],
    [rR + 1,cR],
    [rR + 2,cR],
    [rR + 3,cR],
    [rR + 4,cR],
    [rR + 5,cR],
    [rR + 6,cR],
    [rR + 7,cR],
    [rR,cR + 1],
    [rR,cR + 2],
    [rR,cR + 3],
    [rR,cR + 4],
    [rR,cR + 5],
    [rR,cR + 6],
    [rR,cR + 7],
    [rR,cR - 1],
    [rR,cR - 2],
    [rR,cR - 3],
    [rR,cR - 4],
    [rR,cR - 5],
    [rR,cR - 6],
    [rR,cR - 7]]
  validR = []

  #remove positions for Root according to k 
  for p in possibleR:
    if inBounds(p) and p not in validk:
      validR.append(p)

  #remove positions according to the R and the K 
  #inCheck uses the function "if" to become True
  for p in possiblek:
      if inBounds(p) and p not in validK and p not in validR:
        validk.append(p)
      if k in validR:
        inCheck = not False
  
  #When the White King (K) is in the middle and in the same column of the White Root (R) and the Black King(k) Check is False and add that possible movement 
  if ((k[1] == K[1] == R[1]) and (k[0] < K[0] < R[0])):
    inCheck = False 
    if k[0] + 2 != K[0]:
      validk.append([rk + 1,ck]) 
    if (k[0] - 1 == 0) and k[0] + 2 != K[0]:
      validk.append([rk-1,ck])
    elif (k[0] - 1 >= 0) and (K[0] - k[0]) >= 2:  
      validk.append([rk - 1,ck])
  
  if (k[1] == K[1] == R[1]) and (k[0] > K[0] > R[0]):
    inCheck = False
    if k[0] - 2 != K[0]:
      validk.append([rk - 1,ck])
    if (k[0] + 1 == 0) and k[0] - 2 != K[0]:
      validk.append([rk + 1,ck])
    elif (k[0] + 1 <= 7) and (k[0] - K[0]) >= 2:  
      validk.append([rk + 1,ck])
  
  #When the White King (K) is in the middle and in the same row of the White Root (R) and the Black King(k) Check is False
  if (k[0] == K[0] == R[0]) and (k[1] < K[1] < R[1]):
    inCheck = False
    if k[1] + 2 != K[1]:
      validk.append([rk,ck + 1]) 
    if (k[1] - 1 == 0) and k[1] + 2 != K[1]:
      validk.append([rk,ck - 1])
    elif (k[1] - 1 >= 0) and (K[1] - k[1]) >= 2:  
      validk.append([rk,ck - 1])

  if (k[0] == K[0] == R[0]) and (k[1] > K[1] > R[1]):
    inCheck = False
    if k[1] - 2 != K[1]:
      validk.append([rk,ck - 1]) 
    if (k[1] + 1 == 0) and k[1] - 2 != K[1]:
      validk.append([rk,ck + 1])
    elif (k[1] + 1 <= 7) and (k[1] - K[1]) >= 2:  
      validk.append([rk,ck + 1])

  #inCheckmate uses the function "if" to become True
  if len(validk) == 0 and inCheck == True:
    inCheckmate = not False

  #Returns the result in a list:
  return [validk, inCheck, inCheckmate]

#--------CODE----------------
choice = int(input())
board = []
if choice == 1:
  board = makeBoard()
  board = placeK(board)
  board = placeR(board)
  board = placek(board)
elif choice == 2:
  for r in range(8):
    line = input()           
    row = line.split(" ", 7)    
    row[7] = row[7].strip()     
    board.append(row)        

printBoard(board)

info = getMovesFork(board)
movesk = info[0]
check = info[1]
checkmate = info[2]
print("Black King Moves:", movesk)
print("Check:", check)
print("Checkmate:", checkmate)

'''
Test cases:
1. Do not use letters in the first line when running the program.
2. Do not use special characters in the first line when running the program.
3. Only use 1 or 2 in the first line when running the program. 
4. When selecting the second option, you can use any character but you have to always put the Black King (k), the White King (K) and the White Root (R).
5. When selecting the second option, you must type the Black King (k), the White King (K) and the White Root (R),inside the valid matrix that is 8 x 8. 

Edge case:
Tie, where the black king does not have any movements but the Check and Checkmate is False. 
k @ # @ # @ # @
@ R @ # @ # @ #
# @ K @ # @ # @
@ # @ # @ # @ #
# @ # @ # @ # @
@ # @ # @ # @ #
# @ # @ # @ # @
@ # @ # @ # @ #
Black King Moves: []
Check: False
Checkmate: False
'''