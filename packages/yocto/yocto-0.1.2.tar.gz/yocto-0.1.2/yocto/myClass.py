import numpy as np
class Multiplication:
    """
    Classe brouillon pour essayer de faire fonctionner le pipeline
    """
    def __init__(self, multiplier = 1):
        self.multiplier = multiplier

    def multiply(self,number):
        """
        Multiplies the given number by the multiplier associated with the instance.

        :param number: The number to be multiplied.
        :return: The result of multiplying the number by the instance's multiplier.
        """
        return np.dot(self.multiplier, number)

if __name__ == "__main__":
    pass
