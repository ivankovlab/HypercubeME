from itertools import compress, product
import argparse
import sys
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
    parser.add_argument('-of', '--output_file', help='the filename to write all variations', 
                        default='expanded_hypercubes_{0}.txt'.format(time.strftime("%Y-%m-%d-%H-%M", time.localtime())))
    args = parser.parse_args()
    print('Expand hypercube ================')
    if args.hypercubes == '':
        print('ERROR: empty input filename')
        exit()

    if not os.path.isfile(args.hypercubes):
        print('ERROR: file {0} doesn\'t exist'.format(args.hypercubes))
        exit()

    print('Start processing file: {0}'.format(args.hypercubes))
    with open(args.hypercubes, 'r') as f:
        f.readline()
        rows = []
        rows.append('diagonal \t first_genotype \t variations')
        for line in f:
            line = line.replace('\n','')
            cols = line.split('\t')
            
            diagonal = cols[0]
            diagonal_dict = diagonal_to_dict(diagonal.split(':'))
            first_genotype = cols[1]
            
            genotypes = []
            diagonal_variations = list(get_combinations(diagonal_dict))[1:]
            
            for variation in diagonal_variations:
                m_genotype = apply_mutations(diagonal_dict, variation, first_genotype)
                genotypes.append(m_genotype)
            
            rows.append(diagonal + '\t' + first_genotype + '\t' + ', '.join(genotypes))

    with open(args.output_file, 'w') as out_fh:
        for row in rows:
            print(row, file=out_fh)

    print('Expanding complete')
    print('Elapsed time: {0}'.format(time.time()-start_time))
    print('Output file saved as {0}'.format(args.output_file))