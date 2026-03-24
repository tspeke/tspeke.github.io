import math

def no_paths(w, h):

    """ 
    Consider a 2x2 grid:
    RRDD #
    RDRD #
    RDDR # Symetric with below
    DRRD 
    DRDR
    DDRR

    Basically push one R stepwise towards RHS, when reaches end move next R one step and move again towards end
    
    Consider a 3x3 grid:
    RRRDDD
    RRDRDD
    RRDDRD
    RRDDDR
    RDRRDD
    ...

    Answer is the number of permeatations of a str of length = size with half of letters equivalent
    
    Number of paths:
    
    N = (w + h)! / (w)!*(h)!

    """

    return math.factorial(w + h) // ( math.factorial(w) * math.factorial(h) )

print(no_paths(20, 20))