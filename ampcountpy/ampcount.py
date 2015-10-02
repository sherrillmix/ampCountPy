__MAXLOOKUP__=500

def initValues(row,col):
    #return 1 if row==1 else row if col == 0 else row*2-1 if col==1 else 0
    if row==0: return 0
    if row==1: return 1
    if col==0: return row
    if col==1: return row*2-1
    return 0

def generateAmplificationTable(nForwards=10,nReverses=10):
    out=[[initValues(row,col) for col in range(nForwards+1+1)] for row in range(nReverses+1+1)] 
    for row in range(2,(nForwards+1+1)):
        for col in range(2,(nReverses+1+1)):
            out[row][col]=out[row-1][col]+out[row][col-1]+1
    return(out)

def cumsum(x):
    total = 0
    for y in x:
        total += y
        yield total

def countAmplifications(nForward,nReverse):
    """Predicts the number of expected strand displacement amplifications for a region surrounded by a given number of primers.
    
       Calculates the expected amplifications for a region surrounded by nForward and nReverse primer binding sites in a multiple strand displacement amplification. This function uses a __MAXLOOKUP__ by __MAXLOOKUP__ lookup table for speed. If you need estimates for more primers than __MAXLOOKUP__ then perhaps generate your own table with generateAmplificationTable (watch out for numbers exceeding max float)

       Args:
           nForward (int): number of forward primers upstream of this region and within range of the polymerase
           nReverse (int): number of reverse primers downstream of this region and within range of the polymerase
       
       Returns:
           int: the number of expected amplifications
    """
    if nForward>__MAXLOOKUP__: raise(IndexError("nForward more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",maxLookup))
    if nReverse>__MAXLOOKUP__: raise(IndexError("nReverse more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",maxLookup))
    if nForward<0: raise(IndexError("nForward less than 0"))
    if nReverse<0: raise(IndexError("nReverse less than 0"))
    return __AMPLIFICATIONTABLE__[nForward][nReverse]
   
def predictAmplificationsSingleStrand(forwards,reverses,maxLength=30000,maxPosition=float('inf')):
    #make sure unique
    forwards=list(set(forwards))
    reverses=list(set(reverses))
    forwardEnds=[x+maxLength for x in forwards]
    reverseStarts=[x-maxLength for x in reverses]
    forwardCounters=[1]*len(forwards) + [-1]*len(forwards) + [0]*2*len(reverses)
    reverseCounters=[0]*2*len(forwards) + [1]*len(reverses) + [-1]*len(reverses)
    sortedCounters=sorted(zip(forwards+forwardEnds+reverseStarts+reverses,forwardCounters,reverseCounters))

    sortedReverseCounts=cumsum([x for _,_,x in sortedCounters])
    sortedForwardCounts=cumsum([x for _,x,_ in sortedCounters])
    sortedPos=[x for x,_,_ in sortedCounters]
    sortedAmps=[countAmplifications(start,end) for start,end in zip(sortedForwardCounts,sortedReverseCounts)]
    
    #make sure the regions only cover between 1 and maxPosition
    out=[(max(1,start),min(end,maxPosition),amp) for start,end,amp in zip(sortedPos[:-1],sortedPos[1:],sortedAmps[:-1]) if end>=1 and start<=maxPosition]
    return out

def predictAmplifications(forwards,reverses,maxLength=30000,maxPosition=float('inf')):
    """Predicts the number of expected strand displacement amplifications for a set of primers.
    
       Calculates the expected amplifications across a genome for a set of forward and reverse primer binding sites used in multiple strand displacement amplification

       Args:
           forwards ([int]): The 5'-most position of primer landing sites on the forward strand
           reverses ([int]): The 3'-most position of primer landing sites on the reverse strand
           maxLength (int): The maximum length that the polymerase will amplify
           maxPosition (int): The maximum position that can be amplified i.e. the size of the target genome
       
       Returns:
           list of tuples: each tuple contains the start, end and expected amplifications for a region of the genome. Regions not predicted to amplify are not listed.
    """

    forwardPred=predictAmplificationsSingleStrand(forwards,reverses,maxLength,maxPosition)
    #use last end of forward pred as base for inverting the positions
    maxPosition=forwardPred[-1][1]
    reversePred=predictAmplificationsSingleStrand([maxPosition-x+1 for x in reverses],[maxPosition-x+1 for x in forwards],maxLength,maxPosition)
    #reverse and turn back to forward strand indexing
    reversePred=[(maxPosition-end+1,maxPosition-start+1,amp) for start, end, amp in reversePred[::-1]]
    if any([forward[0]!=reverse[0] or forward[1]!=reverse[1] for forward, reverse in zip(forwardPred,reversePred)]): raise(BaseException('Mismatched start and end between strands in predictAmplifications'))
    out=[(forward[0], forward[1], forward[2]+reverse[2]) for forward,reverse in zip(forwardPred,reversePred)]
    return(out)


__AMPLIFICATIONTABLE__=generateAmplificationTable(__MAXLOOKUP__,__MAXLOOKUP__)
    """Lookup table used by countAmplifications (could calculate each time but efficiency gain using table if many and/or large lookups).
    """

 





