#!/usr/bin/env python3

import sys  #importa a biblioteca sys para obter argumentos fornecidos pelo usuário

#verifica se um arquivo foi passado como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o arquivo")
    sys.exit(1)  #encerra o programa se não houver arquivo

file = sys.argv[1]  #recebe o arquivo da linha de comando

dic = {}  #cria um dicionário para armazenar as informações

#criando variáveis para armazenar cada categoria
sequence = ''  #armazenará temporariamente as sequências em strings
seqDESC = ''  #armazenará temporariamente a descrição de cada sequência em uma string
seqID = ''  #armazenará temporariamente a identificação da sequência

#abre o arquivo fornecido na linha de comando em modo de leitura
with open(file, 'r') as seq:

    for line in seq:  #itera sobre cada linha do arquivo
        if line.startswith('>'):  #se a linha começa com ">", significa que uma nova sequência se inicia
            if len(sequence) > 0:  #se a variável 'sequence' contém alguma sequência, armazena as informações no dicionário
                dic[seqID] = {'sequence': sequence, 'description': seqDESC}
                sequence = ''  #reinicia a variável
            line = line.lstrip('>')  #remove o ">" do início da linha
            line = line.rstrip()  #remove os espaços do fim da linha
            seqID, seqDESC = line.split(maxsplit=1)  #separa seqID, seqDESC e a sequência

        else:
            sequence += line.rstrip()  #se a linha não começa com ">", acumula à variável sequence

    #armazena a última sequência no dicionário
    if len(sequence) > 0:
        dic[seqID] = {'sequence': sequence, 'description': seqDESC}

#abre o arquivo de saída para escrever as sequências em códons
output_file = 'Python_08.codons-3frames.nt'
with open(output_file, 'w') as wFile:
    for key in dic:
        seq_to_split = dic[key]['sequence']  #obtém a sequência para dividir em códons

        #para cada um dos três quadros de leitura
        for frame in range(3):
            split_seq = ''
            seq_frame = seq_to_split[frame:]  #ajusta o quadro de leitura conforme o valor de 'frame'

            #divide a sequência em códons de 3 nucleotídeos e acumula
            for i in range(0, len(seq_frame), 3):
                split_seq += seq_frame[i:i+3] + ' '  #adiciona cada códon separado por espaço

            #remove o último espaço em branco e escreve no arquivo de saída
            wFile.write(f"{key}-frame-{frame + 1}-codons\n{split_seq.strip()}\n")

#mensagem ao usuário informando que o arquivo foi gerado
print(f"A sequência dividida em códons nos 3 quadros de leitura foi salva em {output_file}, gostaria de visualizar? s/n:")

#leitura da resposta do usuário
response = input().strip().lower()

#se a resposta for "s", exibe o conteúdo do arquivo
if response == 's':
    with open(output_file, 'r') as wFile:
        print(wFile.read())  #exibe o conteúdo do arquivo

elif response == 'n':
    print("O conteúdo do arquivo não será exibido.")
else:
    print("Opção inválida. Nenhuma ação será tomada.")
