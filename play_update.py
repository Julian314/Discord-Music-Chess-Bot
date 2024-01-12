from helpers import encode_model_input
import chess

def best_move(engine,board, is_turn):
    '''RETURNS THE BEST MOVE FOR EITHER BLACK OR WHITE, DEPENDING ON 'IS_TURN' '''
    evals = {}
    moves = list(board.legal_moves)
    for move in moves:
        board.push(move)
        model_input = encode_model_input(board)
        evals[move] = engine(model_input).item()
        board.pop()
        if is_turn == chess.WHITE:
            mini = max(list(evals.values()))
        else:
            mini = min(list(evals.values()))
        #print(evals)
    for key in evals:
        if evals.get(key) == mini:
            return (key, evals.get(key))

def move(engine, board, color):
    moves = list(board.legal_moves)
    evals = {}
    for move in moves:
        board.push(move)
        black_hole, wert = best_move(engine, board, not color)
        evals[move] = wert
        board.pop()
    if color == chess.WHITE :
        mini = max(evals.values())
    else:
        mini = min(evals.values())
    for key in evals:
        if evals.get(key) == mini:
            return(key, evals.get(key))

def eval(board, engine):
    model_input = encode_model_input(board)
    return engine(model_input)
            