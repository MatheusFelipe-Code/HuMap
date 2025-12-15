# 🗺️ HuMap
> ⚠️ Este guia é para quem deseja rodar o projeto localmente.
> 
HuMap é um projeto que tem como objetivo principal criar um site que auxilie os cidadãos a se sentirem mais seguros ao circular pelas ruas de suas cidades, independentemente de localização, classe social, deficiência, raça, gênero, orientação sexual ou idade. O site funciona através de denúncias e mapeamento de áreas perigosas, considerando criminalidade e desastres naturais, oferecendo informações para que usuários possam evitar locais de risco.  

Inicialmente focado no estado de Pernambuco, o projeto visa futuramente expandir para todo o Brasil, contribuindo para a segurança de pedestres e motoristas.

<br>

## 📂 Estrutura do Projeto
```bash
HuMap/
├── Back-end/ → Django (API + renderização do feed)
└── Front-end/ → Arquivos estáticos (HTML, CSS, JS)
````



⚠️ **Importante:** Todo o ambiente Python (venv, requirements.txt, migrations, runserver) deve ser configurado dentro da pasta `Back-end`.

<br>
 

## ✅ Pré-requisitos

Antes de começar, tenha instalado na sua máquina:

- Python 3.10+
- Git
- Navegador atualizado

<br>

## 📥 Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
````

<br>


## 🐍 Criar e ativar o ambiente virtual (venv)
⚠️ Este passo deve ser feito dentro da pasta Back-end.

<br>

### 1️⃣ Navegar para a pasta Back-end
```bash
cd Back-end
````

### 2️⃣ Criar a venv

- Windows
```bash
python -m venv venv
````

- Linux / Mac
```bash
python3 -m venv venv
````

### 3️⃣ Ativar a venv

- Windows
```bash
venv\Scripts\activate
````

- Linux / Mac
```bash
source venv/bin/activate
````
💡 **Dica:** O prefixo `(venv)` no início da linha indica que você está usando o ambiente virtual corretamente.

<br>

## 📦 Instalar dependências
Ainda dentro da pasta Back-end e com a venv ativa:

```bash
pip install -r requirements.txt
````
> ✅ **O que isso faz:**  
> Este comando instala todas as dependências do projeto listadas no arquivo `requirements.txt`, garantindo que o ambiente virtual tenha todos os pacotes necessários para o HuMap rodar corretamente.


<br>

## 🗄️ Banco de dados (migrations)

### 1️⃣ Criar as migrations (se necessário)
```bash
python manage.py makemigrations
````

### 2️⃣ Aplicar as migrations
```bash
python manage.py migrate
````

<br>

## 🚀 Rodar o servidor
Após instalar as dependências e configurar o banco de dados, você já pode iniciar o servidor do Django:

```bash
python manage.py runserver
````
