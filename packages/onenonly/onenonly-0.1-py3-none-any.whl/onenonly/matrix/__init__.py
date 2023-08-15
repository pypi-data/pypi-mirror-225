from onenonly import const
from onenonly import List

def isMatrix(matrix:list[list]):
    if not isinstance(matrix,list):
        return const.false
    num_columns = len(matrix[0]) if matrix else const.NULL
    for row in matrix:
        if not isinstance(row, list) or len(row) != num_columns:
            return const.false
    return const.true

def toMatrix(array:list[list],dim:tuple):
    array = List.flatten(array)
    rows,cols = dim
    if rows*cols != len(array):
        raise ValueError("can't rehape the matrix to the specified dimensions!")
    matrix = []
    index = 0
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(array[index])
            index += 1
        matrix.append(row)
    return matrix

def reshape(matrix:list[list],dim:tuple):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    rows,cols = dim
    if len(matrix)*len(matrix[0]) != rows*cols:
        raise ValueError("can't reshape the matrix to the specified dimensions!")
    newMatrix = []
    newRow = []
    count = 0
    for row in matrix:
        for value in row:
            newRow.append(value)
            count += 1
            if count == cols:
                newMatrix.append(newRow)
                newRow = []
                count = 0
    return newMatrix
    
def isSquare(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    if len(matrix) != len(matrix[0]):
        return const.false
    return const.true
    
def dim(matrix:list[list]):
    if not isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
    return len(matrix)

def shape(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    return (len(matrix),len(matrix[0]))
    
def size(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    return len(matrix)*len(matrix[0])
    
def info(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    isSquare = False
    if isSquare(matrix):
        isSquare = True
    return (dim(matrix),shape(matrix),size(matrix),isSquare)
    
def zeros(shape:tuple):
    rows,cols = shape
    return [[0]*cols for _ in range(rows)]

def ones(shape:tuple):
    rows,cols = shape
    return [[1]*cols for _ in range(rows)]
    
def dummy(shape:tuple,value:int|float = 0):
    rows,cols = shape
    return [[value]*cols for _ in range(rows)]

def add(*matrices:list[list]):
    for matrix in matrices:
        if not isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
    if len(set(len(matrix) for matrix in matrices)) != 1 or len(set(len(row) for matrix in matrices for row in matrix)) != 1:
        raise ValueError("All matrices must have the same dimensions for addition.")
    result = [[sum(matrix[i][j] for matrix in matrices) for j in range(len(matrices[0][i]))] for i in range(len(matrices[0]))]
    return result
    
def scalarAdd(matrix:list[list],scalar:int|float=0):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    result = [[matrix[i][j]+scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
    return result
    
def sub(*matrices:list[list]):
    for matrix in matrices:
        if not isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
    if len(set(len(matrix) for matrix in matrices)) != 1 or len(set(len(row) for matrix in matrices for row in matrix)) != 1:
        raise ValueError("All matrices must have the same dimensions for subtraction.")
    result = [[matrices[0][i][j]-sum(matrix[i][j] for matrix in matrices[1:]) for j in range(len(matrices[0][i]))] for i in range(len(matrices[0]))]
    return result

def scalarSub(matrix:list[list],scalar:int|float=0):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    result = [[matrix[i][j]-scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
    return result

def product(*matrices:list[list]):
    result = matrices[0]
    for matrix in matrices[1:]:
        rowsResult = len(result)
        colsResult = len(result[0])
        rowsMatrix = len(matrix)
        colsMatrix = len(matrix[0])
        if colsResult != rowsMatrix:
            raise ValueError("Error: matrix dimensions are not compatible for multiplication!")
        newResult = [[0] * colsMatrix for _ in range(rowsResult)]
        for i in range(rowsResult):
            for j in range(colsMatrix):
                sum = 0
                for k in range(colsResult):
                    sum += result[i][k] * matrix[k][j]
                newResult[i][j] = sum
        result = newResult
    return result

def scalarProduct(matrix:list[list],scalar:int|float=1):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix!")
    result = [[matrix[i][j] * scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
    return result
    
def T(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix!")
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return result
    
def subMatrix(matrix:list[list],shape:tuple):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    row,col = shape
    return [matrix[i][:col] + matrix[i][col+1:] for i in range(len(matrix)) if i != row]
    
def det(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    res = 0
    for j in range(len(matrix[0])):
        sign = (-1) ** j
        minor = subMatrix(matrix,(0,j))
        res += sign*matrix[0][j]*det(minor)
    return res

def cofactor(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    cofactors = [[(-1) ** (i + j) * det(subMatrix(matrix,(i,j))) for j in range(len(matrix[0]))] for i in range(len(matrix))]
    return cofactors

def adjoint(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    cofactors = cofactor(matrix)
    return T(cofactors)

def inv(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: given nested list isn't in the form of matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    det = det(matrix)
    if det == 0:
        raise ValueError("Error: matrix is not invertible (non-singular)")
    adj = adjoint(matrix)
    inv = scalarProduct(adj,1/det)
    return inv
    
def traces(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    trace = 0
    for x in range(len(matrix)):
        trace += matrix[x][x]
    return trace
    
def diagonalSum(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    if not isSquare(matrix):
        raise ValueError("Error: matrix should have same number of rows and cols")
    total = 0
    for x in range(len(matrix)):
        total += matrix[x][x]
        total += matrix[len(matrix)-x-1][x]
    if len(matrix)%2 != 0:
        total -= matrix[int(len(matrix)/2)][int(len(matrix)/2)]
    return total
    
def removeCol(matrix:list[list],column:int):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    for rows in matrix:
        rows.remove(rows[column])
    return matrix
    
def removeRow(matrix:list[list],row:int):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    matrix.remove(matrix[row])
    return matrix
    
def reciprocal(matrix:list[list]):
    if not isMatrix(matrix):
        raise ValueError("Error: input should be a matrix")
    for rows in matrix:
        for x in range(len(rows)):
            rows[x] = 1/rows[x]
    return matrix
