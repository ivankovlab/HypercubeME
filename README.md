# HypercubeME
Generate all combinatorially complete datasets from the given genotype list

## Citation
Esteban LA, Lonishin LR, Bobrovskiy D, Leleytner G, Bogatyreva NS, Kondrashov FA, Ivankov DN.  
HypercubeME: two hundred million combinatorially complete datasets from a single experiment.  
Bioinformatics, 2019, 36:1960-1962.  
doi: 10.1093/bioinformatics/btz841.  
PMID: 31742320.

## Usage
Run in the command line following examples:

Get short help message:

`python3 HypercubeME.py`

Get help message:

`python3 HypercubeME.py -h`

Generate all hypercubes from the example file 'test_complete_03.txt'. Obtained hypercubes are stored in files 'hypercube_\*.txt' located in the newly created folder 'hypercubes':

`python3 HypercubeME.py -g test_complete_03.txt`

Same as before but writing the results into the folder 'test_complete_03':

`python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03`

Same as before but using two cores of the computer:

`python3 HypercubeME.py -g test_complete_03.txt -d test_complete_03 -c 2`

Generate hypercubes of dimensionality two and higher from already calculated one-dimensional hypercubes stored in the file 'test_expected/hypercube_1.txt'. This option is useful if the computation was interrupted and it is desired to continue the calculation rather than start from the very beginning:

`python3 HypercubeME.py -p test_expected/hypercube_1.txt`

## Input format
See the file 'test_complete_03.txt' for input example. Columns are tab-separated, first line is a header which is ignored by 'HypercubeME.py'. First column (example: '0C:2T') is a colon-separated mutation list of a particular mutant variant. Each mutation consists of mutated position and the variant (amino acid residue or RNA/DNA base) where it is mutated. For wild-type 'HypercubeME.py' uses '0Z', where 'Z' means wild-type variant (amino acid residue or RNA/DNA base); however, in the genotype file wild-type can also be denoted as empty string as in the file 'test_complete_03.txt'. All other columns are ignored by 'HypercubeME.py'.

## Output format
See the file 'test_expected/hypercubes_2.txt' for output example. Columns are tab-separated, first line is a header. Hypercubes are written in a short format to save the disk space. To get hypercubes in full format use expand_hypercube.py utility (see below). The first column of the output (example: 'A1Z:C0Z') is a diagonal of a hypercube containing mutations separated by semicolon. Each mutation in the diagonal consists of initial variant, position, and the resulting variant, where wild-type is denoted as 'Z'. The remaining two columns contain the first (example: '0C:1A') and the last (example: '0Z', that is, wild-type) genotypes of the hypercube. So, mutations from the diagonal when applied to the first genotype give you the last genotype: '0C:1A' + 'A1Z:C0Z' = '0Z'.

## Full hypercube representation
To get full hypercube representation use 'expand_hypercubes.py' utility.

Arguments:
- -p *input_hypercubes_filename*, path to file with hypercubes in short format. This file is an output file of the 'HypercubeME.py' script.
- -o (optional) *output_hypercubes_filename*, resulting file, default value: *input_hypercubes_filename*_expanded.txt

Take hypercubes in the short format from the file 'hypercubes/hypercubes_5.txt' and write them expanded into the default file 'hypercubes_5_expanded.txt' in the current folder:  

`python expand_hypercubes.py -p hypercubes/hypercubes_5.txt`

The same as before but write the output into the user-defined file 'hypercubes/hypercubes_5_expanded.txt':  

`python expand_hypercubes.py -p hypercubes/hypercubes_5.txt -o hypercubes/hypercubes_5_expanded.txt`
