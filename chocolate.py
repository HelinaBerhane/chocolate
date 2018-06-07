import random

def random_int(max):
    '''returns a random integer between 1 and max inclusive'''
    return random.randint(1, max)

def generate_integer_list(num_bars, max_size):
    '''returns an array of integers between 1 and max_size inclusive with length num_bars'''
    bars = []
    for i in range(num_bars):
        bars.append(random_int(max_size))
    return bars

def generate_input(max_num_bars, max_bar_size):
    '''returns two arrays of integers between 1 and max_bar_size inclusive with length between 1 and max_num_bars'''

    # generate the bars
    num_bars = random_int(max_num_bars)
    num_requests = random_int(max_num_bars)

    bars = generate_integer_list(num_bars, max_bar_size)
    requests = generate_integer_list(num_requests, max_bar_size)

    # make sure that there are more bars than requests
    while sum(requests) > sum(bars):
        return generate_input(max_num_bars, max_bar_size)

    return bars, requests

def sort_input(bars, requests):
    bars.sort()
    requests.sort(reverse = True)

def remove_simple_requests(bars, requests, final_bars):
    '''removes any request that can be completely fufilled by a bar, returns false if there are no requests left'''
    finished = False
    while not finished and requests != []:
        for i, bar in enumerate(bars):
            if bar in requests:
                del bars[i]
                del requests[requests.index(bar)]
                final_bars.append([bar])
                break
        else:
            finished = True

def remove_large_requests(bars, requests, final_bars):
    '''reduces any request larger than the largest bar'''

    while requests != [] and requests[0] > bars[-1]:

        bars_allocated = []

        # while the remaining request is larger than the largest bar
        while requests[0] > bars[-1]:

            # allocate the bar to the request
            requests[0] -= bars[-1]
            bars_allocated.append(bars[-1])
            del bars[-1]

        # if the remaining request fits in a bar
        if requests[0] in bars:

            # allocate the bar to the request
            bars_allocated.append(requests[0])
            del bars[bars.index(requests[0])]
            del requests[0]
            if requests == []:
                break

        # if the remaining request does not fit in a bar
        else:

            # allocate it from part of the largest bar
            bars[-1] -= requests[0]
            bars_allocated.append(requests[0])
            del requests[0]

        # when finished, re-sort the bars and store the result
        if bars_allocated != []:
            final_bars.append(bars_allocated)
        sort_input(bars, requests)

    if requests == []:
        return True

def remove_pairs_of_bars(bars, requests, final_bars):
    '''resolves any pair of bars that perfectly resolve a request'''
    finished = False
    while requests != [] and not finished:
        for i, a in enumerate(bars):
            for j, b in enumerate(bars):
                if i != j:
                    sum = (a + b)
                    if sum in requests:
                        final_bars.append([bars[j], bars[i]])
                        del requests[requests.index(sum)]
                        del bars[j]
                        del bars[i]
                        break
            else:
                continue
            break
        else:
            finished = True
    # ideally, this wouldn't be duplicated in remove_pairs_of_requests()

def remove_pairs_of_requests(bars, requests, final_bars):
    '''resolves any pair of requests that fit perfectly in a bar'''
    cuts = 0
    finished = False
    while requests != [] and not finished:
        for i, a in enumerate(requests):
            for j, b in enumerate(requests):
                if i != j:
                    sum = (a + b)
                    if sum in bars:
                        cuts += 1
                        final_bars.append([requests[j]])
                        final_bars.append([requests[i]])
                        del bars[bars.index(sum)]
                        del requests[j]
                        del requests[i]
                        break
            else:
                continue
            break
        else:
            finished = True
    else:
        return cuts

def simple_bin_packing(bars, requests, final_bars, verbose = False):
    '''resolves all remaining requests with the smallest bar they fit in'''
    cuts = 0
    test_count = 0

    while requests != []:
        remove_simple_requests(bars, requests, final_bars)
        if remove_large_requests(bars, requests, final_bars):
            continue

        bars_allocated = []
        for i, bar in enumerate(bars):
            if bar > requests[0]:

                cuts += 1
                bars[i] -= requests[0]
                bars_allocated.append(requests[0])
                del requests[0]

                if bars[i] in requests:
                    bars_allocated.append(bars[i])
                    del requests[requests.index(bars[i])]
                    del bars[i]
                else:
                    bars.sort()
                break

        if bars_allocated != []:
            final_bars.append(bars_allocated)

        if verbose:
            test_count += 1
            if test_count < 50:
                print('packing -', bars, requests, '-', cuts)
            else:
                return cuts

    return cuts

def find_minimum_cuts(bars, requests, verbose = False):

    final_bars = []
    sort_input(bars, requests)
    if verbose:
        print('sorted -', bars, requests)

    remove_simple_requests(bars, requests, final_bars)
    if verbose:
        print('simple  -', bars, requests)

    cuts = 0
    if len(bars) < len(requests):
        remove_pairs_of_bars(bars, requests, final_bars)
        cuts = remove_pairs_of_requests(bars, requests, final_bars)
    else:
        cuts = remove_pairs_of_requests(bars, requests, final_bars)
        remove_pairs_of_bars(bars, requests, final_bars)
    if verbose:
        print('paired  -', bars, requests)

    cuts += simple_bin_packing(bars, requests, final_bars)
    if verbose:
        if cuts == 1:
            print('packed  -', bars, requests, "-", cuts, 'cut')
        else:
            print('packed  -', bars, requests, "-", cuts, 'cuts')

    final_bars.sort(key=lambda elem: sum(elem), reverse=True)

    return cuts, final_bars


# future improvements
# - implement classes
# - deal with more edge cases (i.e. running out of bars before filling every request)
# - make output more meaningful / consistent
# - keep track of the distribution of bars as well as how requests are filled
