#!/usr/bin/env python3
import sys

#importa a biblioteca sys para obter argumentos fornecidos pelo usuário
if len(sys.argv) < 2:
    print("Por favor, forneça o arquivo")
    sys.exit(1)  #encerra o programa se não houver arquivo

file = sys.argv[1]  #recebe o arquivo da linha de comando
dic = {}  #cria um dicionário para armazenar as informações

#variáveis para armazenar cada categoria
sequence = ''
seqDESC = ''
seqID = ''

#abre o arquivo fornecido na linha de comando em modo de leitura
with open(file, 'r') as seq:
    for line in seq:
        if line.startswith('>'):
            if len(sequence) > 0:
                dic[seqID] = {'sequence': sequence, 'description': seqDESC}
            sequence = ''
            line = line.lstrip('>').rstrip()
            seqID, seqDESC = line.split(maxsplit=1)
        else:
            sequence += line.rstrip()
    if len(sequence) > 0:
        dic[seqID] = {'sequence': sequence, 'description': seqDESC}

#tabela de tradução
tabela_de_traducao = {
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
    'AAT': 'N', 'AAC': 'N', 'GAT': 'D', 'GAC': 'D', 'TGT': 'C', 'TGC': 'C', 'CAA': 'Q', 'CAG': 'Q', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G', 'CAT': 'H', 'CAC': 'H', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'TTA': 'L',
    'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'AAA': 'K', 'AAG': 'K', 'ATG': 'M', 'TTT': 'F', 'TTC': 'F',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S', 'AGC': 'S',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'TGG': 'W', 'TAT': 'Y', 'TAC': 'Y', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V',
    'GTG': 'V', 'TAA': '*', 'TGA': '*', 'TAG': '*'
}

#função para obter o complemento reverso
trans = str.maketrans("ATGC", "TACG")

#arquivos de saída
output_codons_file = 'Python_08.codons-6frames.nt'
output_translated_file = 'Python_08.translated.aa'
output_longest_file = 'Python_08.translated-longest.aa'

with open(output_codons_file, 'w') as codons_file, open(output_translated_file, 'w') as translated_file, open(output_longest_file, 'w') as longest_file:
    all_codons = []
    all_translations = []

    for key in dic:
        seq_to_split = dic[key]['sequence']
        longest_peptide = ""

        #processa os seis quadros de leitura
        for frame in range(3):
            seq_frame = seq_to_split[frame:]
            split_seq = ' '.join([seq_frame[i:i+3] for i in range(0, len(seq_frame), 3)])
            all_codons.append(f">{key}-frame-{frame + 1}\n{split_seq}")
            aa_translation = ''.join([tabela_de_traducao.get(seq_frame[i:i+3], 'X') for i in range(0, len(seq_frame), 3)])
            all_translations.append(f">{key}-frame-{frame + 1}\n{aa_translation}")

            #encontra o peptídeo mais longo para o quadro
            peptides = aa_translation.split('*')
            for pep in peptides:
                if 'M' in pep:
                    start = pep.find('M')
                    peptide = pep[start:]
                    if len(peptide) > len(longest_peptide):
                        longest_peptide = peptide

        #processa os seis quadros de leitura negativos (complemento reverso)
        rev_seq = seq_to_split.translate(trans)[::-1]
        for frame in range(3):
            seq_frame = rev_seq[frame:]
            split_seq = ' '.join([seq_frame[i:i+3] for i in range(0, len(seq_frame), 3)])
            all_codons.append(f">{key}-frame-{-(frame + 1)}\n{split_seq}")
            aa_translation = ''.join([tabela_de_traducao.get(seq_frame[i:i+3], 'X') for i in range(0, len(seq_frame), 3)])
            all_translations.append(f">{key}-frame-{-(frame + 1)}\n{aa_translation}")

            #encontra o peptídeo mais longo para o quadro
            peptides = aa_translation.split('*')
            for pep in peptides:
                if 'M' in pep:
                    start = pep.find('M')
                    peptide = pep[start:]
                    if len(peptide) > len(longest_peptide):
                        longest_peptide = peptide

        #escreve o peptídeo mais longo no arquivo de saída
        longest_file.write(f">{key}\n{longest_peptide}\n")

    #escreve os resultados de uma vez
    codons_file.write("\n".join(all_codons))
    translated_file.write("\n".join(all_translations))

print(f"As sequências divididas em códons e traduzidas foram salvas em {output_codons_file} e {output_translated_file}.")
print(f"O peptídeo mais longo de cada sequência foi salvo em {output_longest_file}.")
