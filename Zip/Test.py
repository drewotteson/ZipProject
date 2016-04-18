import sys

def Main():
    if ".zip" in sys.argv[1]:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv[1]))
    else:
        print('Not a zip file')



Main()



