Sistema Ubíquo para Monitorização Ambiental Inteligente

## Arquitetura do Sistema

### Visão Geral

O sistema adota uma arquitetura **Cliente-Servidor Modular**, com separação clara entre frontend e backend, facilitando a manutenção, escalabilidade e ubiquidade. O backend é construído com FastAPI (Python), o frontend com Angular, e a base de dados com MySQL. A comunicação em tempo real é realizada via WebSockets, garantindo acesso ubíquo em qualquer dispositivo com navegador web.

### Componentes Principais

- **Frontend (Angular)**: Interface responsiva para visualização de dados, gestão de sensores e alertas. Consome API REST e WebSockets para dados em tempo real.
- **Backend (FastAPI)**: API REST para operações CRUD, processamento de dados, lógica de alertas e simulação de sensores. Gerencia autenticação JWT.
- **Base de Dados (MySQL)**: Armazenamento persistente de usuários, sensores, medições e alertas.
- **Sensores Simulados**: Scripts Python que geram dados ambientais automaticamente (temperatura, humidade, qualidade do ar, ruído).
- **Deploy (Docker)**: Containerização para facilitar o deploy e isolamento de ambientes.

### Fluxo de Dados

1. **Coleta de Dados**: Sensores simulados enviam medições via WebSocket ou REST para o backend.
2. **Processamento**: Backend valida dados, armazena em MySQL, verifica limites para alertas.
3. **Distribuição**: Dados são enviados em tempo real para o frontend via WebSockets. Frontend exibe no dashboard.
4. **Acesso Ubíquo**: Usuários acessam via web responsiva em desktop, mobile ou qualquer dispositivo conectado.

### Diagrama Textual da Arquitetura

```
[Dispositivo Usuário] <--- HTTP/WebSocket ---> [Frontend Angular (SPA)]
                                      |
                                      | API REST / WebSocket
                                      v
[Backend FastAPI] <--- SQL ---> [MySQL Database]
                                      ^
                                      |
[Sensores Simulados] <--- WebSocket/REST ---> [Scheduler (APScheduler)]
```

### Justificativa para Ubiquity

- **Acesso em Qualquer Lugar**: Interface web responsiva acessível via navegador em qualquer dispositivo (desktop, mobile, tablet).
- **Contexto-Aware**: Alertas baseados em limites configuráveis, adaptáveis ao contexto ambiental.
- **Dispositivos Diversos**: Suporte a múltiplos sensores simulados, representando diferentes tipos de dispositivos IoT.

### Tecnologias e Padrões

- **Backend**: FastAPI para APIs assíncronas, SQLAlchemy para ORM, Pydantic para validação.
- **Frontend**: Angular com RxJS para reatividade, Chart.js para gráficos.
- **Segurança**: Autenticação JWT, validação de entrada.
- **Real-Time**: WebSockets para atualizações instantâneas.
- **Deploy**: Docker Compose para orquestração de containers (backend, frontend, MySQL).
