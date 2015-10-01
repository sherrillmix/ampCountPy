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


__AMPLIFICATIONTABLE__=generateAmplificationTable(__MAXLOOKUP__,__MAXLOOKUP__)

def cumsum(x):
    total = 0
    for y in x:
        total += y
        yield total

def checkFile(targetFile):
    if not os.path.isfile(targetFile):
        raise argparse.ArgumentTypeError(targetFile+' is not a file')
    if os.access(targetFile, os.R_OK):
        return targetFile
    else:
        raise argparse.ArgumentTypeError(targetFile+' is not readable')

def check_positive_int(value):
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError("%s is less than 1" % value)
    return ivalue

def readBindingSites(siteFile):
    with open(siteFile, 'r') as f:
        sites=[int(x) for x in  f.read().split()]
    return sites

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

 

def main(argv):
    parser = argparse.ArgumentParser(description="A program to count the number of expected amplifications for a set of forward and reverse primer landing sites in multiple strand displacement amplification. The command generates a csv file (default: output.csv, use `-o` or `--output` to change) with 3 columns; start of region, end of region, expected amplifications.")
    parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-f","--forwardPrimers", help="a text file containing the 1-based position of the first base of all primer landing sites on the forward strand separated by space or new lines",type=checkFile,required=True)
    parser.add_argument("-r","--reversePrimers", help="a text file containing the 1-based position of the last base of all primer landing sites on the reverse strand separated by space or new lines",type=checkFile,required=True)
    parser.add_argument("-l","--maxLength", help="an integer giving the maximum length expected for the polymerase ",type=check_positive_int,default=30000)
    parser.add_argument("-g","--genomeSize", help="an integer giving the maximum position possible for primers (if < 1 then set to the maximum position covered by primers)",type=int,default=-1)
    parser.add_argument("-o","--outFile", help="file to write to ",default="out.csv")
    args=parser.parse_args()
        
    if args.verbose:
        print("Arguments: ")
        for key, value in vars(args).items():
            print("   "+key+": "+str(value))

    if args.genomeSize<1:
        genomeSize=float("inf")
    else:
        genomeSize=args.genomeSize
        
    if args.verbose: print('Reading forwards')
    forwards=readBindingSites(args.forwardPrimers)
    if args.verbose: print('Reading reverses')
    reverses=readBindingSites(args.reversePrimers)

    if args.verbose: print('Predicting forward amplifications')
    plusStrand=predictAmplifications(forwards,reverses,args.maxLength,genomeSize)


    

    if args.verbose: print('Writing to '+args.outFile)
    with open(args.outFile, 'w') as f:
        for start,end,amp in zip(starts,ends,amps):
            f.write("%d,%d,%d\n" % (start,end,amp))

    if args.verbose: print('All done. Thanks')




if __name__ == '__main__':
    import argparse
    import sys
    import os
    main(sys.argv)

