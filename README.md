# FIAP - Faculdade de Informática e Administração Paulista
<br/>
<br/>
<p align="center">
<a href= "https://www.fiap.com.br/"><img src="public/imagens/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# SISTEMA A.T.M (Agricultural Transport Monitoring)

## Grupo 6

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/a1exlima/">Alex da Silva Lima</a>
- <a href="https://www.linkedin.com/in/johnatanloriano/">Johnatan Sousa Macedo Loriano</a>
- <a href="https://www.linkedin.com/in/matheus-maia-655bb1250/">Matheus Augusto Rodrigues Maia</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>


## 📜 Descrição

#### Introdução
O agronegócio é um dos pilares mais significativos da economia global, especialmente no Brasil, onde desempenha um papel crucial na geração de empregos e no desenvolvimento econômico. O projeto " Sistema A.T.M (Agricultural Transport Monitoring)" visa abordar os desafios enfrentados pelos pequenos e médios produtores rurais, focando na eficiência logística no setor de distribuição e consumo de produtos agrícolas. A proposta integra conceitos de tecnologia e inovação, utilizando Python para desenvolver um sistema de monitoramento dos produtos transportados que otimiza a distribuição. O objetivo é reduzir perdas no transporte, garantindo a qualidade dos produtos, a confiança dos consumidores e o aumento da lucratividade para pequenos e médios produtores, através da redução de perdas.

#### Gestão do Agronegócio em Python
O projeto se concentra nos capítulos 3 a 6, que exploram o uso de Python para resolver problemas específicos do agronegócio. A solução proposta envolve o desenvolvimento de um sistema que utiliza subalgoritmos, estruturas de dados, manipulação de arquivos e conexão com banco de dados para otimizar a logística dos produtos agrícolas no setor de distribuição e consumo.

#### Subalgoritmos e Estruturas de Dados
Os subalgoritmos são fundamentais para a implementação de funções e procedimentos que manipulam dados de transporte. Utilizando listas e dicionários, o sistema armazena e processa informações da cadeia de suprimentos, garantindo que cada etapa do transporte seja monitorada e registrada. Os dados de categorias e produtos são armazenados em arquivos JSON, permitindo fácil acesso e modificação, além de garantir a persistência das informações.

#### Manipulação de Arquivos e Conexão com Banco de Dados
A manipulação de arquivos no sistema é realizada utilizando dicionários e listas para armazenar dados temporários. Os logs de transporte são gerados em arquivos de texto, facilitando o monitoramento e auditoria das operações.
A conexão com o banco de dados é fundamental para armazenar e consultar dados críticos de forma segura e eficiente. A estrutura do banco de dados é definida por meio de tabelas para organizar as informações de produtos, origens, destinos e transportes.
Este sistema de banco de dados permite uma gestão eficiente e integrada das operações logísticas, assegurando que todas as etapas do transporte sejam registradas e monitoradas adequadamente. A estrutura relacional facilita a consulta e análise dos dados, promovendo a eficiência e segurança das informações armazenadas.

#### Solução Proposta e Inovação
A solução proposta pelo "Sistema A.T.M (Agricultural Transport Monitoring)" visa resolver os problemas de perdas e desperdícios durante o transporte de produtos agrícolas, melhorando a eficiência logística e acesso a mercados maiores. O uso de tecnologias, como subalgoritmos e manipulação de dados, promove a eficiência e competitividade dos pequenos e médios produtores. O sistema permite o monitoramento contínuo das condições de temperatura do transporte, comparando e analisando com os dados pré-cadastrados de cada produto agrícola e verificando se a temperatura monitorada no transporte está dentro dos limites mínimo e máximo. Isso é feito através de logs quando há desvios nas condições ideais, garantindo a qualidade dos produtos até o ponto de venda.

#### Resultados Esperados
Com a implementação do sistema, espera-se uma redução significativa nas perdas de produtos perecíveis, aumento da eficiência logística e melhoria na qualidade dos produtos no ponto de venda.

#### Conclusão
O projeto "Sistema A.T.M (Agricultural Transport Monitoring)" oferece uma abordagem abrangente para os desafios do agronegócio, utilizando Python para desenvolver um sistema de gestão eficiente e escalável no setor de distribuição e consumo. A solução proposta não só melhora a eficiência da cadeia de suprimentos, mas também aumenta a competitividade dos produtores locais. Ao integrar tecnologia e inovação, o projeto contribui para o desenvolvimento sustentável e econômico do setor agrícola, alinhando-se com as tendências globais de digitalização e automação.



## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>data</b>: Esta pasta contém o arquivo <i>lista_produtos_agro.json</i>, que armazena dados de categorias e produtos pré-cadastrados utilizados para o registro de transporte. Esses dados são essenciais para a correta operação e monitoramento do sistema.

- <b>models</b>: Contém os scripts Python (<i>.py</i>) responsáveis pelos subalgoritmos, procedimentos e funções que suportam a aplicação principal do projeto. 

- <b>public</b>: Armazena todos os arquivos públicos utilizados para a explicação e desenvolvimento do projeto, como imagens e materiais de referência. 

- <b>scripts</b>: Contém scripts auxiliares para tarefas específicas do projeto, como migração de banco de dados e diagramas de modelagem entidade-relacionamento.

- <b>.env.example</b>: Um arquivo de configuração de exemplo que serve como template para a inserção de dados sensíveis do projeto. Este arquivo é crucial para configurar o ambiente 
de execução de maneira segura.

- <b>.gitignore</b>: Arquivo de configuração do Git que especifica quais arquivos e pastas devem ser ignorados pelo controle de versão.

- <b>app.py</b>: O arquivo principal do projeto, onde está implementado o código base da aplicação em Python.

- <b>log_monitoramento_transporte.txt</b>: Arquivo de texto que registra todos os logs gerados pelo simulador de sensor de temperatura.

- <b>README.md</b>: Arquivo de documentação em formato Markdown que serve como guia e explicação geral sobre o projeto.

- <b>requirements.txt</b>: Lista todas as bibliotecas e dependências Python necessárias para a inicialização e funcionamento do projeto.


## 🔧 Como executar o código

*Acrescentar as informações necessárias sobre pré-requisitos (IDEs, serviços, bibliotecas etc.) e instalação básica do projeto, descrevendo eventuais versões utilizadas. Colocar um passo a passo de como o leitor pode baixar o seu código e executá-lo a partir de sua máquina ou seu repositório. Considere a explicação organizada em fase.*


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - XX/XX/2024
    *