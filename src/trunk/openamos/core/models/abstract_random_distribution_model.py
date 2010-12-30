from numpy import zeros
from numpy.random.mtrand import RandomState

class RandomDistribution(RandomState):
    def __init__(self, seed):
        RandomState.__init__(self, seed)
        self.seed = seed

    def return_normal_variables(self, location, scale, size):
        if scale == 0:
            return zeros(size) + location
        norm_vars = self.normal(loc=location, 
                                scale=scale, 
                                size=size)
        return norm_vars
        
    def return_random_variables(self, size=None):
	if size is not None:
	    rand_vars = self.random_sample(size)
	else:
	    rand_vars = self.random_sample()
        return rand_vars

    def return_half_normal_variables(self, location, scale, size):
	norm_vars = self.return_normal_variables(location, scale, size)
	half_norm_vars = abs(norm_vars)
	return half_norm_vars



import unittest


class TestRandomDistribution(unittest.TestCase):
    def setUp(self):
        pass
    def testValues(self):
        for i in range(100):
            self.dist1 = RandomDistribution(seed=1)
            self.dist2 = RandomDistribution(seed=1)
            
            
            dist1Vals = self.dist1.return_normal_variables(location=0, scale=1, size=(10000,1))
            dist2Vals = self.dist2.return_normal_variables(location=0, scale=1, size=(10000,1))
            
            pred_diff = all(dist1Vals == dist2Vals)
            if not pred_diff:
                print 'Run:%s' %(i+1)

                print dist1Vals, dist2Vals
            self.assertEquals(True, pred_diff)



if __name__ == '__main__':
    unittest.main()
