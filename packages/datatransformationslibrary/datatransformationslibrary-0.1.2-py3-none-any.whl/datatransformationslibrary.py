import numpy as np
from typing import Union


def transpose2d(input_matrix: list[list[float]]) -> list:
    '''
    Transposes a 2D matrix.
    
    Args:
        input_matrix (list[list[float]]): A 2D matrix to transpose.
        
    Returns:
        list: The transposed matrix.
    
    Raises:
        ValueError: If the input matrix is empty.
        ValueError: If all rows of the matrix do not have the same length.
    '''

    if not input_matrix:
        raise ValueError("Input matrix is empty.")

    if len(set(len(row) for row in input_matrix)) > 1:
        raise ValueError("All rows of the matrix must have the same length.")

    return [[row[i] for row in input_matrix] 
                    for i in range(len(input_matrix[0]))]


def window1d(
    input_array: Union[list, np.ndarray],
    size: int,
    shift: int = 1,
    stride: int = 1
) -> Union[list[list], list[np.ndarray]]:
    '''
    Generates windows of the specified size, shift, and stride from the input array.
    
    Args:
        input_array (Union[list, np.ndarray]): 1D list or numpy array to generate windows from.
        size (int): The size of each window.
        shift (int, optional): Number of positions to move the window each iteration. Defaults to 1.
        stride (int, optional): The step between consecutive elements within each window. Defaults to 1.
        
    Returns:
        Union[list[list], list[np.ndarray]]: A list of windows.
    
    Raises:
        ValueError: If input_array is not a list or 1D numpy array.
        ValueError: If input_array is not 1D.
    '''

    if not isinstance(input_array, (list, np.ndarray)):
        raise ValueError("input_array must be a list or 1D numpy array.")

    input_array = np.asarray(input_array)

    if len(input_array.shape) != 1:
        raise ValueError("input_array must be 1D.")

    windows = []
    
    for start in range(0, len(input_array) - size * stride + stride, shift):
        window = input_array[start:start+size*stride:stride]
        windows.append(window.tolist())

        
    return windows


def convolution2d(
    input_matrix: np.ndarray,
    kernel: np.ndarray,
    stride: int = 1
) -> np.ndarray:
    '''
    Performs a 2D convolution operation on the input matrix with a specified kernel.
    
    Args:
        input_matrix (np.ndarray): A 2D input matrix for convolution.
        kernel (np.ndarray): A 2D kernel for convolution.
        stride (int, optional): The step size to use when applying the kernel. Defaults to 1.
        
    Returns:
        np.ndarray: A matrix resulting from the convolution operation.
    
    Raises:
        ValueError: If stride is less than or equal to 0.
    '''

    # Validate the stride
    if stride <= 0:
        raise ValueError("Stride should be greater than 0.")
    
    
    # Get dimensions of input matrix and kernel
    i_h, i_w = input_matrix.shape
    k_h, k_w = kernel.shape

    # Check for the case where kernel is larger than the input
    if k_h > i_h or k_w > i_w:
        return np.empty((0, 0))
    
    # Calculate the dimensions of the output
    o_h = int(((i_h - k_h) / stride) + 1)
    o_w = int(((i_w - k_w) / stride) + 1)

    # Initialize the output matrix
    output = np.zeros((o_h, o_w))

    # Iterate over the input matrix
    for i in range(0, i_h - k_h + 1, stride):
        for j in range(0, i_w - k_w + 1, stride):
            # Extract the current region
            region = input_matrix[i:i+k_h, j:j+k_w]
            # Perform convolution (element-wise multiplication and sum)
            output[i//stride, j//stride] = np.sum(region * kernel)

    return output
