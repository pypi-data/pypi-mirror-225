import unittest
import numpy as np
from cryoloBM_tools.virons_prior import group_by_center

class MyTestCase(unittest.TestCase):
    def test_group_by_center(self):

        centers = np.zeros(shape=(2,3))
        centers[0, 0] = 5
        centers[0, 1] = 5
        centers[0, 2] = 5

        centers[1, 0] = 20
        centers[1, 1] = 20
        centers[1, 2] = 20

        picks = np.zeros(shape=(3,3))
        picks[0, 0] = 5 - 1
        picks[0, 1] = 5 - 1
        picks[0, 2] = 5 - 1

        picks[1, 0] = 5 + 1
        picks[1, 1] = 5 + 1
        picks[1, 2] = 5 + 1

        picks[2, 0] = 20 + 1
        picks[2, 1] = 20 + 1
        picks[2, 2] = 20 + 1

        groups = group_by_center(centers=centers,picks=picks,max_distance=10)
        np.testing.assert_array_equal([0,0,1], groups)



if __name__ == '__main__':
    unittest.main()
