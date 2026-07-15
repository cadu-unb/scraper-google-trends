# Como criar loops no n8n

## Loop por agenda

Use quando quiser rodar uma automação de tempos em tempos.

Fluxo simples:

1. Adicione um node `Schedule Trigger`.
2. Configure o intervalo desejado.
3. Adicione um node `Execute Command`.
4. Conecte o `Schedule Trigger` ao `Execute Command`.
5. Coloque o comando que deve rodar.

Exemplo de comando para testar Python:

```bash
python3 --version
```

## Loop para uma lista de itens

Use quando o workflow recebe vários itens e precisa processar um por vez.

Fluxo comum:

1. Um node gera ou recebe uma lista.
2. Um node de divisão/processamento separa os itens.
3. O workflow executa a ação para cada item.
4. O resultado segue para o próximo node.

Não foi identificado automaticamente um workflow exportado neste repositório. Por isso, os nomes exatos dos nodes de iteração devem ser escolhidos dentro da interface do n8n conforme a versão instalada.

## Loop com comando Python

Quando o loop precisa chamar um script Python, use `Execute Command`.

Modelo:

```bash
cd /workspace/1_src && python3 -m nome_do_modulo
```

Para o keyword research:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

## Node para registrar cada execução em JSON

Depois do node que roda o `main.py`, adicione mais um node `Execute Command`.

Conecte assim:

```text
Schedule Trigger -> Execute Command: keyword research -> Execute Command: registrar execução
```

No segundo `Execute Command`, cole:

```bash
python3 /scripts/register_keyword_research_run.py --status success --note "Loop keyword research executado pelo n8n"
```

Esse comando grava o histórico em:

```text
1_src/keyword_research_app/data/n8n_execution_log.json
```

Dentro do container, o mesmo arquivo fica em:

```text
/workspace/1_src/keyword_research_app/data/n8n_execution_log.json
```

O JSON terá uma lista chamada `runs`. Cada item registra:

- data e hora da execução;
- status;
- observação;
- fonte do relatório;
- quantidade de palavras-chave;
- caminho do relatório gerado.

Exemplo simplificado:

```json
{
  "runs": [
    {
      "executed_at": "2026-07-14T18:30:00+00:00",
      "status": "success",
      "note": "Loop keyword research executado pelo n8n",
      "source": "GOOGLE_TRENDS",
      "total_keywords": 10
    }
  ],
  "total_runs": 1
}
```

Importante: esse segundo node só roda se o node anterior terminar com sucesso.
Para registrar falhas também, configure tratamento de erro no workflow ou ative
continuação em caso de falha no node do keyword research.

## Cuidados com loops

Loops podem disparar muitas requisições rapidamente.

Para Google Trends, prefira:

- intervalos maiores entre execuções;
- listas menores de palavras-chave;
- cache preservado com `GOOGLE_TRENDS_NEW_QUERY=false`;
- execução manual para testes.

Evite rodar `GOOGLE_TRENDS_NEW_QUERY=true` em loops muito frequentes, porque isso apaga o cache e força novas consultas.
