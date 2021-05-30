import os
import Bio.SeqIO as SeqIO
import re

ortho_file = '/home/asha/ZIN/magistrat/RNA/proteinortho/groups_13.tsv'
#Сюда нужно вставить ссылку на таблицу с очищенными ортологическими рядами. Сейчас разделитель запятая. можно менять

species_list = ['brandtii', 'fortis', 'glareolus',	'gregalis', 'lemminus2', 'macrotis', 'mandarinus', 'nivalis',
                'pennsylvanicus', 'raddei', 'rufocanus', 'rutilus2', 'tuvinicus']

#Здесь нужно указать порядок видов, как он идет в таблице с ортологическими рядами
species = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},{}]
#В листе сделать нужное количество словарей, соответствующее количеству изучаемых видов

directory = '/home/asha/ZIN/magistrat/RNA/proteinortho/genes_data/'
#Ссылка на папку, в которой лежат cds фасты (нуклеотидные) всех изучаемых видов

output_dir = '/home/asha/ZIN/magistrat/RNA/proteinortho/genes_by_group/'
#Ссылка на папку, куда будут сохраняться результаты

def write_dictionaries(line, count):
    """
    Заполняет файл со словарями по порядку, присваивая каждому гену номер ортологической группы
    """
    org = 0
    for genes in line:
        if org != len(line)-1:
            name = species[org]
            name[genes] = count
        else:
            name = species[org]
            genes = genes[:-1]
            name[genes] = count
        org += 1

def create_dictionaries():
    # "Читает таблицу с ортологическими рядами и по очереди отдает их функции write_dictionaries"
    with open(ortho_file, 'r') as ortologues:
        count = 1
        for line in ortologues:
            line = line.split('\t')
            write_dictionaries(line, count)
            count += 1

def write_clusters(sequence, ortho_group, org_name):
    """
    записывает все в файлы. Номер файла соответствует номеру ортогруппы
    """
    #
    os.chdir(output_dir)
    cluster_name = str(ortho_group) + '.fasta'
    with open(cluster_name, 'a') as answer:
        answer.write('>' + org_name)
        answer.write('\n')
        answer.write(sequence)
        answer.write('\n')

def read_fasta(file, org_number, org_name):
    """
    Читает фасты изучаемых видов и ищет нужные транскрипты в созданных словарях
    """

    full_way = directory + file
    fasta_file = SeqIO.parse(open(full_way), 'fasta')
    for fasta in fasta_file:
        name, sequence = fasta.id, str(fasta.seq)
        my_d = species[org_number]
        if name in my_d.keys():
            ortho_group = my_d[name] - 1
            write_clusters(name, sequence, ortho_group, org_name)

create_dictionaries()
files = os.listdir(directory)

for file in files:
    org_name = file
    org_number = species_list.index(org_name)
    read_fasta(file, org_number, org_name)
