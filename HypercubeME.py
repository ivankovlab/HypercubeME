import os
import time
import argparse
import multiprocessing as mp
from shutil import copyfile
import auxiliary as aux


def divide_genotype_list(num_genotypes: int, num_parts: int) -> list:
    """
    Divide 'num_genotypes' into 'num_parts' and return a list.

    Parameters
    ----------
        num_genotypes : int
            The number of genotypes.
        num_parts : int
            The number of parts.

    Returns
    -------
        division : list
            The list of tuples containing the starting line of the file
            and the number of lines of that chunk.
    """
    if num_genotypes == 0 or num_parts == 0:
        return list()

    # Division will be list of tuples (starting_line, number_of_lines_in_chunk)
    # to have compatibility with dimensions other than one
    division = list()

    if num_genotypes < num_parts:
        for i in range(num_genotypes + 1):
            division.append((i, 1, 0))
        return division

    for i in range(num_parts):
        current: int = round(i * num_genotypes/num_parts)
        following: int = round((i + 1) * num_genotypes/num_parts)
        division.append((current, following - current, 0))

    return division


def write_pairs(genotypes: list, start_index: int, chunk: int, output_file_name: str):
    """
    Write pairs at distance 1 to 'output_file_name' file forming by 'chunk'
       genotypes from 'start_index'

    Parameters
    ----------
        genotypes : list
            List of the genotypes.
        start_index : int
            The index of the first genotype to use.
        chunk : int
            The size of the chunk.
        output_file_name : str
            Name of the file where the pairs will be printed.
    """
    if start_index < 0 or chunk < 0:
        raise Exception("Both start index and number of lines in a chunk must be positive")

    if start_index >= len(genotypes):
        raise Exception("Start index must be less than the size of genotypes")

    # If end_index is too big, we set it equal to the size of genotypes
    chunk = min(chunk, len(genotypes) - start_index)
    lines: list = list()
    for i in range(start_index, start_index + chunk):
        for j in range(i + 1, len(genotypes)):
            direction, delta = aux.get_delta(genotypes[i], genotypes[j])
            if len(delta) == 1:
                if direction == 'forward':
                    lines.append(str(delta[0]) + '\t' + ':'.join(genotypes[i]) + '\t' + ':'.join(genotypes[j]))
                else:
                    lines.append(str(delta[0]) + '\t' + ':'.join(genotypes[j]) + '\t' + ':'.join(genotypes[i]))

    # Print pairs to the output file
    with open(output_file_name, 'w') as fh:
        for line in sorted(lines):
            print(line, file=fh)


def make_division_of_hypercube_file(input_file_name: str) -> list:
    """
    Generate division of the hypercube file into the
    chunks of parallel hypercubes.

    Parameters
    ----------
        input_file_name : str
            Name of the file containing the all the hypercubes.

    Returns
    -------
        division : list
            The division list. It is formed by triples.
            The first element is line of the chunk start.
            The second is the position (in lines) of the genotype in its chunk.
            The third is the chunk start position.
    """
    with open(input_file_name, 'r') as fh:
        # Skip header
        fh.readline()

        division = list()
        chunk_start_line = 1
        chunk_start_position = fh.tell()
        current_line = 1

        # Process lines with hypercubes
        line = fh.readline()
        previous_diagonal = line.split('\t')[0]
        previous_position = 0
        while line:
            diagonal = line.split('\t')[0]

            if diagonal != previous_diagonal:
                if current_line - chunk_start_line > 1:
                    # At least two lines in a chunk => can be a hypercube: add the chunk for processing
                    division.append((chunk_start_line, current_line - chunk_start_line, chunk_start_position))
                chunk_start_line = current_line
                chunk_start_position = previous_position

            previous_position = fh.tell()
            previous_diagonal = diagonal
            current_line += 1
            line = fh.readline()

    # Process correctly the end of file
    if current_line - chunk_start_line > 1:
        # At least two lines in a chunk => can be a hypercube: add the chunk for processing
        division.append((chunk_start_line, current_line - chunk_start_line, chunk_start_position))

    return division


def print_division(division: list):
    """Print division of the hypercube file into the chunks of parallel hypercubes"""
    print('Division into chunks (format: "start line"-"number of lines in chunk"):')
    max_length_of_line = 79
    first = True
    count = 0
    for (line, chunk, position) in division:
        if not first:
            print(', ', end='')
            count += len(', ')
        current = len(str(line) + str(chunk)) + 1
        count += current
        if count > max_length_of_line:
            print()
            count = current
        print(line, chunk, sep='-', end='')
        first = False
    print()


def process_diagonal(diagonal: str, same_diag_start: list, same_diag_end: list) -> str:
    """Take parallel hypercubes with the same 'diagonal',
       generate and return next-dimensional hypercubes."""
    diagonal_list = diagonal.split(':')
    lines: list = list()
    for i in range(len(same_diag_start) - 1):
        for j in range(i + 1, len(same_diag_start)):
            direction, delta = aux.get_delta(same_diag_start[i].split(':'), same_diag_start[j].split(':'))
            if len(delta) == 1 and diagonal_list[-1] < delta[0]:
                new_diagonal = diagonal + ':' + delta[0]
                if direction == 'forward':
                    lines.append(new_diagonal + '\t' + same_diag_start[i] + '\t' + same_diag_end[j])
                else:
                    lines.append(new_diagonal + '\t' + same_diag_start[j] + '\t' + same_diag_end[i])
    return lines


def process_file_with_hypercubes(hypercube_file_name: str, position: int, chunk_length: int, output_file_name: str):
    """Generate the next-dimensional hypercubes from 'hypercube_file_name'
       and write them into 'output_file_name'."""
    same_diag_start_list = list()
    same_diag_end_list = list()
    with open(hypercube_file_name, 'r') as fh:
        fh.seek(position)
        diagonal = ''
        for i in range(chunk_length):
            line = fh.readline()
            diagonal, start, end = line.strip().split('\t')
            same_diag_start_list.append(start)
            same_diag_end_list.append(end)

        lines = process_diagonal(diagonal, same_diag_start_list, same_diag_end_list)

    with open(output_file_name, 'w') as out_fh:
        for line in sorted(lines):
            print(line, file=out_fh)


def process_dimension_one(cores: int, input_file: str, working_dir: str) -> list:
    """Generate all one-dimensional hypercubes from the list of genotypes"""
    genotypes = aux.read_genotypes(input_file)
    num_genotypes = len(genotypes)
    chunks_per_core = 10        # That is, every core has, on average, 10 chunks of work
    chunks = cores * chunks_per_core
    chunks = min(chunks, num_genotypes)
    division = divide_genotype_list(num_genotypes, chunks)

    args = list()
    outfiles = list()
    for chunk in range(chunks):
        outfile_name = working_dir + '/' + str(chunk) + '.txt'
        outfiles.append(outfile_name)
        args.append((genotypes, division[chunk][0], division[chunk][1], outfile_name))

    with mp.Pool(processes=cores) as pool:
        pool.starmap(write_pairs, args)

    return division


def process_dimension(cores: int, hypercube_file_name: str, working_dir: str) -> list:
    """
    Generate all hypercubes of dimension 'dim' from
    hypercubes of lower dimension 'dim-1'.

    The hypercubes of lower dimension are given in the file 'hypercube_{dim-1}.txt'.

    """

    # Understand where in the hypercube_file_name chunks with the same diagonal
    division = make_division_of_hypercube_file(hypercube_file_name)
    chunks = len(division)

    args = list()
    for chunk in range(chunks):
        chunk_start, chunk_length, position = division[chunk]
        output_file_name = working_dir + '/' + str(chunk) + ".txt"
        args.append((hypercube_file_name, position, chunk_length, output_file_name))

    with mp.Pool(processes=cores) as pool:
        pool.starmap(process_file_with_hypercubes, args)

    return division


def get_dimension(filename: str) -> int:
    """Return dimension of the hypercubes stored in the file 'filename'."""
    print('\'' + filename + '\'')
    with open(filename, 'r') as fh:
        # Calculate dimension as number of fields in the diagonal
        dimension = len(fh.readline()[0].split(':'))
    return dimension


def hypercube_file_name(dimension: int) -> str:
    """Return the name of the file where hypercubes
       of the given 'dimension' are stored."""
    return 'hypercubes_' + str(dimension) + '.txt'


if __name__ == '__main__':      # Multiprocessing does not work without this line
    start_time: float = time.time()

    # Maximum number of open files
    # Linux can usually have maximum 1021 open filehandles for files ('ulimit -n')
    # Windows 10 can usually have 8189 for files, but we set here universal value of 1021
    max_open_files = 1021

    # Process arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--genotypes', help='the filename with the list of measured genotypes')
    group.add_argument('-p', '--hypercubes', help='the filename with the list of already calculated hypercubes')
    parser.add_argument('-d', '--folder', help='name of non-existing folder to store intermediate and result files, '
                                               '"hypercubes" by default',
                        default='hypercubes')
    parser.add_argument('-c', '--cores', help='the number of cores to be used in calculation, one by default',
                        type=int, default=1)
    parser.add_argument('-v', '--verbose', help='print detailed information', action='store_true')
    args = parser.parse_args()
    print('HypercubeME, version 1.0 ================================================')
    print('Arguments passed:', args, '\n')

    # Create output folder
    if args.folder.strip() == '':
        print('ERROR: Folder "{0}" contains only whitespaces, give me valid name'.format(args.folder))
        exit(1)
    if os.path.exists(args.folder):
        print('ERROR: Folder/file "{0}" exists, run again with another folder name'.format(args.folder))
        exit(1)
    try:
        os.mkdir(args.folder)
    except:
        print('ERROR: Unable to create folder {0}'.format(args.folder))
        exit(1)

    dimension: int = 1
    if args.hypercubes is not None:
        # Start with hypercubes
        try:
            dimension = get_dimension(args.hypercubes)
        except FileNotFoundError:
            print('ERROR: File "{0}" not found. Please, specify the existing file'.format(args.hypercubes))
            exit(1)
        copyfile(args.hypercubes, args.folder + '/' + hypercube_file_name(dimension))
        dimension += 1

    # Run iterative process of producing N-dimensional hypercubes from (N-1)-dimensional ones
    division: list = list()
    while True:
        print('Generate hypercubes for dimension {0}'.format(dimension))

        # Find hypercubes and write them in sorted order into files 0.txt, 1.txt, ...
        input_file_name: str = ''
        if dimension == 1:
            input_file_name = args.genotypes
            try:
                division = process_dimension_one(args.cores, input_file_name, args.folder)
            except FileNotFoundError:
                print('ERROR: File "{0}" not found. Please, specify the existing file'.format(input_file_name))
                exit(1)
        else:
            input_file_name = args.folder + '/' + hypercube_file_name(dimension - 1)
            division = process_dimension(args.cores, input_file_name, args.folder)

        chunks: int = len(division)
        print('Number of chunks:', chunks)
        if chunks == 0:
            break

        if args.verbose:
            print_division(division)

        # Collect file names of all non-empty files 0.txt, 1.txt, ... into the list
        sorted_file_names: list = list()
        for chunk in range(chunks):
            sorted_file_name = args.folder + '/' + str(chunk) + '.txt'
            if not os.path.isfile(sorted_file_name):
                continue
            elif os.stat(sorted_file_name).st_size == 0:
                os.remove(sorted_file_name)
                continue
            sorted_file_names.append(sorted_file_name)

        with open(args.folder + '/' + hypercube_file_name(dimension), 'w') as fh:
            print('diagonal first_genotype last_genotype', file=fh)
        found = aux.merge_sorted_files(sorted_file_names, max_open_files, args.folder + '/' +
                                       hypercube_file_name(dimension))

        if found == False:
            break

        dimension += 1
        print()

    end_time = time.time()
    print()
    print('Normal termination of the program, check the folder "{0}" for results'.format(args.folder))
    print('Process time:', end_time - start_time)
