import os
import math
import operator


def read_genotypes(filename: str) -> list:
    """Read the genotypes from the 'filename' having header."""
    genotypes = list()

    with open(filename, 'r') as filehandle:
        # Skip header line
        filehandle.readline()

        for line in filehandle:
            first = line.split('\t')[0]
            if first == '' or first == 'wt':
                genotypes.append(('0Z',))
            else:
                genotypes.append(tuple(first.split(':')))

    return genotypes


def get_delta(genotype1: str, genotype2: str) -> str:
    """Returns difference between 'genotype1' and 'genotype2' as
       alphabetically ordered list of mutations."""
    s1 = set(genotype1)
    s2 = set(genotype2)

    # Correction for wild-type: it is denoted as '0Z',
    # 'Z' being wild-type amino acid
    if len(s1) == 1 and '0Z' in s1:
        s1 = set()
    if len(s2) == 1 and '0Z' in s2:
        s2 = set()

    dpos_letters = dict((u[:-1], u[-1]) for u in s1.difference(s2))
    Dpos_letters = dict((u[:-1], u[-1]) for u in s2.difference(s1))
    positions = sorted(int(u) for u in set(list(dpos_letters.keys()) +
                                           list(Dpos_letters.keys())))
    reverse = False

    # Processing first position, which defines 'reverse' or 'forward'
    pos = str(positions[0])
    if pos in dpos_letters and pos in Dpos_letters:
        if dpos_letters[pos] < Dpos_letters[pos]:
            change = dpos_letters[pos] + pos + Dpos_letters[pos]
        else:
            change = Dpos_letters[pos] + pos + dpos_letters[pos]
            reverse = True
    elif pos in dpos_letters:
        change = dpos_letters[pos] + pos + 'Z'
    else:
        change = Dpos_letters[pos] + pos + 'Z'
        reverse = True
    delta = [change]

    # Now adding all other mutations
    for pos in positions[1:]:
        pos = str(pos)
        if pos in dpos_letters and pos in Dpos_letters:
            if not (reverse):
                change = dpos_letters[pos] + pos + Dpos_letters[pos]
            else:
                change = Dpos_letters[pos] + pos + dpos_letters[pos]
        elif pos in dpos_letters:
            if not (reverse):
                change = dpos_letters[pos] + pos + 'Z'
            else:
                change = 'Z' + pos + dpos_letters[pos]
        else:
            if reverse:
                change = Dpos_letters[pos] + pos + 'Z'
            else:
                change = 'Z' + pos + Dpos_letters[pos]

        delta.append(change)

    if reverse:
        return 'reverse', tuple(delta)
    else:
        return 'forward', tuple(delta)


def mergeiter(*iterables, **kwargs):
    """Given a set of sorted iterables, yield the next value in merged order

    Takes an optional `key` callable to compare values by.
    Taken from https://stackoverflow.com/questions/14465154/sorting-text-file-by-using-python?noredirect=1&lq=1
    """
    iterables = [iter(it) for it in iterables]
    iterables = {i: [next(it), i, it] for i, it in enumerate(iterables)}
    if 'key' not in kwargs:
        key = operator.itemgetter(0)
    else:
        key = lambda item, key=kwargs['key']: key(item[0])

    while True:
        value, i, it = min(iterables.values(), key=key)
        yield value
        try:
            iterables[i][0] = next(it)
        except StopIteration:
            del iterables[i]
            if not iterables:
                return


def sort_file(input_file_name: str, output_file_name: str):
    """Sort lines from the input_file_name in alphabetic order
       and print them to the output_file_name."""
    with open(input_file_name, 'r') as fh:
        lines = fh.readlines()

    lines.sort()
    with open(output_file_name, 'w') as fh:
        for line in lines:
            fh.write(line)


def merge_sorted_files(sorted_file_names: list, max_open_files: int, output_file_name: str) -> bool:
    """Merge files from 'sorted_file_names' and writes the
       content into 'output_file_name'."""
    if len(sorted_file_names) > max_open_files:
        num_parts = math.ceil(len(sorted_file_names) / max_open_files)
        num_files_in_part = math.ceil(len(sorted_file_names) / num_parts)
        found = False
        sorted_file_names_new: list = list()
        for i in range(num_parts):
            start_index = num_files_in_part * i
            end_index = num_files_in_part * (i + 1)
            output_file_name_new = sorted_file_names[i] + "." + str(i)
            f = merge_sorted_files(sorted_file_names[start_index:end_index],
                                   max_open_files, output_file_name_new)
            if not found:
                found = f
            sorted_file_names_new.append(output_file_name_new)
        if not found:
            return False
        else:
            return merge_sorted_files(sorted_file_names_new, max_open_files,
                                      output_file_name)
    else:
        # Open *.sorted files into filehandle list to enable merging
        filehandles: list = list()
        for sorted_file_name in sorted_file_names:
            fh = open(sorted_file_name, 'r')
            filehandles.append(fh)

        # Return False if no hypercubes are produced
        if len(filehandles) == 0:
            return False

        # Merge sorted hypercubes into file output_file_name
        with open(output_file_name, 'a') as fh:
            for line in mergeiter(*filehandles):
                print(line, end='', file=fh)

        for fh in filehandles:
            fh.close()

        for sorted_file_name in sorted_file_names:
            os.remove(sorted_file_name)

        return True
