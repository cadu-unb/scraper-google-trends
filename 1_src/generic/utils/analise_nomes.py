from difflib import SequenceMatcher

def possui_palavra_proxima(palavra_alvo, lista_palavras, tolerancia=0.8):
    """
    Retorna True se houver uma palavra na lista muito próxima da palavra_alvo.
    A 'tolerancia' vai de 0.0 (nada a ver) a 1.0 (identicas).
    0.8 geralmente pega variações de 1 ou 2 letras dependendo do tamanho da palavra.
    """
    # Normaliza a palavra alvo para evitar problemas com maiúsculas/minúsculas
    palavra_alvo = palavra_alvo.lower().strip()
    
    for palavra in lista_palavras:
        palavra_normalizada = palavra.lower().strip()
        
        # O SequenceMatcher calcula a similaridade entre as duas strings
        similaridade = SequenceMatcher(None, palavra_alvo, palavra_normalizada).ratio()
        
        if similaridade >= tolerancia:
            return True
            
    return False

def encontrar_palavra_proxima(palavra_alvo, lista_palavras, tolerancia=0.8):
    """
    Procura na lista uma palavra muito próxima da palavra_alvo.
    Retorna a palavra encontrada (da lista) ou None se nenhuma for próxima o suficiente.
    """
    palavra_alvo_norm = palavra_alvo.lower().strip()
    
    for palavra in lista_palavras:
        palavra_norm = palavra.lower().strip()
        
        # Calcula a similaridade entre as duas
        similaridade = SequenceMatcher(None, palavra_alvo_norm, palavra_norm).ratio()
        
        # Se atingir a tolerância, retorna a palavra ORIGINAL da lista (com maiúsculas/minúsculas originais)
        if similaridade >= tolerancia:
            return palavra
            
    return None

def mapear_chaves_da_palavra(palavra_busca, dicionario_dados, tolerancia=0.8):
    """
    Varre o dicionário e retorna uma lista com todas as chaves onde
    a palavra_busca (ou algo muito parecido) foi encontrada.
    """
    chaves_encontradas = []
    
    # Percorre o dicionário chave por chave, pegando a lista de palavras de cada uma
    for chave, lista_de_palavras in dicionario_dados.items():
        
        # Usamos a função anterior para ver se a palavra está nesta lista específica
        # (Estou assumindo que 'encontrar_palavra_proxima' está no mesmo arquivo ou importada)
        palavra_match = encontrar_palavra_proxima(palavra_busca, lista_de_palavras, tolerancia)
        
        # Se encontrou alguma palavra próxima (ou seja, não é None)
        if palavra_match is not None:
            chaves_encontradas.append(chave)
            
    return chaves_encontradas

def verificar_inedito(string_busca, lista_de_listas, tolerancia=0.8):
    """
    Retorna False se a string_busca for próxima de algum elemento da lista_de_listas.
    Retorna True se a string_busca for totalmente nova (inedita).
    """
    # Vamos percorrer cada sublista (linha) da sua estrutura
    for linha in lista_de_listas:
        # 'linha' aqui é algo como ["Análise de Dados", "(estruturação...)"]
        
        # Usamos a nossa função para buscar dentro dessa linha específica
        match = encontrar_palavra_proxima(string_busca, linha, tolerancia)
        
        # Se achou qualquer proximidade na linha (seja no título ou na descrição)
        if match is not None:
            return False  # Houve ocorrência!
            
    return True  # Passou por tudo e não achou nada parecido

__all__ = ["possui_palavra_proxima", "encontrar_palavra_proxima", "mapear_chaves_da_palavra", "verificar_inedito"]

if __name__ == 'main':
    # --- Exemplos de teste ---

    lista = ["computador", "celular", "caderno", "caneta"]

    # Teste 1: Uma letra trocada (computador -> computalor)
    print(possui_palavra_proxima("computalor", lista))  # Retorna True

    # Teste 2: Uma letra a mais (celular -> celulare)
    print(possui_palavra_proxima("celulare", lista))    # Retorna True

    # Teste 3: Uma palavra totalmente diferente
    print(possui_palavra_proxima("garrafa", lista))     # Retorna False

    # --- Testando a nova função ---

    lista_cadastro = ["Computador", "Celular", "Caderno", "Caneta"]

    # Teste 1: Erro de digitação (Trocou 'u' por 'o')
    resultado1 = encontrar_palavra_proxima("computador", lista_cadastro)
    print(f"Encontrado: {resultado1}")  # Retorna: Computador

    # Teste 2: Letra a mais no final
    resultado2 = encontrar_palavra_proxima("celulare", lista_cadastro)
    print(f"Encontrado: {resultado2}")  # Retorna: Celular

    # Teste 3: Nenhuma correspondência
    resultado3 = encontrar_palavra_proxima("garrafa", lista_cadastro)
    print(f"Encontrado: {resultado3}")  # Retorna: None

    # --- Exemplo prático de uso ---

    # O seu dicionário com chaves de primeira ordem e listas de palavras
    meu_dicionario = {
        "Grupo A": ["computador", "teclado", "mouse"],
        "Grupo B": ["celular", "telefone", "computador"],  # 'computador' repetido aqui
        "Grupo C": ["caderno", "caneta", "computadorr"],   # variação com erro de digitação
        "Grupo D": ["garrafa", "copo"]
    }

    # Cenário 1: Buscando uma palavra que se repete e tem erro de digitação
    # Vamos buscar "computalor"
    resultado = mapear_chaves_da_palavra("computalor", meu_dicionario, tolerancia=0.8)

    print(f"A palavra foi encontrada nas chaves: {resultado}")
    # Deve retornar: ['Grupo A', 'Grupo B', 'Grupo C']
    # Nota: Pegou no Grupo C mesmo estando escrito 'computadorr' por causa da tolerância!

    # Cenário 2: Buscando algo que não existe
    resultado_vazio = mapear_chaves_da_palavra("abajur", meu_dicionario)
    print(f"A palavra foi encontrada nas chaves: {resultado_vazio}")
    # Retorna: []

    # --- Testando com os seus dados ---

    a = [
        ["Geração e Escrita de Textos ou Conteúdo", "(respostas automatizadas, manipulação de dados textuais)"],
        ["Análise ou Visualização de Dados", "(estruturação e encaminhamento de informações entre plataformas)"],
        ["Produtividade e Organização", "(automação de fluxos de trabalho, integração de aplicativos)"],
        ["Educação, Tutoria e Estudo Assistido", "(automatização de processos de ensino/aprendizagem)"]
    ]

    # Teste 1: Erro bobo no título da primeira linha
    # "Geração e Escrita de Textos" -> Escrevi "Geracao e Escrita de Testos"
    print(verificar_inedito("Geracao e Escrita de Testos", a))  
    # Retorna: False (porque detectou a proximidade e barrou)

    # Teste 2: Buscando algo próximo à descrição da terceira linha
    # "(automação de fluxos de trabalho...)" -> Escrevi "automaçao de fluxo de trabalho"
    print(verificar_inedito("automaçao de fluxo de trabalho", a))  
    # Retorna: False (também detectou na descrição)

    # Teste 3: Uma string completamente nova
    print(verificar_inedito("Desenvolvimento de Antenas e Circuitos de Micro-ondas", a))  
    # Retorna: True (pode avançar, não tem nada parecido lá dentro)