#!/usr/bin/env python3
import sys

# importa a biblioteca sys para obter argumentos fornecidos pelo usuário
# verifica se um arquivo foi passado como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o arquivo")
    sys.exit(1)  # encerra o programa se não houver arquivo

file = sys.argv[1]  # recebe o arquivo da linha de comando
dic = {}  # cria um dicionário para armazenar as informações

# criando variáveis para armazenar cada categoria
sequence = ''  # armazenará temporariamente as sequências em strings
seqDESC = ''  # armazenará temporariamente a descrição de cada sequência em uma string
seqID = ''  # armazenará temporariamente a identificação da sequência

# abre o arquivo fornecido na linha de comando em modo de leitura
with open(file, 'r') as seq:
    for line in seq:  # itera sobre cada linha do arquivo
        if line.startswith('>'):  # se a linha começa com ">", significa que uma nova sequência se inicia
            if len(sequence) > 0:  # se a variável 'sequence' contém alguma sequência, armazena as informações no dicionário
                dic[seqID] = {'sequence': sequence, 'description': seqDESC}
            sequence = ''  # reinicia a variável
            line = line.lstrip('>')  # remove o ">" do início da linha
            line = line.rstrip()  # remove os espaços do fim da linha
            seqID, seqDESC = line.split(maxsplit=1)  # separa seqID, seqDESC e a sequência
        else:
            sequence += line.rstrip()  # se a linha não começa com ">", acumula à variável sequence
    # armazena a última sequência no dicionário
    if len(sequence) > 0:
        dic[seqID] = {'sequence': sequence, 'description': seqDESC}

# tabela de tradução
tabela_de_traducao = {
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
    'AAT': 'N', 'AAC': 'N', 'GAT': 'D', 'GAC': 'D', 'TGT': 'C', 'TGC': 'C', 'CAA': 'Q', 'CAG': 'Q', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G', 'CAT': 'H', 'CAC': 'H', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'TTA': 'L',
    'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'AAA': 'K', 'AAG': 'K', 'ATG': 'M', 'TTT': 'F', 'TTC': 'F',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S', 'AGC': 'S',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'TGG': 'W', 'TAT': 'Y', 'TAC': 'Y', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V',
    'GTG': 'V', 'TAA': '*', 'TGA': '*', 'TAG': '*'
}

# função para obter o complemento reverso
trans = str.maketrans("ATGC", "TACG")

# abre os arquivos de saída para escrever as sequências e suas traduções
output_codons_file = 'Python_08.codons-6frames.nt'
output_translated_file = 'Python_08.translated.aa'
output_longest_file = 'Python_08.translated-longest.aa'
output_orf_longest_file = 'Python_08.orf-longest.nt'

with open(output_codons_file, 'w') as codons_file, open(output_translated_file, 'w') as translated_file, open(output_longest_file, 'w') as longest_file, open(output_orf_longest_file, 'w') as orf_longest_file:
    all_codons = []
    all_translations = []

    for key in dic:
        seq_to_split = dic[key]['sequence']
        longest_peptide = ""
        longest_codon_sequence = ""

        # Processa os seis quadros de leitura
        for frame in range(3):
            seq_frame = seq_to_split[frame:]
            split_seq = ' '.join([seq_frame[i:i+3] for i in range(0, len(seq_frame), 3)])
            all_codons.append(f">{key}-frame-{frame + 1}\n{split_seq}")
            aa_translation = ''.join([tabela_de_traducao.get(seq_frame[i:i+3], 'X') for i in range(0, len(seq_frame), 3)])
            all_translations.append(f">{key}-frame-{frame + 1}\n{aa_translation}")

            # Encontra os peptídeos que começam com 'M' e terminam com '*'
            peptides = aa_translation.split('*')
            for pep in peptides:
                if 'M' in pep:
                    start = pep.find('M')
                    peptide = pep[start:]
                    codon_seq = ' '.join([seq_frame[i * 3:i * 3 + 3] for i in range(start, start + len(peptide))])

                    # Se o peptídeo encontrado for maior que o anterior, armazena o novo peptídeo e a sequência de códons
                    if len(peptide) > len(longest_peptide):
                        longest_peptide = peptide
                        longest_codon_sequence = codon_seq

        # Armazena a sequência do peptídeo mais longo para cada sequência
        longest_file.write(f">{key}-longest-peptide\n{longest_peptide}\n")
        orf_longest_file.write(f">{key}-longest-codons\n{longest_codon_sequence}\n")
    
    # Escreve os resultados de códons e traduções
    codons_file.write("\n".join(all_codons))
    translated_file.write("\n".join(all_translations))

# mensagem ao usuário informando que os arquivos foram gerados
print(f"As sequências divididas em códons e traduzidas para aminoácidos foram salvas em {output_codons_file}, {output_translated_file}, {output_longest_file} e {output_orf_longest_file}")

