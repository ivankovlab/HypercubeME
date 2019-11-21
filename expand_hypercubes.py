from itertools import compress, product
import argparse
import os
import time

def get_combinations(items):
    """Get all variations of diagonal"""
    return (list(compress(items,mask)) for mask in product(*[[0,1]]*len(items)))

def diagonal_to_dict(diagonal):
    """Make dictionary from diagonal string"""
    diagonal_list = {}
    for mutation in diagonal:
        pos = mutation[:-1][1:]
        result = mutation[-1]
        diagonal_list[pos] = result
        
    return diagonal_list    

def apply_mutations(diagonal, variations, genotype):
    """Apply mutations to given genotype"""
    mutations_list = []
    for l in genotype.split(':'):
        if l[:-1] in variations:
            if  diagonal.get(l[:-1]) != 'Z':
                mutations_list.append(str(l[:-1]) + diagonal.get(l[:-1]))
            else:
                continue
        else:
            mutations_list.append(l)

    genotype_line = '0Z' if len(mutations_list) == 0 else ':'.join(mutations_list)

    return genotype_line
    

if __name__ == '__main__':   
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-hc', '--hypercubes', help='the filename with the list of measured genotypes')
    parser.add_argument('-of', '--output_file', help='the filename to write all variations')
    args = parser.parse_args()

    print('Expand hypercube ================')
    if args.hypercubes == '':
        print('ERROR: empty input filename')
        exit()

    if not os.path.isfile(args.hypercubes):
        print('ERROR: file {0} doesn\'t exist'.format(args.hypercubes))
        exit()

    if args.output_file is None:
        args.output_file = '{0}_expanded.txt'.format(os.path.splitext(os.path.basename(args.hypercubes))[0])

    if  os.path.isfile(args.output_file):
        print('ERROR: file {0} already exists, please rename/rebase existing file or specify output file name with argument -of'.format(args.output_file))
        exit()
        
    print('Start processing file: {0}'.format(args.hypercubes))

    try:
        with open(args.hypercubes, 'r') as f:
            f.readline()
            rows = []
            rows.append('diagonal \t variations')
            for line in f:
                line = line.replace('\n','')
                cols = line.split('\t')
                
                diagonal = cols[0]
                diagonal_dict = diagonal_to_dict(diagonal.split(':'))
                first_genotype = cols[1]
                
                genotypes = []
                genotypes.append(first_genotype)
                diagonal_variations = list(get_combinations(diagonal_dict))[1:]
                
                for variation in diagonal_variations:
                    m_genotype = apply_mutations(diagonal_dict, variation, first_genotype)
                    genotypes.append(m_genotype)
                
                rows.append(diagonal + '\t' + ', '.join(genotypes))
    except:
        print('ERROR: fail while reading file: please, be sure that the format of the input file is correct')
        exit()
        
    with open(args.output_file, 'w') as out_fh:
        for row in rows:
            print(row, file=out_fh)

    print('Expanding complete')
    print('Elapsed time: {0}'.format(time.time()-start_time))
    print('Output file saved as {0}'.format(args.output_file))