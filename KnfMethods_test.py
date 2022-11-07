import unittest
import KnfMethods
from KnfMethods import *

class KnfMethodsUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.knf1 = []
        self.knf2 = [[(True, "a"), (True, "b"), (False, "b")], [(True, "a"), (True, "b"), (False, "b")]]
        self.knf3 = [[(True, "a"), (True, "b"), (False, "b")], [(True, "a"), (True, "b"), (False, "b")], [(True, "a"), (True, "b"), (False, "b")]]
        self.knf4 = [[(True, "a"), (True, "b"), (False, "b")], [(False, "d")], [(True, "a"), (True, "b"), (False, "b")]]

        return super().setUp()

    def test_subsumAndRemoveDuplicatesFromKNF(self):
        #test duplicate-removal
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF(self.knf1), [])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF(self.knf2), [[(True, "a"), (True, "b"), (False, "b")]])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF(self.knf3), [[(True, "a"), (True, "b"), (False, "b")]])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF(self.knf4), [[(False, "d")], [(True, "a"), (True, "b"), (False, "b")]])

        #test subsum
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF(self.knf1), [])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF( [[(True, "a"), (True, "b"), (False, "b")]]), [[(True, "a"), (True, "b"), (False, "b")]])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF([[(True, "a"), (False, "a"), (True, "a")], [(True, "a")]]), [[(True, "a")]])
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF([[(True, "a"), (False, "b")], [(False, "a"), (True, "b")]]), [[(True, "a"), (False, "b")], [(False, "a"), (True, "b")]]) 

        #test both in 
        self.assertListEqual(subsumAndRemoveDuplicatesFromKNF([[(True, "a"), (True, "b"), (False, "b")], [(True, "a"), (True, "b"), (False, "b")], [(True, "a"), (False, "b")]]), [[(True, "a"), (False, "b")]])
    
    def test_makeUnitResolutionWithinKNF(self):
        self.assertListEqual(makeUnitResolutionWithinKNF([]), [])
        self.assertListEqual(makeUnitResolutionWithinKNF([[(True, "a"), (False, "b")], [(True, "c"), (False, "a")]]), [[(True, "a"), (False, "b")], [(True, "c"), (False, "a")]])
        self.assertListEqual(makeUnitResolutionWithinKNF([[(True, "a"), (False, "b")], [(True, "c"), (False, "a")], [(True, "a")]]), [[(True, "c")], [(True, "a")]])
        self.assertListEqual(makeUnitResolutionWithinKNF([[(True, "a")], [(True, "a"), (False, "b")], [(True, "c"), (False, "a")], [(True, "a")]]), [[(True, "a")], [(True, "c")], [(True, "a")]])

        test = [
            [(True, "a")],
            [(True, "a"), (False, "b")],
            [(False, "a"), (True, "c"), (False, "d")],
            [(False, "a"), (False, "c")]
        ]
        self.assertListEqual(makeUnitResolutionWithinKNF(test), [[(True, 'a')], [(False, 'd')], [(False, 'c')]])

    def test_minimzeKNF(self):
        test = [
            [(False, "a"), (False, "b"), (False, "c"), (False, "d")],
            [(False, "a"), (False, "b"), (False, "c"), (False, "d"), (False, "e")],
            [(False, "a"), (False, "b"), (False, "c"), (False, "d")],
            [(False, "a"), (False, "b"), (False, "c"), (True, "d")],
            [(False, "a"), (False, "b"), (True, "c"), (False, "d")],
            [(False, "a"), (False, "b"), (True, "c"), (True, "d")],
            
            [(False, "a"), (True, "b"), (False, "c"), (False, "d")],
            [(False, "a"), (False, "a"), (True, "b"), (False, "c"), (True, "d")],
            [(False, "a"), (True, "b"), (True, "c"), (False, "d")],
            
            [(True, "a"), (False, "b"), (False, "c"), (False, "d")],
            [(False, "a"), (False, "b"), (False, "c"), (False, "d")],
            [(True, "a"), (False, "b"), (False, "c"), (True, "d")],
            [(True, "a"), (False, "b"), (True, "c"), (False, "d"), (False, "d")],
            [(True, "b"), (False, "b"), (False, "b")],
            
            [(True, "a"), (True, "b"), (False, "c"), (False, "d")],
            [(True, "a"), (True, "b"), (True, "c"), (True, "d")]
        ]

        tmp = minimzeKNF(test)

        self.assertListEqual(minimzeKNF([]), [])
        self.assertEqual(len(tmp), 7)
        self.assertTrue([(False, 'a'), (False, 'b')] in tmp)
        self.assertTrue([(False, 'a'), (False, 'c')] in tmp)
        self.assertTrue([(False, 'a'), (False, 'd')] in tmp)
        self.assertTrue([(False, 'b'), (False, 'c')] in tmp)
        self.assertTrue([(False, 'b'), (False, 'd')] in tmp)
        self.assertTrue([(False, 'c'), (False, 'd')] in tmp)
        self.assertTrue([(True, 'a'), (True, 'b'), (True, 'c'), (True, 'd')] in tmp)

    def tearDown(self) -> None:
        del self.knf1
        del self.knf2
        del self.knf3
        del self.knf4
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()