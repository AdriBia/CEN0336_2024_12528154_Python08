#!/usr/bin/env python3

import sys #importa a biblioteca sys para obter argumentos fornecidos pelo usuário

#verifica se um arquivo foi passado como argumento
if len(sys.argv) < 2:
	print("Por favor, forneça o arquivo")
	sys.exit(1) #encerra o programa se não houver arquivo

file = sys.argv[1] #recebe o arquivo da linha de comando

dic= {}  #cria um dicionário para armazenar as informações

#criando variáveis para armazenar cada categoria:
sequence = '' #armazenará temporariamente as sequências em strings
seqDESC = '' #armazenará temporariamente a descrição de cada sequencia em uma string
seqID = '' #armazenará temporariamente a identificação da sequência

with open(file, 'r') as seq: #Abre o arquivo fornecido na linha de comando em modo de leitura

  for line in seq: #itera sobre cada linha do arquivo
    if line.startswith('>'): #declara que se a linha começa com ">", significa que uma nova sequência se inicia
      if len(sequence) > 0: #identifica se a variável 'sequence' contém alguma informação
        dic[seqID] = { 'sequence' : sequence , 'description' : seqDESC } #caso sim, armazena as informações no dicionário
        sequence= '' #reinicia a variável
      line = line.lstrip('>') #remove o ">" do inicio da linha
      line = line.rstrip() #remove os espaços do fim da linha
      seqID, seqDESC = line.split(maxsplit = 1) #separa seqID, SeqDESC e a sequência.

    else:
      sequence += line.rstrip() #se a sequência nao se iniciar em ">", acumula à variável sequence apenas retirando o espaço final.

  if len(sequence) > 0: #ao final do loop armazena as ultimas variáveis
        dic[seqID] = { 'sequence' : sequence , 'description' : seqDESC }

#itera cada sequência no dicionario para fazer a contagem
  for key in dic:
    seq_to_count = dic.get(key).get('sequence') #chama a sequência de cada ID

#conta cada nucleotídeo e armazena cada tipo em sua respectiva variável
    countA = seq_to_count.count('A')
    countT = seq_to_count.count('T')
    countC = seq_to_count.count('C')
    countG = seq_to_count.count('G')

#armazena os resultados da contagem, substituindo pelo novo a cada contagem.
    dic[key] = { 'sequence_composition' : { 'A' : countA , 'T' : countT , 'C' : countC , 'G' : countG } }

#imprime as informações ao usuário.
    print(key + '\tA:' + str(countA) + '\tT:' + str(countT) + '\tG:' + str(countG) + '\tC:' + str(countC))
