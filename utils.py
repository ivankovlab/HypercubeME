# TODO: write Docs

def read_file_with_hypercubes(hypercube_file_name: str):
    """Read the file 'hypercube_file_name'
       and store it on memory."""

    same_diag_start_list = list()
    same_diag_end_list = list()
    with open(hypercube_file_name, 'r') as fh:
        diagonal = ''
        next(fh)
        for line in fh:
            diagonal, start, end = line.strip().split('\t')
            same_diag_start_list.append(start)
            same_diag_end_list.append(end)
    return same_diag_start_list, same_diag_end_list
