from chocolate import *
import unittest

class Test(unittest.TestCase):
    def test_random_int(self):
        '''tests that random_int returns a random integer between 1 and 10 inclusive'''

        result = True

        # test the type
        ran = random_int(50)
        if type(ran) != int:
            result = False

        # test the values returned
        for i in range(10):
            ran = random_int(10)
            if ran < 1 or ran > 10:
                result = False

        self.assertEqual(result, True)

    def test_generate_integer_list(self):
        '''tests that generate_integer_list returns an array of 5 bars with length between 1 and 10 inclusive'''

        result = True

        # test the type
        bars = generate_integer_list(5, 10)
        if type(bars) != list:
            result = False

        # test the values returned
        for i in range(50):
            bars = generate_integer_list(5, 10)
            if len(bars) != 5:
                result = False
            for bar in bars:
                if bar < 1 or bar > 10:
                    result = False


        self.assertEqual(result, True)

    def test_generate_input(self):
        '''tests that generate_input returns two arrays of integers between 1 and 10 inclusive of variable length between 1 and 5'''

        result = True

        max_length = 5
        max_int = 10
        iterations = 5

        # test the types
        bars, requests = generate_input(max_length, max_int)
        if type(bars) != list or type(requests) != list:
            result = False

        # test the values returned
        for i in range(iterations):
            bars, requests = generate_input(max_length, max_int)

            # test the list lengths
            if len(bars) > max_length or len(requests) > max_length:
                print(len(bars), len(requests))
                result = False

            # test the integer values
            for bar in bars:
                if bar < 1 or bar > max_int:
                    print("bar:", bar)
                    result = False
            for bar in requests:
                if bar < 1 or bar > max_int:
                    print("request:", bar)
                    result = False

            # test the relative sums
            if sum(bars) < sum(requests):
                print(sum(requests), ">", sum(bars))
                result = False

        self.assertEqual(result, True)

    def test_sort_input(self):
        '''tests that sort_input() sorts the lists'''

        result = True

        max_length = 5
        max_int = 10

        bars, requests = generate_input(max_length, max_int)
        sort_input(bars, requests)
        if not all(bars[i] <= bars[i+1] for i in range(len(bars)-1)):
            print('bars wasn\'t sorted')
            result = False
        if not all(requests[i] >= requests[i+1] for i in range(len(requests)-1)):
            print('requests wasn\'t sorted')
            result = False

        self.assertEqual(result, True)

    def test_remove_simple_requests(self):
        '''tests that remove_simple_requests() removes any integers that appear in both lists'''

        result = True

        max_length = 5
        max_int = 10
        iterations = 10

        for i in range(iterations):
            bars, requests = generate_input(max_length, max_int)
            final_bars = []
            sort_input(bars, requests)
            remove_simple_requests(bars, requests, final_bars)

            for bar in bars:
                if bar in requests:
                    print(bars, requests)
                    result = False

        self.assertEqual(result, True)

    def test_remove_large_requests(self):
        '''tests that remove_large_requests() removes any requests that are larger than the bars available'''

        result = True

        max_length = 5
        max_int = 10
        iterations = 500
        verbose = False

        for i in range(iterations):
            bars, requests = generate_input(max_length, max_int)
            final_bars = []
            sort_input(bars, requests)

            check = bars[-1] < requests[0] and (requests[0] - bars[-1]) in bars
            if verbose and check:
                print('start -', bars, requests)

            remove_large_requests(bars, requests, final_bars)

            if verbose and check:
                print('large -', bars, requests, "\n")

            if requests != [] and bars[-1] < requests[0]:
                result = False

        self.assertEqual(result, True)

    def test_remove_pairs_of_bars(self):
        '''tests that remove_pairs_of_bars() removes all pairs of bars that perfectly fill a request - currently relies on visual inspection'''

        result = True

        max_length = 5
        max_int = 10
        iterations = 100
        verbose = False

        for i in range(iterations):
            if verbose:
                print("\n",i)

            bars, requests = generate_input(max_length, max_int)
            final_bars = []
            if verbose:
                print('start   -', bars, requests)

            sort_input(bars, requests)
            if verbose:
                print('sorted  -', bars, requests)

            remove_simple_requests(bars, requests, final_bars)
            if verbose:
                print('simple  -', bars, requests)

            remove_pairs_of_bars(bars, requests, final_bars)
            if verbose:
                print('paired  -', bars, requests)

        self.assertEqual(result, True)

    def test_remove_pairs_of_requests(self):
        '''tests that remove_pairs_of_requests() removes all pairs of requests that fit perfectly in a bar - currently relies on visual inspection'''

        result = True

        max_length = 5
        max_int = 10
        iterations = 100
        verbose = False

        for i in range(iterations):
            if verbose:
                print("\n",i)

            bars, requests = generate_input(max_length, max_int)
            final_bars = []
            if verbose:
                print('start   -', bars, requests)

            sort_input(bars, requests)
            if verbose:
                print('sorted  -', bars, requests)

            remove_simple_requests(bars, requests, final_bars)
            if verbose:
                print('simple  -', bars, requests)

            cuts = remove_pairs_of_requests(bars, requests, final_bars)
            if verbose:
                print('paired  -', bars, requests, '-', cuts)

        self.assertEqual(result, True)

    def test_simple_bin_packing(self):
        '''tests that simple_bin_packing() counts the number of cuts required to fill all requests using a simple bin packing algoithm - currently relies on visual inspection'''

        result = True

        max_length = 10
        max_int = 10
        iterations = 50
        verbose = False

        for i in range(iterations):
            if verbose:
                print(i)

            bars, requests = generate_input(max_length, max_int)
            final_bars = []
            if verbose:
                print('start   -', bars, requests)

            sort_input(bars, requests)
            if verbose:
                print('sorted  -', bars, requests)

            remove_simple_requests(bars, requests, final_bars)
            if verbose:
                print('simple  -', bars, requests)

            cuts = simple_bin_packing(bars, requests, final_bars, verbose)
            if verbose:
                print('packed  -', bars, requests, "-", cuts, "\n")

        self.assertEqual(result, True)

    def test_find_minimum_cuts(self):
        '''tests that find_minimum_cuts() counts the minimum number of cuts required to fill all requests - currently relies on visual inspection'''
        # to do
        # - check that the sum of the bars at the end = at the beginning
        # - check that the number of bars at the end >= at the beginning

        result = True

        max_length = 10
        max_int = 10
        iterations = 50
        verbose = True

        for i in range(iterations):
            if verbose:
                print(i)

            bars, requests = generate_input(max_length, max_int)
            if verbose:
                print('start  -', bars, requests)

            cuts, final_bars = find_minimum_cuts(bars, requests, verbose)
            if verbose:
                print('filled requests -', final_bars, "\n")

        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
