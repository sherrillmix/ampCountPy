import argparse
import sys
import os
from ampcountpy import predictAmplifications 

def readBindingSites(siteFile):
    with open(siteFile, 'r') as f:
        sites=[int(x) for x in  f.read().split()]
    return sites

def check_file(targetFile):
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

def main(argv=None):
    if argv is None:
        argv=sys.argv[1:]

    parser = argparse.ArgumentParser(description="A program to count the number of expected amplifications for a set of forward and reverse primer landing sites in multiple strand displacement amplification. The command generates a csv file (default: output.csv, use `-o` or `--output` to change) with 3 columns; start of region, end of region, expected amplifications.")
    parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-f","--forwardPrimers", help="a text file containing the 1-based position of the first base of all primer landing sites on the forward strand separated by space or new lines",type=check_file,required=True)
    parser.add_argument("-r","--reversePrimers", help="a text file containing the 1-based position of the last base of all primer landing sites on the reverse strand separated by space or new lines",type=check_file,required=True)
    parser.add_argument("-l","--maxLength", help="an integer giving the maximum length expected for the polymerase ",type=check_positive_int,default=30000)
    parser.add_argument("-g","--genomeSize", help="an integer giving the maximum position possible for primers (if < 1 then set to the maximum position covered by primers)",type=int,default=-1)
    parser.add_argument("-o","--outFile", help="file to write to ",default="out.csv")
    args=parser.parse_args(argv)
        
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
    predictedAmps=predictAmplifications(forwards,reverses,args.maxLength,genomeSize)

    

    if args.verbose: print('Writing to '+args.outFile)
    with open(args.outFile, 'w') as f:
        f.write("start,end,amps\n")
        for start,end,amp in predictedAmps:
            f.write("%d,%d,%d\n" % (start,end,amp))

    if args.verbose: print('All done. Thanks')


if __name__ == '__main__':
    main(sys.argv[1:])
