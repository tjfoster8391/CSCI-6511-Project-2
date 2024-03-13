    


# formerly in LCVMove()
for futureSection in state.sectionList:
        
        if not (equals(futureSection, section) and not(futureSection.assigned == True)):
            print("LCV, in a legal section")
            for futureMove in futureSection.movesAllowed:
                if futureSection.movesAllowed[move] == True:
                    print("move: ", futureSection.movesAllowed[futureMove])
                    copyState = copy.deepcopy(state) # moveDone is fake until a find a way of choosning a mov
                    futureCopyState = applyMove(copyState, futureSection, futureMove)
                    if LCVmin == 0: 

                        LCVmin = constraintPropagation(futureCopyState, move)

                        print("legal moves after constraint propagation: ", LCVmin)
                        LCVMove = move
                    else: 
                        constrainedAmount = constraintPropagation(futureCopyState, move)
                        if constrainedAmount< LCVmin: 
                            LCVmin= constrainedAmount
                            print("legal moves after constraint propagation: ", LCVmin)
                            LCVMove = move