"""
Принимает на вход фаста файлы со всеми найденными рамками считывания для генов,
убирает из названий мета-информацию о длине рамок и оставляет для каждой последовательности
только одну самую длинную ORF.
"""

from Bio import SeqIO
from glob import glob


original_file_path = glob("/home/asha/ZIN/magistrat/RNA/proteinortho/genes_by_group/CDS/*.fa")
corrected_file_path = "/home/asha/ZIN/magistrat/RNA/proteinortho/cleaned_genes_by_group/"

def clean_fasta_id(file_path, out_path):
    """
    Args:
        file_path: путь до файла с мультифастой, содержащей рамки считывания
        out_path: путь до выходного файла
    Returns:
        записывает очищенные ORF в файл, ничего не возвращает
        путь до выходного файла можно задать вручную
    """
    ids = {}
    name = file_path.split('/')[-1]
    print(name)
    output_path = out_path + name
    with open(file_path), open(output_path, 'w') as corrected:
        records = SeqIO.parse(file_path, 'fasta')
        for record in records:
            gene_id = str(record.id.split(':')[0]).split('|')[1]
            record.id = gene_id
            record.description = gene_id
            if gene_id not in ids:
                ids[gene_id] = str(record.seq)
            else:
                if len(ids[gene_id]) < len(record.seq):
                    ids[gene_id] = str(record.seq)

        names_id = ids.keys()
        seqs = ids.values()
        for n, s in zip(names_id, seqs):
            corrected.write('>' + n + '\n')
            corrected.write(s + '\n')
            # SeqIO.write(record, corrected, 'fasta')

for paths in original_file_path:
    clean_fasta_id(paths, corrected_file_path)