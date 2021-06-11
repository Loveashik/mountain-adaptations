import os
from glob import glob

paths = glob('/home/taxon/RNA/assembled/peptide_trinity/*.fasta')
names = [p.split('/')[-1].split('.')[0] for p in paths]

for p, n in zip(paths, names):
        print('='*50)
        print(f'Now working on {n} guy...')
        print('='*50)
        os.system(f'diamond blastp --db /home/DBS/nr.gz --query {p} --out /home/taxon/RNA/annotated/by_protein/{n}.diamond.tsv --threads 10 -b8 -c1 --max-target-seqs 1')
        print('='*50)
        print(f'Finished with {n}!')
        print('='*50)