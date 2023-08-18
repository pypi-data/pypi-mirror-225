'''
NAME: Mihir Rao
DATE: 17th August, 2023
'''

# Imports
import numpy as np

# Class
class Complexity():

    def __init__(self, 
                 weight_threshold : float = 0.01, 
                 absolutize_and_normalize : bool = True,
                 return_num_of_weights : bool = False) -> None:
        '''
        Constructor for the Complexity class.
        '''
        self._weight_threshold = weight_threshold
        self._absolutize_and_normalize = absolutize_and_normalize
        self._return_num_of_weights = return_num_of_weights

    def __absolutizeExplanation(self,
                                exp : np.array) -> np.array:
        '''
        Absolutizes the explanation array.
        '''
        return np.abs(exp)

    def __normalizeExplanation(self,
                               exp : np.array) -> np.array:
        '''
        Normalizes the explanation array to sum to 1.
        '''
        # Compute the sum of the explanation array
        exp_sum = np.sum(exp)
        # Check if the sum is 0 and raise an error if so
        if exp_sum == 0:
            raise ZeroDivisionError('Explanation sum is 0. Cannot normalize.')
        else:
            exp = exp / exp_sum
        # Return the normalized explanation
        return exp
    
    def compute(self,
                exp : np.array) -> np.array:
        '''
        Computes the complexity of the explanation.
        '''
        # Check if explanation is to be absolutized and normalized
        if self._absolutize_and_normalize:
            exp = self.__absolutizeExplanation(exp)
            exp = self.__normalizeExplanation(exp)
        # Compute the complexity
        if self._return_num_of_weights:
            complexity = np.sum(exp > self._weight_threshold)
        else:
            complexity = np.sum(exp > self._weight_threshold) / np.size(exp)
        # Return the complexity
        return complexity