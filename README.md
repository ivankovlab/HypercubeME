# HypercubeME
Generate all combinatorially complete datasets from the given genotype list

## Usage
Run in the command line following examples:

Get short help message:

`python3 HypercubeME.py`

Get help message:

`python3 HypercubeME.py -h`

Generate all hypercubes from the example file 'test_complete_03.txt'. Obtained hypercubes are stored in files 'hypercube_\*.txt' located in the newly created folder 'hypercubes'.

`python3 HypercubeME.py -g test_complete_03.txt`

Same as before but writing the results into the folder 'test_complete_03'

`python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03`

Same as before but using two cores of the computer

`python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03 -c 2`

Generate hypercubes of dimensionality two and higher from already calculated one-dimensional hypercubes stored in the file 'test_expected/hypercube_1.txt'. This option is useful if the computation was interrupted and it is desired to continue the calculation rather than start from the very beginning.

`python3 HypercubeME.py -p test_expected/hypercube_1.txt`

## Input format
See the file 'test_complete_03.txt' for input example. Columns are tab-separated, first line is a header which is ignored by HypercubeME. First column (example: '0C:2T') is a column-separated mutation list of a particular mutant variant. Each mutation consists of mutated position and the amino acid where it is mutated. For wild-type HypercubeME uses '0Z', where 'Z' means wild-type amino acid residue; however, in the genotype file wild-type can also be denoted as empty string as in the file 'test_complete_03.txt'. All other columns are ignored by HypercubeME.

## Output format
See the file 'test_expected/hypercubes_2.txt' for output example. Columns are tab-separated, first line is a header. The hypercube is written in a short format to save the disk space. The first column (example: 'A1Z:C0Z') is a diagonal of a hypercube containing mutations separated by semicolumn. Each mutation in the diagonal consists of initial amino acid, position, and the resulting amino acid, where wild-type variant is denoted as 'Z'. The remaining two columns contain the first (example: '0C:1A') and the last (example: '0Z', that is, wild-type) genotypes of the hypercube. So that, the mutations from the diagonal applied to the first genotype give you the last genotype: '0C:1A' + 'A1Z:C0Z' = '0Z'
