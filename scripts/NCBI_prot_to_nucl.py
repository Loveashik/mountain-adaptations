"""
Берет на вход белковую таблицу ортологов и создает список ID исходных мРНК (модифицирован)
"""

import re
import itertools


def open_function(protein_file):
    """
    записывает все белки из списка в словарь. Поскольу в конце есть перенос строки, то его убираем
    """
    with open(protein_file, 'r') as ortologues:
        count = 1
        for line in ortologues:
            proteins[line[:-1]] = []
            order[line[:-1]] = count
            count += 1


def distributor(rna, ids,value):
    """
    создает словарь соответствия rna - transcript ID и protein ID - Parent
    """

    if value == 'protein' and ids in proteins.keys():
        print('Find it into ortologues')
        proteins[ids] += [rna]
    if value == 'transcript' and rna not in transcripts.keys():
        print('Add it to transcripts')
        transcripts[rna] = ids

def retriever(gff_file):
    """
    из gff файла выцеляет соответствие  белковое ID - Parent RNA
    """
    with open(gff_file, 'r') as gff:
        for line in gff:
            match_rna = re.compile(r'Parent=rna-([A-Za-z\_0-9\.]+)')
            if match_rna.findall(line):
                print(match_rna.findall(line)[0])
                rna = match_rna.findall(line)[0]
                match_protein = re.compile(r'protein_id=([A-Za-z\_0-9\.]+)')
                if match_protein.findall(line):
                    ids = match_protein.findall(line)[0]
                    distributor(rna, ids, 'protein')
                match_transcript = re.compile(r'transcript_id=([A-Za-z\_0-9\.]+)')
                if match_transcript.findall(line):
                    ids = match_transcript.findall(line)[0]
                    distributor(rna, ids, 'transcript')




def table_divide(protein,i,length, new_value, table):
    """
    Создает таблицу Prot- количество rna - rna- transcript для каждого вида
    """
    table[i][0] = protein
    table[i][1] = list(str(length))
    table[i][2] = new_value
    for value in new_value:
        if value in transcripts.keys():
            table[i][3].append(transcripts[value])
        else:
            table[i][3] = 'Non transcripts found'

def table_creator(table_name):
    table = [[[] for i in range(4)] for _ in range(len(order))]
    for key, value in proteins.items():
        i = order[key] -1
        protein = key
        new_value = list(set(value))
        length = len(new_value)
        table_divide(protein,i,length, new_value, table)
    with open(table_name, 'w') as answer:
        for elem in table:
            answer.write(str(elem[-1]).strip('[\']'))
            answer.write('\n')
            print(str(elem).strip())

def common_function(gff_file, protein_file, table_name):

    global proteins, transcripts, order
    proteins = {}
    transcripts = {}
    order = {}
    open_function(protein_file)
    retriever(gff_file)
    table_creator(table_name)

#На вход дается gff, файл с белковыми ID, соответствие которым нужно установить и название выходного файла

common_function('/home/asha/ZIN/magistrat/RNA/proteinortho/Ocrogaster.gff',
    '/home/asha/ZIN/magistrat/RNA/proteinortho/genes_data/ochrogaster_ID.txt',
    'Ochrogaser_good.genes')
