# PORTFOLIO: A DATA WAREHOUSE

My portfolio project on Data Warehouse based on Postgres, MongoDB, Django as API builder, Apache Airflow, and Apache Kafka.

# SOURCES

[DJANGO] Django Documentation Website: https://www.djangoproject.com/
[DJANGO-PACKAGES] Django Packages Website: https://djangopackages.org/
[DJANGO-REST-FRAMEWORK] Django-Rest-Framework Website: https://www.django-rest-framework.org/
[EBOOK] KIMBALL, RAUPH; 2020. The Definitive Guide to Dimensional Modeling.
[END-POINT] Payment CSV FIle: https://docs.google.com/spreadsheets/d/1j_2LLIoJqO3B0eqMjhBFwWldFDiXWrcdxM7vArM0oQw/edit?usp=sharing
[END-POINT] Plan CSV FIle:
[END-POINT] GET Customer API: https://demo4461965.mockable.io/clientes

# INSTALLATION & SETUP

Clone the codes on GitHub:

    $ git clone <>

Download the files and put them at /lake/raw.

Run the application:

    $ docker-compose up

# TEST DOCUMENTATION

● Como será a ingestão desses dados?

Um sistema em engenharia de dados deve fazer a ingestão automática de um conjunto amplo de tipos de dados e fontes. Dessa maneira, ele torna-se escalável (objetivo primário de qualquer sistema informacional). Tecnologias como processamento de dados em data lakes, etl ou elt design patterns, monitoramento e análise dos dados, e robôs com inteligência artificial devem ser adicionadas para melhor processar e extrair valor dos dados gerados.

A ideia inicial seria fazer o download dos dados nas fontes (html, csv e json), salvá-los na camada de dados brutos em um data lake, e processá-los em camadas subsequentes até o seu carregamento no banco de dados relacional.

Contudo, não tive tempo hábil de implementar uma das soluções para o download automatizado dos arquivos em spreadsheet no Google Sheets:
- uso de soluções de terceiros em Python (https://stackoverflow.com/questions/3287651/download-a-spreadsheet-from-google-docs-using-python),
- automação web via selenium,
- processamento do resultado de requisição web no format html para extração dos dados contidos no html.

Sendo assim, a ingestão dos arquivos no Google Sheet (csv), o download seria feito manualmente. Isso não está correto e seria resolvido imediatamente.

● Qual será a frequência de atualização?

O conjunto de dados são simples, contudo, o objetivo do teste seria fornecer esses dados para todos os setores de uma organização. Como cada setor dentro de uma organização tem demandas em contextos e tempos diferentes, estruturei o sistema de processamento de dados conforme uma arquitetura de dados em padrão lambda.

Sendo assim, cada layer teria tempo diferentes:
- batch layer teria frequência diária (1 dia)
- speed layer teria frequência horaria ou menor (>=1h)

● Como lidar com possíveis erros?

Nenhum sistema em tecnologia informacional está imune a erros. Uma série de ações devem ser tomadas à fim de garantir boa capacidade e qualidade nesse processo de extração, transformação, carregamento e gestão dos dados.

Algumas ações:
- uso sistemático de metodologia em desenvolvimento orientadas à testes como TDD
- uso de metodologias agéis e continuo desenvolvimento
- um bom logging e um sistema de monitoramento bem feito apontariam os principais erros a serem tratados via gestão de exceções, melhorias e demanda de novas funcionalidades (uso de princípio de pareto)
- uso de crawler e inteligências artificiais que mapeassem os padrões nos dados e identificassem possíveis erros.

● Qual será a disposição das tabelas? Elas são otimizadas?

Seguindo o objetivo do teste de uso desses dados pelos mais diversos setores de uma organização, adotei a melhor abordagem em modelagem de dados nesse intuito: modelo fato-dimensão. Esta modelagem permite o contínuo desenvolvimento e manutenção dos dados, além de ser orientado ao modelo de negócio da organização e escalável para abranger novas demandas de todos os setores. Outra vantagem é a simplificação do processo de requisição via SQL (DQL).

A disposição seria uma tabela contendo o fato e tabelas relacionadas com as informações acerca das dimensões:
- O fato são os pagamentos: nesse caso, o problema foi simplificado. Uma empresa agrega valor, vende algo e recebe pagamentos. Aqui, deve-se analisar o modelo de negócio da empresa.
- As dimensões são cliente, tempo, modalidade (plano): nesse caso, três tabelas contento as dimensões teriam todas as informações pertinentes às demandas dos setores sobre o objtivo (o fato que é os pagamentos).

Obs: as dimensões são aspectos sobre os fatos que são importantes e devem ser monitorados.

● Há algum tipo de backup?

Sim, todo banco de dados tem que ter redundância, disponibilidade, eficiência e um backup. Hoje, os custos para se manter backups em empresas de cloud computing estão muito baixos. No AWS, o AWS Glacier é uma ótima solução, bons custos, e altamente integrável.

● Caso seja necessário fazer alterações nas transformações ou ingestão de dados, qual será o impacto na estrutura em produção? Como minimizá-lo?

Infelizmente, o modelo está fraco nesse sentido na parte de ingestão e transformações, pois o processamento está específico e pouco abrangente. Adaptações seriam necessária. Contudo, o modelo está bem escalável e dinâmico na adesão, modificação, retirada de dados no banco de dados.

Como já foi dito, o objetivo principal sempre é criar soluções abrangentes, escaláveis e inteligentes. Poderia-se minimizar tais efeitos de possíveis alterações com:
- adição de mais etapas ou camadas de processamento no data lake,
- contínuo desenvolvimento e monitoramento,
- busca de maior abrangência com análise de dados e melhorias nos métodos automatizados,
- uso de processamento de dados via inteligência artificial.

## Arquitetura

O Data Warehouse foi estruturado seguindo uma arquitetura lambda e modelagem de dados via paradigma fato-dimensão.

# Testes automatizados

Não foram elaborados testes automatizados ainda. Contudo, o uso do framework Django, que usa o pytest, tornaria esse processo bem mais simples e dinâmico. O framework Django possui uma ótima solução em testes automatizados.

# QUICK STARTED

Not available yet.

# DEVELOPER GUIDE

Not available yet.

# USER GUIDE

Not available yet.

