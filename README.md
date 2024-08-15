### EN (pt-br version below)

# Room Reservation System - DevSecOps Sketch

## Project Overview

This project is a sketch for a DevSecOps project, focusing on implementing a secure room reservation system using Flask and SQLite. The application features user authentication, room reservations, and an admin interface for managing reservations.

## Project Structure

The project folder contains the following structure:
```
project_folder/
│
├── config.py
├── populate.py
├── README.md
├── requirements.txt
├── resetdb.py
├── run.py
│
├── app/
│ ├── init.py
│ ├── .env
│ ├── forms.py
│ ├── models.py
│ └── routes.py
│
│ ├── static/
│ │ ├── css/
│ │ │ └── styles.css
│ │ └── js/
│ │ └── script.js
│ │
│ └── templates/
│ ├── admin.html
│ ├── cancel.html
│ ├── edit_profile.html
│ ├── explore.html
│ ├── index.html
│ ├── list_reservations.html
│ ├── login.html
│ ├── main.base.html
│ ├── profile.html
│ ├── reserve.html
│ ├── reset_password.html
│ └── user_reservations.html
```

## File Descriptions

### Project Root Files

- **config.py**: Contains configuration settings for the Flask application, including database connections and other application settings.
- **populate.py**: Script to populate the database with initial data such as users, rooms, and reservations.
- **README.md**: This file, providing an overview and documentation for the project.
- **requirements.txt**: Lists the Python packages required to run the application.
- **resetdb.py**: Script to reset the database, deleting all existing data.
- **run.py**: Entry point for running the Flask application.

### `app` Folder

- **__init__.py**: Initializes the Flask application and sets up the application context.
- **.env**: Environment variables file for sensitive configuration like database URLs and secret keys.
- **forms.py**: Contains form classes for handling user input in the application.
- **models.py**: Defines the database models used in the application, such as User, Room, and Reservation.
- **routes.py**: Defines the routes and their associated view functions for handling user requests.

### `app/static` Folder

- **css/styles.css**: Contains the styling for the application, including dark mode adaptations and responsive design rules.
- **js/script.js**: Contains JavaScript functions for toggling dark mode, applying saved themes, and displaying messages.

### `app/templates` Folder

- **admin.html**: Admin interface for managing reservations and users.
- **cancel.html**: Page for canceling reservations.
- **edit_profile.html**: Page for users to edit their profile information.
- **explore.html**: Public page for exploring available rooms and reservations.
- **index.html**: Home page of the application.
- **list_reservations.html**: Lists all reservations.
- **login.html**: Login page for user authentication.
- **main.base.html**: Base template with common layout elements used by other templates.
- **profile.html**: User profile page.
- **reserve.html**: Page for reserving a room.
- **reset_password.html**: Page for resetting user passwords.
- **user_reservations.html**: Page showing the user's own reservations.

## Configuration and Setup

### Automated Project Generation

To quickly set up the project, you can use the `generate-project-automated.py` script located in the project folder. This script creates the necessary files and directories with the appropriate content. Run the script to automatically generate the project structure.

### Setup Virtual Environment

# Linux/Mac:
python -m venv venv
source venv/bin/activate

# Windows Command Prompt:
python -m venv venv
venv\Scripts\activate

# Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate


### Install Requirements
# Linux/Mac/Windows:
pip install -r requirements.txt

## Initialize and Migrate Database
# Linux/Mac/Windows:
flask db init
flask db migrate
flask db upgrade

### Run the Application
# Linux/Mac/Windows:
flask run

### Future Updates
- **Styling Issues:** Address the persistent white rectangle not adapting to dark mode and style the explore page to be visible to all users.
- **Functionality Enhancements:** Add more features and refine the existing functionality based on user feedback and requirements.
- **Error Handling:** Implement better error handling and user feedback mechanisms.

### Known Issues
- **White Rectangle in Dark Mode:** The white rectangle does not adapt to dark mode.
- **Explore Page Styling:** The explore page is not styled and is currently restricted to authenticated users.
- **Unresolved Functionalities:** Some functionalities might still be incomplete or need improvement.



### PT-BR

# Sistema de Reserva de Quarto - DevSecops Sketch

## Visão geral do projeto

Este projeto é um esboço para um projeto DevSeCops, com foco na implementação de um sistema de reserva de salas seguro usando o Flask e o SQLite.O aplicativo apresenta autenticação do usuário, reservas de salas e uma interface de administração para gerenciar reservas.

## Estrutura do projeto

A pasta do projeto contém a seguinte estrutura:
```
Project_folder/
│
├── config.py
├── preenchimento.py
├── readme.md
├── requisitos.txt
├── resetdb.py
├── run.py
│
├── App/
│ ├── init.py
│ ├── .env
│ ├── form.py
│ ├── Models.py
│ └── rotas.py
│ │
│ ├── estático/
│ │ ├── CSS/
│ │ │ └── Styles.csss
│ │ └── JS/
│ │ └── script.js
│ │
│ └── modelos/
│ ├── admin.html
│ ├── cancel.html
│ ├── edit_profile.html
│ ├sto Explore.html
│ ├── Index.html
│ ├── list_Reservations.html
│ ├── login.html
│ ├── main.base.html
│ ├── perfil.html
│ ├── Reserve.html
│ ├── reset_password.html
│ └── User_Reservations.html
```

## Descrições de arquivo

### Projeto Arquivos root

- ** Config.py **: Contém configurações de configuração para o aplicativo Flask, incluindo conexões de banco de dados e outras configurações de aplicativos.
- ** POPULE.PY **: Script para preencher o banco de dados com dados iniciais como usuários, salas e reservas.
- ** README.MD **: Este arquivo, fornecendo uma visão geral e documentação para o projeto.
- ** requisitos.txt **: lista os pacotes Python necessários para executar o aplicativo.
- ** RESETDB.PY **: Script para redefinir o banco de dados, excluindo todos os dados existentes.
- ** run.py **: ponto de entrada para executar o aplicativo Flask.

### `app` pasta

- ** __ init __. py **: inicializa o aplicativo de frasco e configura o contexto do aplicativo.
- **. Env **: Arquivo de variáveis ​​de ambiente para configuração sensível, como URLs de banco de dados e teclas secretas.
- ** form.py **: contém classes de formulário para lidar com a entrada do usuário no aplicativo.
- ** Models.py **: Define os modelos de banco de dados usados ​​no aplicativo, como usuário, sala e reserva.
- ** ROTES.PY **: Define as rotas e suas funções de visualização associadas para lidar com solicitações de usuário.

### `App/static` Pasta

- ** css/styles.css **: contém o estilo do aplicativo, incluindo adaptações do modo escuro e regras de design responsivo.
- ** js/script.js **: contém funções JavaScript para alternar o modo escuro, aplicar temas salvos e exibir mensagens.

Pasta#`App/modelos`

- ** Admin.html **: Interface de administração para gerenciar reservas e usuários.
- ** Cancel.html **: página para cancelamento de reservas.
- ** edit_profile.html **: Página para os usuários editarem suas informações de perfil.
- ** Explore.html **: página pública para explorar os quartos e reservas disponíveis.
- ** Index.html **: página inicial do aplicativo.
- ** LIST_RESERVATIONS.HTML **: Lista todas as reservas.
- ** Login.html **: página de login para autenticação do usuário.
- ** main.base.html **: modelo base com elementos de layout comuns usados ​​por outros modelos.
- ** perfil.html **: página de perfil do usuário.
- ** Reserve.html **: Página para reservar uma sala.
- ** Reset_password.html **: página para redefinir senhas de usuário.
- ** user_reservations.html **: página mostrando as próprias reservas do usuário.

## Configuração e configuração

### Geração automatizada de projeto

Para configurar rapidamente o projeto, você pode usar o script `Gereate-Project-Automated.`, localizado na pasta do projeto.Este script cria os arquivos e diretórios necessários com o conteúdo apropriado.Execute o script para gerar automaticamente a estrutura do projeto.

### Configurar o ambiente virtual

# Linux/Mac:
python -m venv venv
fonte VENV/BIN/ativação

# Prompt de comando windows:
python -m venv venv
venv \ scripts \ ativar

# Windows PowerShell:
python -m venv venv
. \ venv \ scripts \ ativar


### Instale requisitos
# Linux/Mac/Windows:
pip install -r requisitos.txt

## Inicialize e migre banco de dados
# Linux/Mac/Windows:
Flask DB init
Flask db migrar
Flask DB Upgrade

### Execute o aplicativo
# Linux/Mac/Windows:
Flask Run

### atualizações futuras
- ** Problemas de estilo: ** Area o retângulo branco persistente, não se adaptando ao modo escuro e estilize a página de exploração para ser visível a todos os usuários.
- ** Aprimoramentos da funcionalidade: ** Adicione mais recursos e refine a funcionalidade existente com base no feedback e requisitos do usuário.
- ** LIDADE DE ERRO: ** Implementar melhores mecanismos de manuseio de erros e feedback do usuário.

### problemas conhecidos
- ** Retângulo branco no modo escuro: ** O retângulo branco não se adapta ao modo escuro.
- ** Explore o estilo da página: ** A página Explore não é estilizada e atualmente está restrita a usuários autenticados.
- ** Funcionalidades não resolvidas: ** Algumas funcionalidades ainda podem estar incompletas ou precisar de melhorias.
