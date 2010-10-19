from scipy.stats import norm
from numpy import random
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.errors import ErrorSpecificationError
from openamos.core.models.abstract_random_distribution_model import RandomDistribution

class StocFronRegressionModel(AbstractRegressionModel):
    """
    This is teh base class for stochastic frontier regression models in OpenAMOS.
    
    Inputs:
    specification - Specification object
    error_specification - StochasticRegErrorSpecification object
    """
    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(self, specification, error_specification)
        
        if not isinstance(error_specification, StochasticRegErrorSpecification):
            raise ErrorSpecificationError, """incorrect error specification; it """\
                """should be StochasticRegErrroSpecification object"""

    def calc_errorcomponent(self, variance_norm, variance_halfnorm, 
                            vertex, size, seed):
        """
        The method returns the contribution of the error component in the 
        calculation of the predicted value for the different choices.
        
        Inputs:
        variance_norm - numeric value (variance of the normal portion of error)
        variance_halfnorm - numeric value (variance of the half normal portion of
                                        error)
        vertex - string (the vertext to predict -- start/end)
        size - numeric value (number of rows)

        random.seed(seed=seed)
        err_norm = norm.rvs(loc=0, scale=variance_norm**0.5, size=size)
        err = norm.rvs(size=size)
        f = open('test_res', 'a')
        f.write('stochastic - %s\n' %seed)
        f.write(str(list(err[:3,:])))
        f.write('\n')
        f.close()
        #raw_input()
        f = open('test_res', a)
        f.write('stochastic')x
        f.write(str(list(err_norm[:3,:])))
        f.write('\n')
        f.close()
        random.seed(seed=seed)
        #err_halfnorm = halfnorm.rvs(scale=variance_halfnorm**0.5, size=size)

        """
        dist = RandomDistribution(seed=seed)
        #randState = RandomState(seed)
        #dist = randState.normal(loc=0, scale=variance_norm**0.5, size=size, seed
        err_norm = dist.return_normal_variables(location=0, scale=variance_norm**0.5, size=size)

        if vertex == 'start':
            return err_norm

        if vertex == 'end':
            return err_norm

    def calc_predvalue(self, data, seed=1):
        """
        The method returns the predicted value for the different choices in the
        specification input.
        
        Inputs:
        data - DataArray object
        """
        if seed == None:
            raise Exception, "linear"

        expected_value = self.calc_expected_value(data)
        variance_norm = self.error_specification.variance[0,0]
        variance_halfnorm = self.error_specification.variance[1,1]
        vertex = self.error_specification.vertex
        threshold = self.error_specification.threshold
        size = (data.rows, 1)

        err = self.calc_errorcomponent(variance_norm, variance_halfnorm, 
                                       vertex, size, seed)
        
        pred_value = expected_value.data + err

        if vertex == 'start':
            predValue_lessThresholdInd = pred_value < threshold
            print '\t\tPred value is less than START threshold for - %d cases ' \
                % predValue_lessThresholdInd.sum()
            pred_value[predValue_lessThresholdInd] = threshold


        if vertex == 'end':
            predValue_moreThresholdInd = pred_value > threshold
            print '\t\tPred value is greater than END threshold for - %d cases ' \
                % predValue_moreThresholdInd.sum()
            pred_value[predValue_moreThresholdInd] = threshold

        _sum = ((pred_value) < 0).sum()
        if _sum > 0:
            print '\t\t -- SUM LESS THAN ZERO --', _sum


        return DataArray(pred_value, self.specification.choices)

    
import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import StochasticRegErrorSpecification

class TestStocFronRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['Frontier']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])       
        variance = array([[1., 0], [0, 1.1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = StochasticRegErrorSpecification(variance, 'start')


    def testvalues(self):
        model = StocFronRegressionModel(self.specification, 
                                        self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        expected_act = self.data.calculate_equation(
                                                    self.specification.coefficients[0])
        expected_act.shape = (4,1)
        variance = self.errorspecification.variance

        dist = RandomDistribution(seed=1)
        err_norm = dist.return_normal_variables(location=0, scale=variance[0,0]**0.5, size=(4,1))
        
        pred_act = (expected_act + err_norm)
        
        pred_diff = all(pred_value.data == pred_act)
        self.assertEquals(True, pred_diff)
        
if __name__ == '__main__':
    unittest.main()
