from graphics import *


#direction vector 
grid = [[0 for i in range(16)] for i in range(16)] #Display all available points on the board via a two-dimensional array
directionX = [1,1,0,-1,-1,-1,0,1] 
directionY = [0,1,1,1,0,-1,-1,-1]
order=[8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]
window = GraphWin("Gomoku",452,550)
message = Text(Point(226,480),"") 
lastMove_AI = Text(Point(226,500),"") 
lastMove_human = Text(Point(226,520),"") 
turn = 1 #indicate who's turn is it
ai = 1 #ai's turn is 1;human's turn is 2
alpha=-100000  # initial value of alpha
beta=100000   # initial value of beta
pieces=[] # store all dropped piece 
gaveover = False 


#check the mouse click point are in the available zone
def checkInBoard(x,y):
    if(x>=0 and x<=15 and y>=0 and y<=15): return True
    else: return False
#Check the mouse click point in the board and no yet to drop a piece
def checkDrop(x,y):
    if(checkInBoard(x,y) and grid[x][y]==0): return True
    else: return False
#check the mouse click point if it is equal to i
def checkSameColor(x,y,i):
    if(checkInBoard(x,y) and grid[x][y]==i): return True
    else: return False
#The number of points with the same value as the key in the z-direction
def samekeyNumber(x,y,z,i,key,sk):
    if(i==1):
        while(checkSameColor(x+directionX[z]*i,y+directionY[z]*i,key)):
            sk+=1
            i+=1   

    elif(i==-1):
        while(checkSameColor(x+directionX[z]*i,y+directionY[z]*i,key)):
            sk+=1
            i-=1
    return sk,i
#Count the number of pieces of the same color in the z direction
def pieceinLine(x,y,z):
    i=x+directionX[z]; j=y+directionY[z]
    s=0; ref=grid[x][y]
    if(ref==0): return 0
    while(checkSameColor(i,j,ref)):
        s,i,j=s+1,i+directionX[z],j+directionY[z]
    return s
#to see if the gave is over
def gameOver(x,y):
    global gaveover
    for u in range(4):#if the pieces is morethan 4, gameover
        if((pieceinLine(x,y,u)+pieceinLine(x,y,u+4))>=4):
            gaveover=True
            return True
    return False


#Evaluation function to get a score
def evaluation(x,y):
    global gaveover
    if(gameOver(x,y)):
        gaveover=False
        return 10000
    score=openFour(x,y)*1000+(continuousFour(x,y)+openThree(x,y))*100
    
    for u in range(8):
        if(checkInBoard(x+directionX[u],y+directionY[u]) and grid[x+directionX[u]][y+directionY[u]]!=0):
            score=score+1
    return score
#The number of openFour situations in the four directions of the landing point
def openFour(x,y):
    key,number=grid[x][y],0
    for u in range(4):
        samekey=1
        samekey,i=samekeyNumber(x,y,u,1,key,samekey)
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        samekey,i=samekeyNumber(x,y,u,-1,key,samekey)
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        if(samekey==4):
            number=number+1
    return number
#Continuousfour is a position where, in addition to a "open four", one more move can form a five-row
#The number of Four situations in the four directions of the landing point 
def continuousFour(x,y):
    key=grid[x][y]; number=0
    for u in range(8):
        samekey=0; flag=True; i=1
        while(checkSameColor(x+directionX[u]*i,y+directionY[u]*i,key) or flag):
            if(not checkSameColor(x+directionX[u]*i,y+directionY[u]*i,key)):
                if(flag and checkInBoard(x+directionX[u]*i,y+directionY[u]*i) and grid[x+directionX[u]*i][y+directionY[u]*i]!=0):
                    samekey-=10
                flag=False
            samekey+=1
            i+=1
        i-=1
        if(not checkInBoard(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        samekey,i=samekeyNumber(x,y,u,-1,key,samekey)
        if(samekey==4):
            number+=1
    return number-openFour(x,y)*2
#The number of open threes in the four directions and the number of dead threes in the eight directions of the point
def openThree(x,y):
    key=grid[x][y]; number=0
    for u in range(4):
        samekey=1
        samekey,i=samekeyNumber(x,y,u,1,key,samekey)
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        if(not checkDrop(x+directionX[u]*(i+1),y+directionY[u]*(i+1))):
            continue
        samekey,i=samekeyNumber(x,y,u,-1,key,samekey)
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        if(not checkDrop(x+directionX[u]*(i-1),y+directionY[u]*(i-1))):
            continue
        if(samekey==3):
            number+=1
    for u in range(8):
        samekey=0; flag=True; i=1
        while(checkSameColor(x+directionX[u]*i,y+directionY[u]*i,key) or flag):
            if(not checkSameColor(x+directionX[u]*i,y+directionY[u]*i,key)):
                if(flag and checkInBoard(x+directionX[u]*i,y+directionY[u]*i) and grid[x+directionX[u]*i][y+directionY[u]*i]!=0):
                    samekey-=10
                flag=False
            samekey+=1
            i+=1
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        if(checkInBoard(x+directionX[u]*(i-1),y+directionY[u]*(i-1)) and grid[x+directionX[u]*(i-1)][y+directionY[u]*(i-1)]==0):
            continue
        samekey,i=samekeyNumber(x,y,u,-1,key,samekey)
        if(not checkDrop(x+directionX[u]*i,y+directionY[u]*i)):
            continue
        if(samekey==3):
            number+=1
    return number


#Game Tree
def GameTree1():
    timer=0
    global alpha
    alpha=-100000
    if(grid[8][8]==0): #drop a piece in the middle of the board if there has not a piece
        return dropPiece(8,8)
    keyi=-1; keyj=-1
    #Iterate over x, y coordinates 
    for x in order:  
        for y in order:
            timer+=1
            if(not checkDrop(x,y)):
                continue
            grid[x][y]=ai
            #use evaluation functon to get a score accourding to the coordinates
            tempp=evaluation(x,y)
            if(tempp!=0):
                print(f'The evaluation score for ({x},{y}) is {tempp}')
            if(tempp==0):
                grid[x][y]=0; continue
            if(tempp==10000):
                print(f'Total search time is: {timer}')
                return dropPiece(x,y)
            #enter into gametree depth 2
            tempp=GameTree2()
            grid[x][y]=0
            if(tempp>alpha): #get max value 
                alpha=tempp; keyi=x; keyj=y
    dropPiece(keyi,keyj)

def GameTree2():
    global beta 
    beta=100000
    for x in order:
        for y in order:
            if(not checkDrop(x,y)):
                continue
            grid[x][y]=3-ai
            tempp=evaluation(x,y)
            if(tempp==0):
                grid[x][y]=0; continue
            if(tempp==10000):
                grid[x][y]=0; return -10000
            tempp=GameTree3(tempp)
            if(tempp<alpha): #Pruning level 1
                grid[x][y]=0; return -10000
            grid[x][y]=0
            if(tempp<beta): #get minimum value
                beta=tempp
    return beta

def GameTree3(p2):
    keyp=-100000
    for x in order:
        for y in order:
            if(not checkDrop(x,y)):
                continue
            grid[x][y]=ai
            tempp=evaluation(x,y)
            if(tempp==0):
                grid[x][y]=0; continue
            if(tempp==10000):
                grid[x][y]=0; return 10000
            if(tempp-p2*2>beta): ##Pruning level 2
                grid[x][y]=0; return 10000
            grid[x][y]=0
            if(tempp-p2*2>keyp): #get max value
                keyp=tempp-p2*2
    return keyp


#human play
def humanPlay():
    position=window.getMouse()
    x,y=round(position.getX()/30),round(position.getY()/30)
    dropPiece(x,y) if checkDrop(x,y) else humanPlay()
#drop a piece and check if the game is over
def dropPiece(x,y):
    global gaveover
    piece=Circle(Point(x*30,y*30),13)
    if(turn==ai):
        grid[x][y]=ai
        lastMove_AI.setText("AI:(x:y)=("+str(x)+":"+str(y)+")")
        piece.setFill('black')
    else:
        grid[x][y]=3-ai
        lastMove_human.setText("Player:(x:y)=("+str(x)+":"+str(y)+")")
        piece.setFill('white') 
    piece.draw(window)
    pieces.append(piece)

    if(gameOver(x,y)):
        if(turn==ai):
            message.setFill('red')
            message.setText("AI Win! Click anywhere to quit")
        else:
            message.setFill('red')
            message.setText("Player Win! Click anywhere to quit")
            
#draw the gomoku board
def initBoard():
    #Set back ground color
    window.setBackground('#f8df70')
    #draw lines vertical 
    for i in range(0,451,30):
        line=Line(Point(i,0),Point(i,450))
        line.draw(window)
    #draw lines vertical horizontal
    for j in range(0,451,30):
        line=Line(Point(0,j),Point(450,j))
        line.draw(window)
    message.draw(window)
    lastMove_AI.draw(window)
    lastMove_human.draw(window)
    
##------------------------------------------------------------------##
if __name__=='__main__':
    initBoard()
    while(not gaveover):
        if(turn==ai):
            message.setText("AI's turn")
            GameTree1()
        else:
            message.setText("Your turn")
            humanPlay()
        #make turns 1 is AI's turn; 2 is human players turn
        turn=3-turn
    
    #use to quit the game
    window.getMouse()
    window.close()