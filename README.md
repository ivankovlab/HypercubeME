# HypercubeME
Generate all combinatorially complete datasets from the given genotype list

## Usage
Run in the command line following examples:

Get short help message:

python3 HypercubeME.py

Get help message:

python3 HypercubeME.py -h

Generate all hypercubes from the file 'test_complete_03.txt'. As a result, hypercubes are written into files 'hypercube_\*.txt' stored in the newly created folder 'hypercubes'.

python3 HypercubeME.py -g test_complete_03.txt

Same as before but writing the results into the folder 'test_complete_03'

python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03

Same as before but using two cores of the computer

python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03 -c 2

Generate hypercubes of dimensionality two and higher from one-dimensional hypercubes stored in the file 'hypercube_1.txt'. Useful if the computation was interrupted and it is desired to continue from the middle of the process.

python3 HypercubeME.py -p test_expected/hypercube_1.txt

## Input format
See the file 'test_complete_03.txt' for example, columns are tab-separated, first line is a header:

mut_list	fitness	error

    0.15641055120485037	0.06235045412543177

0C:2T	0.1718712615576915	0.06538658769979198

0C:1A:2T	0.22727007820835443	0.05868817972931428

...

First column is a mutation consisting of mutated position and the amino acid where it is mutated. Wild-type is denoted as empty string. Second and third columns usually come from the experiment but HypercubeME program ignores them.

## Output format
See the file 'test_expected/hypercubes_2.txt' for example, columns are tab-separated, first line is a header:

diagonal first_genotype last_genotype

A1Z:C0Z	0C:1A	0Z

A1Z:C0Z	0C:1A:2T	2T

...

The hypercube is written in a short format to save the disk space. The first column is a diagonal of a hypercube (containing mutations separated by semicolumn, each mutation consisting of initial amino acid, position, and the resulting amino acid), the remaining two columns contain the first and the last genotypes of the hypercube. So that if to apply changes from the diagonal to the first genotype, you get the last genotype.
