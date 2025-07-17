import math
import random
from collections import Counter


def random_emission_sequence(length, p_start, p_trans, p_emit):
    """Generates a random emission sequence and corresponding state path.

    Parameters:
        length (int): Length of the sequence.
        p_start (dict): Starting probabilities
        p_trans (dict): Transition probabilities
        p_emit (dict): Emission probabilities

    Returns:
        state_path (str): Sequence of states
        emissions (str): Sequence of emissions
    """
    states = []
    emissions = []

    #Initial state -> chooses randomly Fair (F) or B (Biased) based on the the start probabilities
    #weights -> Probabilities to choose either F or B
    current_state = random.choices(list(p_start.keys()), weights=p_start.values())[0] # <- returns a list with only one item = State

    states.append(current_state) #Add Start State to List of visited States

    #Emit based on initial state -> current state (B or F) is the key for the emission probabilities
    #Emission Probabilities contain the probabilities for Heads or Tails 
    emission = random.choices(list(p_emit[current_state].keys()), weights=p_emit[current_state].values())[0]
    emissions.append(emission) #Add Emmission to List of seen Emissions

    for i in range(1, length): #Travel through Sequence
        #Transition to next state based on Transition Probailities for current states
        current_state = random.choices(list(p_trans[current_state].keys()), weights=p_trans[current_state].values())[0]
        states.append(current_state) #Add State to visited States

        #Emit symbol from current state based on Emission probabilities of the current state
        emission = random.choices(list(p_emit[current_state].keys()), weights=p_emit[current_state].values())[0]
        emissions.append(emission)

    return ''.join(states), ''.join(emissions) #Returns a String for all visited States and all Emitted Letters (H or T)


def viterbi(eseq, p_start, p_trans, p_emit):
    """Implements the Viterbi algorithm to find the most likely hidden state path.

    Parameters:
        eseq (str): Emission sequence HTHHHTTHHTHTHTHTHTHTHTTHTTHHTHTHHTTHHHHHHHHHHHHHHHHHHHHH
        p_start (dict): Starting probabilities for each state
        p_trans (dict): Transition probabilities between states
        p_emit (dict): Emission probabilities for each state and observation

    Returns:
        best_path (str): Most likely sequence of hidden states
        best_prob (float): Probability of that best path
    """
    states = list(p_start.keys())  #List of all possible states, here ['F', 'B']
    n = len(eseq)  #Length of the emission sequence
    all_symbols = list({sym for emits in p_emit.values() for sym in emits}) #saves all possible symbols in a list
    
    #Convert all probabilities to log-space to avoid numeric underflow
    log_start = {s: math.log(p_start[s]) for s in states}                                   #Log of start probabilities
    log_trans = {s1: {s2: math.log(p_trans[s1][s2]) for s2 in states} for s1 in states}     #Log of transition probabilities
    log_emit = {s: {e: math.log(p_emit[s][e]) for e in all_symbols} for s in states}        #Log of emission probabilities

    #Initialize dynamic programming tables
    V = [{} for _ in range(n)]  #Viterbi table: V[time][state] = max Log-Probability for each state
    backpointer = [{} for _ in range(n)]  #Backpointer table: stores previous best state for path reconstruction

    #Initialization step (t = 0)
    #V[t=0][state] = Start Probability for that State + Emission prob for first symbol
    for s in states:
        V[0][s] = log_start[s] + log_emit[s][eseq[0]]  #Addition in Log translates to multiplication! 
        backpointer[0][s] = None  #No predecessor at time 0

    #Iterate through emission sequence -> start at 1 as 0 was already initialized
    for t in range(1, n): 
        for s in states:

            candidates = [] #Tuples of: (Probability, previous state) 
            
            #For current state s, consider all possible previous states s_prev
            for s_prev in states:
                #Compute total log-prob: previous max log-prob + transition + emission
                prob = (
                    V[t-1][s_prev]          #Probability of previous state
                    + log_trans[s_prev][s]  #Probability of transitioning from prev_state to current state s
                    + log_emit[s][eseq[t]]  #Probability of emitting seqeunce symbol based on current state s
                )
                candidates.append((prob, s_prev))

            #Choose candidate with highest probability
            max_prob, max_state = max(candidates, key=lambda item: item[0])

            V[t][s] = max_prob  #Save best prob for current state
            backpointer[t][s] = max_state  #Save previous state that led to this max (for backtracing later)
    #Termination step: identify state with highest probability at final time step
    last_state = max(V[-1], key=V[-1].get)  #Determine the state with the highest prob at the last symbol in the sequence
    best_prob = V[-1][last_state]  #get the probability for the determined last state

    #Traceback: reconstruct the most likely path using the backpointer table
    best_path = [last_state]  # Start with the final best state
    for t in range(n - 1, 0, -1): #travel the sequence backwards
        best_path.insert(0, backpointer[t][best_path[0]])  #Insert the previous state at the beginning
                                                           #best_path[0] will always be the latest state, because evey new item is added at the begining of the list

    return ''.join(best_path), math.exp(best_prob)  #Return full path and true probability (convert log back to normal)



def parameter_estimation(eseq, path):
    """Estimate HMM transition and emission probabilities from a known
    emission sequence and its corresponding hidden state path.

    Parameters:
        eseq (str):   Emission sequence
        path (str):   Hidden state path

    Returns:
        tp (dict):    Transition probabilities
        ep (dict):    Emission probabilities
    """
    #Identify all states and emission symbols
    states = sorted(set(path))
    symbols = sorted(set(eseq))

    #Initialize count tables to zero
    tp_counts   = {s1: {s2: 0 for s2 in states} for s1 in states}
    emit_counts = {s: {e: 0 for e in symbols} for s in states}

    #Count transitions along the path
    for i in range(len(path) - 1):
        s_from = path[i]
        s_to   = path[i + 1]
        tp_counts[s_from][s_to] += 1

    #Count emissions for each state
    for s, e in zip(path, eseq):
        emit_counts[s][e] += 1

    #Normalize counts to probabilities
    tp = {}
    for s_from, dests in tp_counts.items():
        total = sum(dests.values())
        tp[s_from] = {}
        for s_to, cnt in dests.items():
            tp[s_from][s_to] = cnt / total if total > 0 else 0.0

    ep = {}
    for s, emits in emit_counts.items():
        total = sum(emits.values())
        ep[s] = {}
        for e, cnt in emits.items():
            ep[s][e] = cnt / total if total > 0 else 0.0

    return tp, ep

def forward(eseq, p_start, p_trans, p_emit):
    """Implements the Forward algorithm to compute the total observation likelihood P(x).

    Parameters:
        eseq (str): Emission sequence
        p_start (dict): Starting probabilities for each state
        p_trans (dict): Transition probabilities between states
        p_emit (dict): Emission probabilities for each state and observation

    Returns:
        prob (float): Total likelihood of the emission sequence
        F    (list of dict): Forward table
    """
    states = list(p_start.keys())  #List of all possible hidden states
    n = len(eseq)                  #Length of the emission sequence
    all_symbols = list({sym for emits in p_emit.values() for sym in emits})  #All possible emission symbols
    
    #Initialize forward table: F[t][s] = forward probability up to time t ending in state s
    F = [{} for _ in range(n)]

    #Initialization step (t = 0)
    #F[0][s] = P(start in s) * P(emit first symbol | s)
    for s in states:
        F[0][s] = p_start[s] * p_emit[s][eseq[0]]

    #Recursion step
    for t in range(1, n):
        for s in states:
            total = 0.0  #accumulate probability from all possible previous states
            for s_prev in states:
                #Sum of probabilities of being in t-1 states and current state
                total += F[t-1][s_prev] * p_trans[s_prev][s]
            #multiply by emission of eseq[t]
            F[t][s] = total * p_emit[s][eseq[t]]

    #Termination step
    #P(x) = sum of forward probabilities at final time step
    prob = sum(F[-1][s] for s in states)

    return prob, F



def backward(eseq, p_start, p_trans, p_emit):
    """Implements the Backward algorithm to compute the total observation likelihood P(x)
    and the backward probabilities.

    Parameters:
        eseq (str): Emission sequence
        p_start (dict): Starting probabilities for each state
        p_trans (dict): Transition probabilities between states
        p_emit (dict): Emission probabilities for each state and observation

    Returns:
        prob (float): Total likelihood of the emission sequence
        B    (list of dict): Backward table
    """
    states = list(p_start.keys())            #List of hidden states ['F', 'B']
    n = len(eseq)                            #Length of the emission sequence
    all_symbols = list({sym for emits in p_emit.values() for sym in emits})  #All possible emission symbols
    
    #Initialize backward table: B[t][s] = backward probability from time t in state s
    B = [{} for _ in range(n)]

    #Initialization step (t = n-1)
    #B[n-1][s] = 1 for all states (no future observations)
    for s in states:
        B[n-1][s] = 1.0

    #Recursion step (t = n-2 down to 0)
    #B[t][s] = sum over next states of:
    #P(s -> s_next) * P(emit x[t+1] | s_next) * B[t+1][s_next]
    for t in range(n-2, -1, -1):
        for s in states:
            total = 0.0  #accumulate probability contributions
            for s_next in states:
                total += (
                    p_trans[s][s_next]               #Probability of transitioning to s_next
                    * p_emit[s_next][eseq[t+1]]      #Emission probability at next time
                    * B[t+1][s_next]                 #Backward prob from t+1 in s_next
                )
            B[t][s] = total  #store the summed contributions

    # Termination step:
    #P(x) = sum over states of:
    #P(start in s) * P(emit x[0] | s) * B[0][s]
    prob = sum(
        p_start[s] * p_emit[s][eseq[0]] * B[0][s]
        for s in states
    )

    return prob, B

def forward_backward(eseq, p_start, p_trans, p_emit):
    """Combines Forward and Backward to compute posterior state probabilities

    Parameters:
        eseq (str): Emission sequence
        p_start (dict): Starting probabilities for each state
        p_trans (dict): Transition probabilities between states
        p_emit (dict): Emission probabilities for each state and observation

    Returns:
        gamma (list of dict)
    """
    #Run forward to get P(x) and forward table F
    prob_fwd, F = forward(eseq, p_start, p_trans, p_emit)
    #Run backward to get P(x) and backward table B
    prob_bwd, B = backward(eseq, p_start, p_trans, p_emit)
    # (prob_fwd and prob_bwd should be equal, up to numerical noise)

    states = list(p_start.keys())    #all hidden states
    n = len(eseq)                    #length of the sequence

    #Compute posterior gamma
    gamma = [{} for _ in range(n)]
    for t in range(n):
        for s in states:
            gamma[t][s] = (F[t][s] * B[t][s]) / prob_fwd

    return gamma

def profileHMM_c(param = None):
    # Returns solution from a dummy example to explain the 
    # format of return values.
    return profileHMM_syntax_c()
