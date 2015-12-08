_MAXLOOKUP=500

def initValues(row,col):
    #return 1 if row==1 else row if col == 0 else row*2-1 if col==1 else 0
    if row==0: return 0
    if row==1: return 1
    if col==0: return row
    if col==1: return row*2-1
    return 0

def generateAmplificationTable(nForwards=10,nReverses=10):
    out=[[initValues(row,col) for col in range(nForwards+1)] for row in range(nReverses+1)] 
    for row in range(2,(nForwards+1)):
        for col in range(2,(nReverses+1)):
            out[row][col]=out[row-1][col]+out[row][col-1]+1
    return(out)

def cumsum(x):
    total = 0
    for y in x:
        total += y
        yield total

def countAmplifications(nForward,nReverse,isTerminal=True,onlyFirstPrimer=False):
    """Predicts the number of expected strand displacement amplifications for a region surrounded by a given number of primers.
    
       Calculates the expected amplifications for a region surrounded by nForward and nReverse primer binding sites in a multiple strand displacement amplification. This function uses a _MAXLOOKUP by _MAXLOOKUP lookup table for speed. If you need estimates for more primers than _MAXLOOKUP then perhaps generate your own table with generateAmplificationTable (watch out for numbers exceeding max float)

       Args:
           nForward (int): number of forward primers upstream of this region and within range of the polymerase
           nReverse (int): number of reverse primers downstream of this region and within range of the polymerase
           isTerminal (boolean): If True then there are no upstream forward primers to release the 5'-most forward primer in this set. If FALSE then the 5'-most forward primer is assumed to be released by an unknown upstream primer
           onlyFirstPrimer (boolean): If True then count only fragments whose initial fragment initiating from the 5'-most forward primer (mostly for internal usage to allow individual counting of sets of primers where only subsets overlap)
       
       Returns:
           int: the number of expected amplifications
    """
    if nForward>_MAXLOOKUP: raise(IndexError("nForward more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",_MAXLOOKUP))
    if nReverse>_MAXLOOKUP: raise(IndexError("nReverse more than max lookup %d (set to limit memory size of lookup table). Look at using generateAmplificationTable() to make your own table",_MAXLOOKUP))
    if nForward<0: raise(IndexError("nForward less than 0"))
    if nReverse<0: raise(IndexError("nReverse less than 0"))
    if onlyFirstPrimer: 
        return countAmplifications(nForward,nReverse,isTerminal)-countAmplifications(max(0,nForward-1),nReverse,False)
    if isTerminal:
        return _AMPLIFICATIONTABLE[nForward][nReverse]
    else:
        return _AMPLIFICATIONTABLE[nForward+1][nReverse]-1
   
def isSorted(x):
    return all([x[ii]<=x[ii+1] for ii in range(len(x)-1)])

def pairSortedForwardReverse(forwards,reverses,maxLength=None,returnPos=True):
    if maxLength is None: maxLength=30000
    if not isinstance(maxLength,list): maxLength=[maxLength]*len(forwards)
    if len(maxLength) != len(forwards): raise(ValueError("forwards and maxLength different lengths"))
    #if not sorted then we need to sort but that will lose correspondence with information outside the function or add unneccesary code so just throw error for now
    if not isSorted(forwards): raise(ValueError("Unsorted forwards"))
    if not isSorted(reverses): raise(ValueError("Unsorted reverses"))
    reverseIdStart=0
    nReverse=len(reverses)
    out=[]
    for forwardId in range(len(forwards)):
        out.append([]) 
        while reverseIdStart<nReverse and reverses[reverseIdStart]<forwards[forwardId]:
            reverseIdStart+=1
        reverseId=reverseIdStart
        while reverseId<nReverse and reverses[reverseId]<forwards[forwardId]+maxLength[forwardId] and reverses[reverseId]>=forwards[forwardId]:
            if returnPos: out[forwardId].append(reverses[reverseId])
            else: out[forwardId].append(reverseId)
            reverseId+=1
    return out

def predictAmplificationsSingleStrand(forwards,reverses,maxLength=30000,maxPosition=float('inf'),minPosition=1):
    #make sure unique
    forwards=sorted(list(set(forwards)))
    reverses=sorted(list(set(reverses)))
    #no -1 since we should step down on base following the end
    inRangeReverses=pairSortedForwardReverse(forwards,reverses,maxLength)
    forwardEnds=[x+maxLength for x in forwards]
    reverseStarts=[x-maxLength+1 for x in reverses]
    #add 1 to reverses since we should step down on the following base
    pos=forwards+forwardEnds+reverseStarts+[x+1 for x in reverses]
    pos.sort()
    #make sure the regions only cover between 1 and maxPosition
    out=[(max(minPosition,start),min(end-1,maxPosition)) for start,end in zip(pos[:-1],pos[1:]) if end>=minPosition and start<=maxPosition]
    #make sure we take the last tuple where several tuple describe the same location
    out=[(x[0],max(x[0],x[1])) for  x, lagX in zip(out,out[1:]+[(float('inf'),float('inf'),float('NaN'))]) if x[0]!=lagX[0]]
  #regionForwards<-lapply(out$start,function(x)inRangeReverses[forwards<=x&forwards>=x-maxLength+1])
    regionForwards=pairSortedForwardReverse([start-maxLength+1 for start,_ in out],forwards,maxLength,False)
    reverseCounts=[[sum([x>=end for x in inRangeReverses[forwardId]]) for forwardId in forwardIds] for forwardIds, end in zip(regionForwards,[x for _,x in out])]
    amps=[sum([countAmplifications(f,r,terminal,True) for f,r,terminal in zip(range(len(revCounts),0,-1),revCounts,[True]+[False]*(len(revCounts)-1))]) for revCounts in reverseCounts]
    out=[(x[0],x[1],y) for x,y in zip(out,amps)]
    return out

'''
def predictAmplificationsSingleStrand(forwards,reverses,maxLength=30000,maxPosition=float('inf')):
    #make sure unique
    forwards=list(set(forwards))
    reverses=list(set(reverses))
    #no -1 since we should step down on base following the end
    #inRangeReverses<-lapply(forwards,function(x)reverses[reverses>=x&reverses-x<maxLength])
    forwardId=0
    reverseId=0
    #for 
    #inRangeReverses=
    forwardEnds=[x+maxLength for x in forwards]
    reverseStarts=[x-maxLength+1 for x in reverses]
    forwardCounters=[1]*len(forwards) + [-1]*len(forwards) + [0]*2*len(reverses)
    reverseCounters=[0]*2*len(forwards) + [1]*len(reverses) + [-1]*len(reverses)
    #add 1 to reverses since we should step down on the following base
    sortedCounters=sorted(zip(forwards+forwardEnds+reverseStarts+[x+1 for x in reverses],forwardCounters,reverseCounters))

    sortedForwardCounts=cumsum([x for _,x,_ in sortedCounters])
    sortedReverseCounts=cumsum([x for _,_,x in sortedCounters])
    sortedPos=[x for x,_,_ in sortedCounters]
    sortedAmps=[countAmplifications(start,end) for start,end in zip(sortedForwardCounts,sortedReverseCounts)]
    
    #make sure the regions only cover between 1 and maxPosition
    out=[(max(1,start),min(end-1,maxPosition),amp) for start,end,amp in zip(sortedPos[:-1],sortedPos[1:],sortedAmps[:-1]) if end>=1 and start<=maxPosition]
    #make sure we take the last tuple where several tuple describe the same location
    out=[(x[0],max(x[0],x[1]),x[2]) for  x, lagX in zip(out,out[1:]+[(float('inf'),float('inf'),float('NaN'))]) if x[0]!=lagX[0]]
    return out
'''



def predictAmplifications(forwards,reverses,maxLength=30000,maxPosition=float('inf')):
    """Predicts the number of expected strand displacement amplifications for a set of primers.
    
       Calculates the expected amplifications across a genome for a set of forward and reverse primer binding sites used in multiple strand displacement amplification

       Args:
           forwards ([int]): The 5'-most position of primer landing sites on the forward strand
           reverses ([int]): The 3'-most position of primer landing sites on the reverse strand
           maxLength (int): The maximum length that the polymerase will amplify
           maxPosition (int): The maximum position that can be amplified i.e. the size of the target genome
       
       Returns:
           [(int,int,int),(int,int,int),...]: each tuple contains the start, end and expected amplifications for a region of the genome. Regions not predicted to amplify are not listed.
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


_AMPLIFICATIONTABLE=generateAmplificationTable(_MAXLOOKUP,_MAXLOOKUP)
"""Lookup table used by countAmplifications (could calculate each time but efficiency gain using table if many and/or large lookups).
"""

 





