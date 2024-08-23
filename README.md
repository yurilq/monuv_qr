# Solução de Rastreamento de QR Codes Monuv

## 📖 Visão Geral

A **Solução de Rastreamento de QR Codes Monuv** é um sistema abrangente projetado para processar, armazenar e analisar leituras de QR Codes capturadas em salas de cinema. Utilizando serviços da AWS como API Gateway, Lambda, SQS, Glue, S3, Athena e CloudWatch, esta solução permite o processamento em tempo real e análises detalhadas dos dados de QR Codes para melhorar a eficiência operacional e a experiência do cliente.

## 🏗️ Estrutura do Projeto

```plaintext
monuv_qr_code_tracking_solution/
│
├── lambda_functions/
│   ├── monuv_qr_lambda.py
│   └── requirements.txt
│
├── glue_jobs/
│   ├── monuv_qr_glue_job.py
│   └── glue_job_script.py
│
├── cloudformation/
│   └── monuv_template.yaml
│
├── athena_queries/
│   └── monuv_hourly_peak_query.sql
│
├── monitoring/
│   └── monuv_create_alarm.py
│
├── scripts/
│   └── monuv_deploy.sh
│
├── api_gateway/
│   └── monuv_api_gateway_config.json
│
├── README.md
│
└── .gitignore
📂 Descrição dos Diretórios e Arquivos


lambda_functions/

monuv_qr_lambda.py: Função Lambda que processa as imagens recebidas do API Gateway, extrai os dados dos QR Codes e os envia para o Amazon SQS e para o servidor de controle de bilheteria.
requirements.txt: Lista as dependências Python necessárias para a função Lambda.
glue_jobs/

monuv_qr_glue_job.py: Script de ETL do AWS Glue que processa os dados armazenados na fila SQS, agregando e transformando as informações dos QR Codes, e salva os dados processados no Amazon S3 em formato Parquet.
glue_job_script.py: Script auxiliar para transformações adicionais conforme necessário.
cloudformation/

monuv_template.yaml: Template AWS CloudFormation para provisionar toda a infraestrutura AWS necessária para a solução.
athena_queries/

monuv_hourly_peak_query.sql: Consulta SQL para o Amazon Athena que analisa os dados armazenados no Amazon S3, identificando os horários de pico das operações de leitura dos QR Codes.
monitoring/

monuv_create_alarm.py: Script para criar alarmes no Amazon CloudWatch, que monitoram o desempenho da função Lambda e notificam em caso de erros.
scripts/

monuv_deploy.sh: Script Bash para automatizar o processo de deployment, incluindo o upload do código para o S3 e a implantação dos recursos via CloudFormation.
api_gateway/

monuv_api_gateway_config.json: Arquivo de configuração JSON para o API Gateway, definindo os endpoints, métodos HTTP e integrações com a função Lambda para recepção das imagens das câmeras.
README.md: Este documento. Fornece uma visão geral do projeto, instruções de instalação, uso e detalhes sobre a arquitetura e os componentes da solução.

.gitignore: Especifica os arquivos e diretórios que devem ser ignorados pelo Git.

LICENSE: Arquivo de licença que define os termos sob os quais o código do projeto pode ser utilizado, distribuído ou modificado.

⚙️ Pré-requisitos
Antes de implantar e executar a Solução de Rastreamento de QR Codes Monuv, certifique-se de ter o seguinte:

Conta AWS: Uma conta AWS ativa com permissões apropriadas para criar e gerenciar serviços da AWS.
AWS CLI: Instalado e configurado com credenciais para acessar sua conta AWS.
Python 3.9+: Instalado em sua máquina local para executar scripts e gerenciar dependências.
Boto3: AWS SDK para Python instalado (pip install boto3).
AWS SAM CLI (opcional): Para testes locais e deploy.
🚀 Guia de Deploy
Siga estes passos para implantar a Solução de Rastreamento de QR Codes Monuv:

1. Clonar o Repositório
bash
Copiar código
git clone https://github.com/monuv/monuv_qr_code_tracking_solution.git
cd monuv_qr_code_tracking_solution
2. Instalar Dependências da Função Lambda
Navegue até o diretório lambda_functions e instale os pacotes necessários:

bash
Copiar código
cd lambda_functions
pip install -r requirements.txt -t ./package
Este comando instala todas as dependências em um diretório local package, que será compactado e enviado para o AWS Lambda.

3. Empacotar e Enviar a Função Lambda
bash
Copiar código
cd package
zip -r ../monuv_qr_lambda.zip .
cd ..
zip monuv_qr_lambda.zip monuv_qr_lambda.py
aws s3 cp monuv_qr_lambda.zip s3://monuv-code-bucket/monuv-qr-lambda.zip
Substitua monuv-code-bucket pelo nome real do bucket S3 designado para armazenar os pacotes de código da Lambda.

4. Implantar Recursos AWS via CloudFormation
Execute o script de deployment para configurar todos os recursos AWS necessários:

bash
Copiar código
bash scripts/monuv_deploy.sh
Este script realiza as seguintes ações:

Envia o pacote de código Lambda para o S3.
Implanta o stack AWS CloudFormation conforme definido em cloudformation/monuv_template.yaml.
Nota: Certifique-se de ter as permissões IAM corretas para criar e gerenciar recursos AWS.

5. Configurar o API Gateway
Implemente a configuração do API Gateway:

Navegue até o console Amazon API Gateway.
Crie uma nova API REST e importe a definição de api_gateway/monuv_api_gateway_config.json.
Implante a API para um stage (por exemplo, prod).
Isso configurará o endpoint /upload, que acionará a função Lambda ao receber dados de imagem.

6. Executar o Glue Job
Após configurar e começar a receber dados no SQS, execute o AWS Glue job para processar e armazenar os dados:

Acesse o console AWS Glue.
Crie um novo job utilizando o script de glue_jobs/monuv_qr_glue_job.py.
Configure o job com a função IAM apropriada e conexões.
Execute o job manualmente ou agende conforme necessário.
7. Consultar Dados Processados com Amazon Athena
Utilize o Amazon Athena para realizar consultas nos dados processados armazenados no S3:

Acesse o console Amazon Athena.
Configure um banco de dados e tabela apontando para a localização no S3 com os dados processados.
Execute consultas como a fornecida em athena_queries/monuv_hourly_peak_query.sql para obter insights.
8. Configurar Monitoramento e Alertas
Configure alarmes no CloudWatch para monitorar o desempenho do sistema e erros:

bash
Copiar código
python monitoring/monuv_create_alarm.py
Este script cria alarmes que notificam via SNS quando certos limites são ultrapassados, garantindo o monitoramento proativo do sistema.

🧪 Testes
Para testar a solução:

Teste da API: Use ferramentas como Postman para enviar requisições HTTP POST para o endpoint /upload com imagens codificadas em base64.
Função Lambda: Verifique os logs do AWS CloudWatch para garantir que a função Lambda processa as imagens corretamente e envia mensagens para o SQS.
Glue Job: Verifique se o Glue job processa as mensagens do SQS e grava os dados corretos no S3.
Consultas no Athena: Execute consultas e valide que os resultados correspondem aos resultados esperados com base nos dados de teste.
Monitoramento: Provoque cenários de erro para garantir que os alarmes do CloudWatch e notificações do SNS funcionam conforme o esperado.
💰 Estimativa de Custos
Os custos associados à execução desta solução dependem dos padrões de uso e do volume de dados. Para estimar os custos:

Utilize a Calculadora de Preços AWS e insira as métricas de uso esperadas para cada serviço:
Lambda: Número de requisições, tempo de execução, alocação de memória.
SQS: Número de mensagens enviadas e recebidas.
Glue: Número de DPUs usados e duração do job.
S3: Tamanho do armazenamento de dados e frequência de acesso.
Athena: Quantidade de dados varridos por consulta.
API Gateway: Número de chamadas de API.
CloudWatch: Número de métricas monitoradas e logs armazenados.
Monitore regularmente a fatura da AWS para acompanhar os custos reais e ajustar o uso dos recursos conforme necessário.
