def two_sum(sequence, t):
    '''
    Args:
        sequence: the given sequence as a list
        t: the given target number, which should be the sum of two selected integers.

    Returns:
        res: A list of tuple. And each tuple would be the idx of two selected integers.
    Example:
        input:
        1 2 3 4
        5
        output:
        0 3
        1 2

    '''
    res = []
    ##############
    #  Please write your own code in the given space.
    #############




    #############
    i = 0
    j = len(sequence) - 1
    while i < j:
        if sequence[i]+sequence[j] < t:
            i = i + 1
        elif sequence[i]+sequence[j] > t:
            j = j - 1
        else:
            i_num = 1
            j_num = 1
            while sequence[i] == sequence[i+i_num]:
                i_num = i_num + 1
            while sequence[j] == sequence[j-j_num]:
                j_num = j_num - 1

            for m in range(i_num):
                for n in range(j_num):
                    res.append((i+m,j+n))
            i = i + i_num
            j = j - j_num

    return res

if __name__ == '__main__':
    for i in range(3):
        print(f'case {i}')
        with open(f'./test_cases/problem1/{i+1}.txt', 'r') as f:
            seq, tar = f.read().strip().split('\n')
            seq = [*map(int, seq.split(' '))]
            tar = int(tar)

        for item in two_sum(seq, tar):
            print('%d %d' % item)

