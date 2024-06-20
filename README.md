# Sistema Interno de Avaliações de Desempenho

## Requisitos para rodar o projeto

### Setup de ambiente:

- [Python 3.10+](https://www.python.org/downloads/)
- [Django 3.2+](https://docs.djangoproject.com/en/stable/releases/3.2/)
- [Poetry](https://python-poetry.org/)

### Como rodar na minha máquina?

1. Clone o projeto:
   ```bash
   git clone https://github.com/seu-usuario/seu-projeto.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd seu-projeto
   ```
3. Instale as dependências:
   ```bash
   poetry install
   ```
4. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```
5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```
6. Rode o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
7. Pronto 🎉

## Estrutura do projeto

### `app`

O app principal contém as configurações básicas do projeto.

- `asgi.py`: Configuração para ASGI.
- `settings.py`: Configurações globais do projeto Django.
- `urls.py`: Roteamento principal do projeto.
- `wsgi.py`: Configuração para WSGI.
- `templates/base.html`: Template base para herança nos outros templates.

### `accounts`

O app `accounts` gerencia todas as informações relacionadas a usuários e clientes.

- `models.py`: Modelos para Usuário, Departamento, Função e Cliente.
- `views.py`: Views para cadastro, edição e listagem de usuários e clientes.
- `forms.py`: Formulários para criação e edição de usuários e clientes.
- `urls.py`: Roteamento específico para as funcionalidades de usuários e clientes.
- `templates/accounts`:
  - `clients/add_client.html`: Template para adicionar um cliente.
  - `clients/edit_client.html`: Template para editar um cliente.
  - `clients/list_clients.html`: Template para listar clientes.
  - `users/add_user.html`: Template para adicionar um usuário.
  - `users/edit_user.html`: Template para editar um usuário.
  - `users/list_users.html`: Template para listar usuários.

### `assessments`

O app `assessments` gerencia todas as funcionalidades relacionadas às avaliações de desempenho.

- `models.py`: Modelos para Avaliações, Tipos de Avaliações, Agendamentos, Perguntas e Respostas.
- `views.py`: Views para criação, edição, listagem e consulta de avaliações.
- `forms.py`: Formulários para criação e edição de avaliações.
- `urls.py`: Roteamento específico para as funcionalidades de avaliações.
- `templates/assessments`:
  - `create_evaluation.html`: Template para criar uma avaliação.
  - `evaluation_detail.html`: Template para detalhes de uma avaliação.
  - `schedule_evaluation.html`: Template para agendar uma avaliação.
  - `view_evaluations.html`: Template para visualizar avaliações.
  - `view_scheduled_evaluations.html`: Template para visualizar avaliações agendadas.

## Decisões arquiteturais

- **Separação de responsabilidades**: A estrutura do projeto foi dividida em três principais aplicativos (`app`, `accounts`, `assessments`) para melhor modularização e organização do código.
- **Uso de templates**: Templates foram organizados em diretórios específicos para facilitar a manutenção e escalabilidade do projeto.
- **Formulários**: Uso de formulários do Django para gerenciamento de entradas de dados do usuário, garantindo validação e segurança.
