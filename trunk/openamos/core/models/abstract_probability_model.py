from numpy import ndarray, array, random, ma, all, zeros, ones
from openamos.core.errors import ProbabilityError, DataError
from openamos.core.data_array import DataArray

class AbstractProbabilityModel(object):
    def __init__(self, probabilities, seed=1):
        if not isinstance(probabilities, DataArray):
            raise DataError, 'probability input is not a valid DataArray object'
        self.probabilities = ma.array(probabilities.data)
        self.seed = seed
        random.seed(self.seed)
        self.check()
        self.choices = probabilities.varnames


    def check(self):
        self.check_probabilities()
        self.check_sum()

    def check_probabilities(self):
        if not isinstance(self.probabilities, ndarray):
            raise ProbabilityError, 'probability input is not a valid array object'

    def check_sum(self):
        self.num_agents = self.probabilities.shape[0]
        self.num_choices = self.probabilities.shape[-1]

        cumsum_across_rows = self.probabilities.cumsum(-1)[:,-1]
        diff_from_unity = abs(cumsum_across_rows - 1)
        if not all(diff_from_unity < 1e-6):
            raise ProbabilityError, 'probability values do not add up to one across rows'

    def generate_random_numbers(self):
        return random.random(self.num_agents)

    def cumprob(self):
        return self.probabilities.cumsum(-1)

    def selected_choice(self):
        choice = zeros(self.num_agents)
        random_numbers = self.generate_random_numbers()

        print random_numbers

        self.prob_cumsum = self.cumprob().filled(-1)

        for i in range(self.num_choices):
            # Indicator for the zero cells in the choice array
            indicator_zero_cells = ones(self.num_agents)
            zero_indices = choice == 0
            indicator_zero_cells[~zero_indices] = ma.masked

            # Indicator for the cells where the random number is less than the probability
            indicator_less_cells = ones(self.num_agents)
            less_indices = random_numbers < self.prob_cumsum[:,i]
            indicator_less_cells[~less_indices] = ma.masked


            indicator_less_zero_cells = indicator_zero_cells + indicator_less_cells
            
            indicator_less_zero_cells = indicator_less_zero_cells == 2

            choice[indicator_less_zero_cells] = i + 1

        choice.shape = (self.num_agents, 1)

        alt_text = []
        for i in choice:
            alt_text.append(self.choices[int(i[0])-1])
        alt_text = array(alt_text)
        alt_text.shape = (self.num_agents, 1)

        return alt_text
        #return DataArray(choice, ['selected choice']), alt_text

import unittest
from numpy import array, zeros, dtype, float32

class TestBadInputAbstractProbabilityModel(unittest.TestCase):
    def setUp(self):
        self.probabilities1 = [(0.5,0.19, 0.31), (0.1, 0.2, 0.72)]
        self.probabilities2 = DataArray(array([[0.5,0.29, 0.31], [0.1, 0.2, 0.7]]), 
                                        ['ch1', 'ch2', 'ch3'])
        self.probabilities3 = DataArray(array(self.probabilities1), 
                                        ['ch1', 'ch2', 'ch3'])
        
    def testprobabilitylist(self):
        self.assertRaises(DataError, AbstractProbabilityModel, self.probabilities1)

    def testvaluessum(self):
        self.assertRaises(ProbabilityError, AbstractProbabilityModel, self.probabilities3)


class TestAbstractProbabilityModel(unittest.TestCase):
    def setUp(self):

        probabilities = array([[0.5,0.19, 0.31], [0.1, 0.2, 0.7]])
        choices = ['ch1', 'ch2', 'ch3']
        self.model = AbstractProbabilityModel(DataArray(probabilities, choices))


    def testrandomvalues(self):
        random_array = array([0.417022, 0.72032449])
        random_numbers_frommodel = self.model.generate_random_numbers()
        diff_numbers = random_array - random_numbers_frommodel
        sum_diff_numbers = diff_numbers.sum()
        if sum_diff_numbers < 1e-6:
            sum_diff_numbers = 0
        self.assertEqual(0, sum_diff_numbers)


    def testcalculatecumprob(self):
        cumprob_array = array([[0.5,0.69, 1.00], [0.1, 0.3, 1.0]])
        cumprob_array_frommodel = self.model.cumprob()
        diff_cumprob = cumprob_array - cumprob_array_frommodel
        diff_cumprob_sum = diff_cumprob.sum()
        if diff_cumprob_sum < 1e-6:
            diff_cumprob_sum = 0
        self.assertEqual(0, diff_cumprob_sum)
        

    def testchoicecolumns(self):
        choice_array = array([['ch1'], ['ch3']])
        choice_array_frommodel = self.model.selected_choice()
        diff_choice = all(choice_array == choice_array_frommodel)
        self.assertEqual(True, diff_choice)
        


if __name__ == '__main__':
    unittest.main()
