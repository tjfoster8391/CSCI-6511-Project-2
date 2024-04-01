#T. J. Foster
# CSCI 6511
# Project 2: Constraint Satisfaction Problem
# 3/12/2024
# must have an appropriate tilesproblem text file in working directory
# IE tilesproblem_1326658924404900.txt

import copy

class State: # the landscape 
    def __init__(self):
        self.stateColorCounter = {1: 0, 2: 0, 3: 0, 4: 0}
        self.dim= 0 # either 20 or 25

        self.landscape  = [[0 for i in range(20)] for j in range(20)]#2D array with full landscape 

        self.sectionList = []# 1D array with starting points for each 4x4 grid square "variable" or "section".  
                            # sections processed regardless of 2D position, read one afte the other 
  
    # break it up into variables with starting points 
        self.tilesRemaining = dict() # tracks remaining tiles to place

        # make target 


class section: # 4x4 grid 
    def __init__(self, top: int, left: int):
        self.top = top
        self.left = left
        #self.tile = 0
        self.assigned = False # set to true when a move is ultimately applied 
        self.movesAllowed = {1: True, 2: True, 3: True, 4: True, 5:True, 6:True} # tracks legality of each move on that tile
                                                                                 # based on previous constraint propagations

#def toString():
    # return "Section. top: " + self.top,"left: " + self.left, "assigned: " + self.assigned
        
def equals(section1: section, section2: section):
    if section1.top == section2.top and section1.left == section2.left:
            return True
        
    return False
        # create "section" class, each section is a "variable"
colorEnum = {1, 2, 3, 4}
origLandscape = State()
targets = {1:0, 2:0, 3:0, 4:0}
recursiveCounter = 0


#tilesRemaining = dict() I don't want moves used for LCV, MRV, and constraint propagation to affect original state 
def readFile(fileName: str): # processes file with all the landscape data 
    #print("in readFile")
    file = open(fileName, "r")

    file.readline() # skip descriptive lines in file. 
    file.readline()
    global origLandscape



    for I in range (20): 
        thisRow = file.readline()
        #print("this row: ", thisRow)
        #print("storing file lines")
        
        for J in range(0, len(thisRow)-1, 2):  # alternate every 2nd character to deal with spaces
         
            origLandscape.landscape[I][int(J/2)] = thisRow[J] # populate 2D array with 
           
            if thisRow[J] != " ":
                origLandscape.stateColorCounter[int(thisRow[J])] += 1 # track color instances
   
    print("landscape read:")
    print(origLandscape.landscape)
    print(origLandscape.stateColorCounter)
        
    file.readline()
    file.readline()

    tilesString = file.readline()

    processTileString(origLandscape, tilesString)

 
    print(origLandscape.tilesRemaining)


    # process file string

    file.readline()
    file.readline()

    global targets 
    for I in range(1, 5): # read for lines each with a color and a target 
        targetString = file.readline().split(":")
        print(targetString)
        

        targets[I] = int(targetString[1])

    print(targets)
    # process targets string 
    divideSections(origLandscape) # break landscape into sections 

    assignTiles(origLandscape) # call the first 

def processTileString(state: State, tilesString: str):

    tileCounts = tilesString.split(",")

    tileI = 1
    print(tileCounts)
    #global tilesRemaining
    for tile in tileCounts:
       
        secondToLast = len(tile)-2 # the actual last character is '\n', I want the last number
        last = len(tile) -1 # last character, sufficient for a 1-digit qualitity
        if tile[secondToLast].isnumeric(): 
            state.tilesRemaining[tileI] = tile[last-1] # double check python indexing, including strings
        else: 
            state.tilesRemaining[tileI] = tile[last]
        tileI += 1
    state.tilesRemaining[3] = 10 #!!!!!!!!!!!!!!!!!hardcode for now
    for number in state.tilesRemaining: 
        state.tilesRemaining[number] = int(state.tilesRemaining[number]) # turn values into integers for counter

def divideSections(state: State): # divide section into 4x4 with top and right coords 
    #print(" in divideSections")
    for I in range (0, len(state.landscape), 4):
        for J in range (0, len(state.landscape[0]), 4):
            newSection = section(I, J)
            # no need to populate section with landscape values
            # just use sections for top-left coords and change original landscape view with other functions
            state.sectionList.append(newSection) # use 1D array 
    #print("sectionlist length: ", len(state.sectionList))
    

    

def assignTiles(origLandscape: State): # first iteration. 
    
        #print("in assign tiles")

        
        nextSect = chooseMRV(origLandscape) # choose variable with minimimum remaining values, IE the fewest legal moves


        nextMove = chooseLCV(origLandscape, nextSect) # choose the legal move which constrains the leasst future moves 

        # assign the state with that move implemented to origLandscape 
        #print("move applied from assignTiles")
        #print("section chosen: ", nextSect.top, " ", nextSect.left)

        origLandscape = applyMove(origLandscape, nextSect, nextMove) # apply constraint propagation to prune future moves that violate constraitn

  
        prop = constraintPropagation(origLandscape) # constraint propagation on actual landscape



        print(origLandscape.landscape)
        print(origLandscape.stateColorCounter)
      
        # decide what happens when it works 
        assignTilesRecursive(origLandscape, nextSect, nextMove) # recursively call for future iterations 

def assignTilesRecursive(state: State, lastSection: section, LastMove: int):
    global recursiveCounter
    #print("in assignTilesRecursive")
    #print("recursive calls: ", recursiveCounter)
    recursiveCounter += 1
    if meetsContraint(state) == False: # base case: constraint is not met. 
            print("assignment failed")
            print(state.tilesRemaining)
            print(origLandscape.landscape)
            print(origLandscape.stateColorCounter)
            return
    else: 
        tilesAllUsed = True # might be true, will become false if a tile is still available
        for I in state.tilesRemaining: 

            if state.tilesRemaining[I] >=0: 
                tilesAllUsed = False
        if tilesAllUsed == True: # if all tiles have been used, all tiles assigned
                print("all tiles assigned")
                print(state.tilesRemaining)
                print(origLandscape.landscape)
                print(origLandscape.stateColorCounter)
                return


        
            
    
     #recursive case 


    nextSec = chooseMRV(state) # choose next unassigned variable 

    #print("section chosen by MRV: ", nextSec.top, nextSec.left)

    nextMove = chooseLCV(state, nextSec) # choose least constraining move allowed on that variable. 
    
   

    #print("move choosen in assignmove: ", nextMove)

    #print("section chosen in assignTilesRecursive", nextSec.top, " ", nextSec.left)

    #print("move applied from applyTilesRecursive")
    state = applyMove(state, nextSec, nextMove) # apply chosen move to state

    prop = constraintPropagation(state) # constraint propagation on actual landscape
                                                  # no tile or move input needed: all unassigned sections acted upon based
                                                  # based on new state of last move
    assignTilesRecursive(state, nextSec, nextMove)

    # call recursive function
    # what, if anything, does this return? 



def constraintPropagation(state: State): # eliminates other moves that are impossible given the current state
    # can either be used in choosing the LCV to count how many moves it would constrain in a copy
    # or used after the current move in the true state to prune future moves 
    #print("in constraintPropagation")
    movesConstrained = 0
    for I in range(len(state.sectionList)): 
    #for futureSec in state.sectionList:
        # does not depend on which section was must recently moved upon
        # it changes whatever moves would be allowed based only on the last move
        # because all previous moves made already had constraint propagation used after them
        futureSec = state.sectionList[I] # go through all sections that have not been assigned a move already. 
        if futureSec.assigned == False: 


            for move in futureSec.movesAllowed: # go through each move 
                if futureSec.movesAllowed[move] == True: # ignore moves that have previously been pruned, might be pruned later
                    futureTestState = copy.deepcopy(state) # make another copy to apply the move and see if it is allowed given current state
                                                            # without affecting the current state, if not, just disallow the current state
                    #print("move applied from constraint propagation")
                    futureTestState = applyMove(futureTestState, futureTestState.sectionList[I], move)  
                    # use the result to see if its allowed
                    if meetsContraint(futureTestState) == False: 
                        #print(" future move pruned")
                        futureSec.movesAllowed[move] == False # pruning future moves 
                        movesConstrained += 1 # counting moves to see how much a hypothetical move would constrain 
                    else: 
                        #print("future move not pruned")
                        pass
                

    #print("end of constraint propagation")
    return movesConstrained # return moves constrained 




def chooseLCV(state: State,section: section):  # choose move for chosen section that constrains the least future moves 
    #print("in choose LCV")
    LCVMin = 0
    LCVMove = 0#find an object type for move
    
    for move in section.movesAllowed: 
        tileCode = 0 #check to make sure I still have tiles remaining for that move 
        if move >2: # each EL tile is a separate move, but the same tile option 
            tileCode = 3
        else: 
            tileCode = move
        if (section.movesAllowed[move] == True) and (state.tilesRemaining[tileCode] > 0) : 
            
            LCVState = copy.deepcopy(state) # make a copy 
            #print("move applied from chooseLCV")
            LCVState = applyMove(LCVState, section, move) # apply the new move and 
            if LCVMin == 0: # in case this is the first move checked
                LCVMin = constraintPropagation(LCVState) # count constraining based on propagation

                LCVMove = move
            else: 
                constrainedAmount = constraintPropagation(LCVState)# test restraints for this move
                if constrainedAmount < LCVMin: # if it has the new min, choose it instead 
                    LCVMin = constrainedAmount
                    LCVMove = move
    


    if LCVMove != 0: 
        #print("move chosen: ", LCVMove)
        pass
    else: 
        #print("no move chosen")
        pass
    return LCVMove # should be an int, the keys of the move options 

        
  
def chooseMRV(state: State): # choose the available variable with the smallest number of legal moves, 
                            # tracked in that section's movesAllowed dictionary 
    #print("in choose MRV")
    MRVmin = 0
    MRVSect = section(0, 0)

    tiedMinSections = dict() # stories multiple MRV's if there's a tie


    
    for I in range( len(state.sectionList)): # figure out how to do sections
        #print("var status: ", var.assigned)
        var = state.sectionList[I]
        if var.assigned == True:
            continue
        #print("var: ", var.top, var.left)
        
        varMoveCtr = 0
        for J in var.movesAllowed:  
            if var.movesAllowed == True:
                varMoveCtr += 1
        if MRVmin == 0:  # determine minimum, first case is if this is the first one counter 
            MRVmin = varMoveCtr
            MRVSect = var
        else: 
            if varMoveCtr == MRVmin: # if it is tied for min with previous value
                tiedMinSections[I] = MRVmin # add that section's index with that value
            if varMoveCtr < MRVmin: # for other cases, track the new minimum
                MRVmin = varMoveCtr
                MRVSect = state.sectionList[I]
                for minCheck in tiedMinSections: 
                    # if there is a new min, remove all MRV's from previous min with larger values
                    # no test necessary all min's in the dictionary have the same value, which has been beaten by this one
                    tiedMinSections.pop(minCheck) # remove all previous tied ones from the 
                tiedMinSections[I] = MRVSect# add new one to dictionary
    if len(tiedMinSections) > 1: # if there is more than one section tied for min
        tieBreakerMax = 0
        tieBreakerSection = section(0, 0)
        for I in tiedMinSections: # go through each tie
         
                tieBreakerVal = tieBreakerValue(state, tiedMinSections[I]) # compute how many future moves constrained
                                                                           # by each move of tied MRV sections
                                                                            # pick section that constrains the most future moves
                if tieBreakerVal >  tieBreakerMax: # if a new tieBreaker value is greater, make that section the new max
                    tieBreakerMax= tieBreakerVal
                    tieBreakerSection = tiedMinSections[I]
        MRVSect = tieBreakerSection
        # the originally ties sections still might have a tie in this case
        # ignore future ties from here
            
    else: 
        return MRVSect


    return MRVSect


def tieBreakerValue(state: State, section: section):  # go through all moves in this value and how many values
                                                      # are constrained by a move in this 
    constraintOccurances = 0

    for move in section.movesAllowed: 
        moveTestState = applyMove(state, section, move)
        constraintOccurances += constraintPropagation(moveTestState)
    
    return constraintOccurances
    
def meetsContraint (state: State): # tests a state at various points to see if it meets the constraints 
    #print("in meets constraint")
    for color in colorEnum: # if the process eliminates too many of a given color
        if state.stateColorCounter[color] < targets[color]:
            return False
    # make a copy of the tile counter for this pah. 
    for tileCount in state.tilesRemaining: # if there is too few of a tile 
        if state.tilesRemaining[tileCount] < 0:
            return False
    if (state.tilesRemaining[1] == 0 and state.tilesRemaining[2] == 0 and state.tilesRemaining[3] == 0): # if all tiles are used up
            return False
    return True

def applyMove(state: State, section: section, moveCode: int): # apply a chosen move to a section in a given state

    #print("in applyMove")
    #print("section: ",section.top, " , " , section.left)
    #global tilesRemaining
    if moveCode == 1: 
        state = applyBox(state, section.top, section.left)
    if moveCode == 2: 
        state = applyBorder(state, section.top, section.left)
    if moveCode == 3: 
        state = applyEL1(state, section.top, section.left)
    if moveCode == 4: 
        state = applyEL2(state, section.top, section.left)
    if moveCode == 5: 
        state = applyEL3(state, section.top, section.left)
    if moveCode == 6: 
        state = applyEL4(state, section.top, section.left)
   
    if moveCode <3: # decrement that move's tile
        state.tilesRemaining[moveCode] -= 1
    else: 
        state.tilesRemaining[3] -= 1

    section.assigned = True
    return state
    
# function to apply each different shape 
def applyBox(state: State, top: int, left: int): #solid box 
    #print("apply box")
    
    for I in range(left, left +4):
        for J in range(top, top + 4):
            thisColor = state.landscape[I][J]
            eraseColor(state, thisColor, I, J)
 
    return state



def applyEL1(state:State, top, left): # each orientation of EL is a combination of two edges' code 
    #print("applyEL1")
    for I in range(top, top+4):
        
        thisColor = state.landscape[I][left]
        eraseColor(state, thisColor, I, left)
    for J in range (left, left + 4):
        thisColor = state.landscape[top][J]
        eraseColor(state, thisColor, top, J)
    
    return state
def applyEL2(state:State, top, left):

    #print("apply EL2")
    for I in range(top, top+4):
        
        thisColor = state.landscape[I][left+3]
        eraseColor(state, thisColor, I, left+3)
    for J in range (left, left + 4):
        thisColor = state.landscape[top+3][J]
        eraseColor(state, thisColor, top+3, J)
    return state
def applyEL3(state:State, top, left):
    ##print("apply El3")
    for I in range(top, top+4):
        
        thisColor = state.landscape[I][left]
        eraseColor(state, thisColor, I, left)

    for J in range (left, left + 4):
        thisColor = state.landscape[top+3][J]
        eraseColor(state, thisColor, top+3, J)
    return state

def applyEL4(state:State, top, left):
    #print("apply EL4")
   # #print("top: ", top, ". top + 4", top + 4)
    for I in range(top, top+4):
        
        thisColor = state.landscape[I][left+3]
        eraseColor(state, thisColor, I , left + 3)
    for J in range (left, left + 4):
        thisColor = state.landscape[top][J]
        eraseColor(state, thisColor, top, J)
    
    return state
def applyBorder (state: State, top: int, left: int): # border 
    #print("apply border")

    #print("top: ", top, ". left", left)
    for I in range(top, top+4):
        

        thisColor = state.landscape[I][left]
        eraseColor(state, thisColor, I, left)
    for J in range (left, left + 4):
        thisColor = state.landscape[top][J]
        eraseColor(state, thisColor, top, J)
    
    for I in range(top, top+4):
        
        thisColor = state.landscape[I][left+3]
        eraseColor(state, thisColor, I, left + 3)
    for J in range (left, left + 4):
        thisColor = state.landscape[top+3][J]
        eraseColor(state, thisColor, top+3, J)
    return state
def eraseColor(state: State, color: int, I: int, J: int): # erase 
            #print("in erase color")
            if color != ' ':
                state.stateColorCounter[int(color)] -= 1
            state.landscape[I][J] = " "

def main():
    readFile("tilesproblem_1326658924404900.txt")
    #readFile("tilesproblem_1326658931783100.txt")

main()