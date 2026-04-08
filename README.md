# Estação Meteorológica IoT - Ponderada M05

Projeto final de monitoramento climático com integração entre Hardware (Arduino) e Software (Flask/SQLite).

## Como Executar
1. Instale as dependências: `pip install flask pyserial requests`
2. Conecte o Arduino na porta correspondente.
3. Execute o servidor: `python src/app.py`
4. Execute o leitor serial: `python src/serial_reader.py`
5. Acesse: `http://localhost:5000`

## Descrição das Rotas de API Rest
- **GET `/`**: Renderiza o Dashboard principal.
- **GET `/historico`**: Exibe a tabela com as leituras armazenadas no banco.
- **GET `/editar/<id>`**: Página de formulário para editar um registro específico.
- **POST `/leituras`**: Recebe o JSON do hardware e insere no banco de dados.
- **PUT `/leituras/<id>`**: Atualiza os dados de uma leitura.
- **DELETE `/leituras/<id>`**: Remove uma leitura.
- **GET `/api/estatisticas`**: Retorna as leituras em JSON para o gráfico.

### Obs: o arquivo requirements.txt é o que substitui a venv, é um arquivo de texto listando o que o usuário precisa instalar de dependências para rodar o projeto.
