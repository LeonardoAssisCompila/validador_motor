<img width="1376" height="768" alt="image" src="https://github.com/user-attachments/assets/7ce854d7-555a-4200-a992-7736ff914740" />
Explicação do Diagrama
1️ Arquivo Principal – app.py

O arquivo app.py é o ponto de entrada da aplicação.
Ele apresenta 5 opções de execução:

Cadastro no Motor

Download (NFS-e)

Download (NF-e)

Download (CT-e)

Acesso ao Motor

Cada opção executa um fluxo específico através dos robôs localizados na pasta templates.

2️⃣ Pasta templates – Robôs de Navegação

Dentro da pasta templates, estão os robôs responsáveis pela navegação e execução das ações no sistema.

Os robôs são:

Cadastro no Motor

Download (NFS-e)

Download (NF-e)

Download (CT-e)

Acesso ao Motor

Cada robô encapsula uma responsabilidade específica dentro do fluxo de automação.

3️⃣ Estratégia e Arquitetura do Projeto

A ideia principal da estrutura é:

✅ Reutilizar classes e componentes ao máximo
✅ Evitar duplicação de código
✅ Manter o fluxo organizado e escalável

🔄 Fluxo padrão de execução:

Primeiro robô executado: Cadastro

Sempre iniciamos apagando o usuário anterior.

Segundo robô executado: Acesso ao Motor

Realiza o login no sistema.

Terceiro robô executado:

O robô selecionado no app.py

Exemplo: Download de NFS-e

🧹 Ao final da execução:

Os seguintes registros são removidos:

Usuário

Conta

Empresa

Isso garante que cada execução comece com um ambiente limpo.

4️⃣ Arquivo config_dados

O arquivo config_dados é responsável por armazenar os dados do usuário utilizado na automação.

Esses dados podem ser atualizados sempre que necessário.

5️⃣ Arquivo banco_mongo

O arquivo banco_mongo contém todas as funções relacionadas ao banco de dados, incluindo:

Ativação de serviços

Criação de registros

Exclusão de usuário

Exclusão de conta

Exclusão de empresa

Ele centraliza toda a lógica de persistência.

⚠️ Observação Importante

Em alguns casos, o processo de upload no sistema Motor Fiscal pode demorar mais do que o esperado.

🚨 Isso não significa que houve falha.
O processo pode continuar executando corretamente, apenas com maior tempo de resposta.

3) A ideia da estrtura desse projeto seria, aproveitar ao maximo cada classe e reutilizar cada robo quando o necessario. Para não duplicar codigos:
    - Como funciona sempre o primeiro robo que roda é o Cadastro pois sempre apagamos o usuario. Depois disso o Segundo Robo que roda e o de acesso. e por fim o terceiro robo que roda e aquele que selecionou na lista no app.py Exemplo robo de NFSe 
no final desse robo. Deletamos 
    - Usuario
    - Conta 
    - empresa 


4) no Arquivo config_dados, armagenamos od dados desse usuario que pode ser altualizado caso precise 

5) no arquivo banco_mongo temos todas as funcoes que serve tanto para ativar os serviços tanto para deletar os usuario 
** Informação importante as vezes para fazer uploard no motorfiscal demora muito, mas não anula a opçao que esta tudo funicionado 
