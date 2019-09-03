from random import seed
from csv import reader
from random import randrange

def carregar_dados(arquivo):
	dadosExcel = list()
	with open(arquivo, 'r') as Arquivo:
		csv_reader = reader(Arquivo)
		for linha in csv_reader:
			if not linha:
				continue
			dadosExcel.append(linha)
	return dadosExcel

def coluna_converte_para_float(dadosExcel, coluna):
	for linha in dadosExcel:
		linha[coluna] = float(linha[coluna].strip())
 
def coluna_converte_para_inteiro(dadosExcel, coluna):
	valores_classe = [linha[coluna] for linha in dadosExcel]
	valor_unico = set(valores_classe)
	mapear = dict()
	for i, valor in enumerate(valor_unico):
		mapear[valor] = i
	for linha in dadosExcel:
		linha[coluna] = mapear[linha[coluna]]
	return mapear

def separaDados(dadosExcel, separacao):
	dadosExcel_dividir = list()
	dadosExcel_copiar = list(dadosExcel)
	tamanho_separacao = int(len(dadosExcel) / separacao)
	for i in range(separacao):
		corte = list()
		while len(corte) < tamanho_separacao:
			index = randrange(len(dadosExcel_copiar))
			corte.append(dadosExcel_copiar.pop(index))
		dadosExcel_dividir.append(corte)
	return dadosExcel_dividir
 
def porcentagem(primeiro_valor, valor_previsto):
	temp = 0
	for i in range(len(primeiro_valor)):
		if primeiro_valor[i] == valor_previsto[i]:
			temp += 1
	return temp / float(len(primeiro_valor)) * 100.0
 
def testees_do_algoritimo(dadosExcel, algoritimo, separacao, *args):
	cortes = separaDados(dadosExcel, separacao)
	valoresFinais = list()

	for corte in cortes:
		treino = list(cortes)
		treino.remove(corte)
		treino = sum(treino, [])
		treino_atibuir = list()

		for linha in corte:
			linha_copiar = list(linha)
			treino_atibuir.append(linha_copiar)
			linha_copiar[-1] = None

		valor_previsto = algoritimo(treino, treino_atibuir, *args)
		primeiro_valor = [linha[-1] for linha in corte]
		porcentagemAcerto = porcentagem(primeiro_valor, valor_previsto)
		valoresFinais.append(porcentagemAcerto)

	return valoresFinais
 
def gradiente(linha, pesos):
	funcaoAtivacao = pesos[0]
	for i in range(len(linha)-1):
		funcaoAtivacao += pesos[i + 1] * linha[i]
	return 1.0 if funcaoAtivacao >= 0.0 else 0.0
 
def treino_pesos(treino, taxa_aprendizagem, numero_epocas):
	pesos = [0.0 for i in range(len(treino[0]))]
	for epoca in range(numero_epocas):
		for linha in treino:
			calculo_gradiente = gradiente(linha, pesos)
			erro = linha[-1] - calculo_gradiente
			pesos[0] = pesos[0] + taxa_aprendizagem * erro
			for i in range(len(linha)-1):
				pesos[i + 1] = pesos[i + 1] + taxa_aprendizagem * erro * linha[i]
	return pesos

def perceptron(treino, teste, taxa_aprendizagem, numero_epocas):
	calculo_gradientes = list()
	pesos = treino_pesos(treino, taxa_aprendizagem, numero_epocas)
	for linha in teste:
		calculo_gradiente = gradiente(linha, pesos)
		calculo_gradientes.append(calculo_gradiente)
	return(calculo_gradientes)
 
# Faz o teste do Algoritimo
seed(1)

arquivo = 'ValoresAtv.csv'
dadosExcel = carregar_dados(arquivo)
for i in range(len(dadosExcel[0])-1):
	coluna_converte_para_float(dadosExcel, i)
coluna_converte_para_inteiro(dadosExcel, len(dadosExcel[0])-1)

# Dados
separacao = 4
taxa_aprendizagem = 0.01
numero_epocas = 1000

valoresFinais = testees_do_algoritimo(dadosExcel, perceptron, separacao, taxa_aprendizagem, numero_epocas)

print('Numero de Epocas: %s' %numero_epocas)
print('Valores: %s' %valoresFinais)
print('Precisao: %.2f%%' %(sum(valoresFinais)/float(len(valoresFinais))))