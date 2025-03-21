direction_offsets = [ 8, -8, 1, -1, 7, -7, 9, -9 ]

def PrecomputeMoveData():
  num_squares_to_edge = {}
  
  for file in range(8):
    for rank in range(8):
      square = rank * 8 + file
      
      numSquaresNorth = 7 - rank
      numSquaresSouth = rank
      numSquaresEast = 7 - file
      numSquaresWest = file
      
      num_squares_to_edge[square] = [
        numSquaresNorth,
        numSquaresSouth,
        numSquaresEast,
        numSquaresWest,
        min(numSquaresNorth, numSquaresWest),
        min(numSquaresSouth, numSquaresEast),
        min(numSquaresNorth, numSquaresEast),
        min(numSquaresSouth, numSquaresWest)
      ]
  
  return num_squares_to_edge