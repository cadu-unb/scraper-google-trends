# Notas sobre APIs e fontes de dados

## Google Ads API

Google Ads API, por meio de recursos ligados ao Keyword Planner, e a fonte preferencial para metricas como:

- volume medio mensal;
- nivel de competicao;
- indice numerico de competicao;
- estimativas de lance no topo da pagina.

A integracao futura deve ser implementada em `integrations/google_ads_client.py`.

## Google Trends

Google Trends mostra interesse relativo ao longo do tempo. Ele ajuda a comparar tendencias, mas nao deve ser tratado como volume absoluto de buscas.

A estrutura inicial fica em `integrations/google_trends_client.py`.

## Limites de dados gratuitos

Fontes gratuitas ou sem autenticacao podem ter dados agregados, arredondados, incompletos ou indisponiveis por regiao. Por isso, a arquitetura separa fonte de dados, regras de negocio e exportacao.

## Bibliotecas nao oficiais

Bibliotecas como pytrends podem ser uteis para prototipos, mas nao sao APIs oficiais do Google. Se forem usadas futuramente, documente riscos, limites e possiveis quebras.

## Scraping direto do Google

Scraping direto deve ser evitado porque pode violar termos de uso, ser instavel e gerar bloqueios. Prefira APIs oficiais, dados exportados ou fontes autorizadas.
