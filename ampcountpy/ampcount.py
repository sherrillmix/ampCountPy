__MAXLOOKUP__=1000


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
    if nForward>__MAXLOOKUP__: raise(IndexError("nForward more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",maxLookup))
    if nReverse>__MAXLOOKUP__: raise(IndexError("nReverse more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",maxLookup))
    if nForward<0: raise(IndexError("nForward less than 0"))
    if nReverse<0: raise(IndexError("nReverse less than 0"))
    return __AMPLIFICATIONTABLE__[nForward][nReverse]
   
def predictAmplifications(forwards,reverses,maxLength=30000,maxPosition=float('inf')):
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

__AMPLIFICATIONTABLE__=generateAmplificationTable(__MAXLOOKUP__,__MAXLOOKUP__)

 





