# AI Sales Assistant: Техническая спецификация

## Технологический стек

### Backend
- **Framework**: FastAPI
- **Python**: 3.11+
- **Основные библиотеки**:
  ```requirements.txt
  fastapi>=0.104.0
  uvicorn[standard]
  pydantic>=2.4
  python-jose[cryptography]  # JWT
  passlib[bcrypt]           # password hashing
  sqlalchemy>=2.0.0        # ORM
  alembic                  # миграции
  redis                    # кэширование
  celery                   # фоновые задачи
  langchain               # оркестрация LLM
  anything-llm            # RAG система
  ```

### Frontend
- **Framework**: Next.js 14+
- **UI Library**: React 18+
- **Основные зависимости**:
  ```package.json
  {
    "dependencies": {
      "next": "^14.0.0",
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "@tanstack/react-query": "^5.0.0",  // data fetching
      "tailwindcss": "^3.3.0",           // стили
      "@headlessui/react": "^1.7.0",     // UI компоненты
      "socket.io-client": "^4.7.0",      // real-time чат
      "zustand": "^4.4.0"                // state management
    }
  }
  ```

### RAG (AnythingLLM)
- **Конфигурация**:
  ```yaml
  vector_db: chroma        # векторная БД
  embedding_model: all-MiniLM-L6-v2  # модель для embeddings
  llm_provider: openai     # провайдер LLM
  collection_name: sales_knowledge  # коллекция для sales данных
  ```

- **Структура документов**:
  ```
  /knowledge_base
  ├── products/
  │   ├── catalog.md
  │   ├── pricing.md
  │   └── specifications.md
  ├── sales/
  │   ├── scripts.md
  │   ├── objections.md
  │   └── best_practices.md
  └── processes/
      ├── ordering.md
      ├── delivery.md
      └── support.md
  ```

### Task Management Интеграции

#### 1. Trello
```python
from trello import TrelloClient

class TrelloIntegration:
    def __init__(self, api_key: str, token: str):
        self.client = TrelloClient(
            api_key=api_key,
            token=token
        )
    
    async def create_lead_card(self, data: LeadData) -> str:
        board = self.client.get_board(SALES_BOARD_ID)
        lead_list = board.get_list(LEADS_LIST_ID)
        
        card = lead_list.add_card(
            name=f"Lead: {data.client_name}",
            desc=self._format_lead_description(data),
            labels=self._get_lead_labels(data.priority)
        )
        return card.id
```

#### 2. ClickUp
```python
from clickup_sdk import ClickUpClient

class ClickUpIntegration:
    def __init__(self, api_token: str):
        self.client = ClickUpClient(api_token)
    
    async def create_lead_task(self, data: LeadData) -> str:
        task = self.client.create_task(
            list_id=LEADS_LIST_ID,
            name=f"New Lead: {data.client_name}",
            description=self._format_lead_description(data),
            priority=self._map_priority(data.priority),
            custom_fields=self._prepare_custom_fields(data)
        )
        return task.id
```

#### 3. Shortcut
```python
from shortcut import ShortcutClient

class ShortcutIntegration:
    def __init__(self, api_token: str):
        self.client = ShortcutClient(api_token)
    
    async def create_lead_story(self, data: LeadData) -> str:
        story = self.client.create_story(
            project_id=SALES_PROJECT_ID,
            name=f"Lead: {data.client_name}",
            description=self._format_lead_description(data),
            story_type="feature",
            labels=[{"name": "lead", "color": "#3399ff"}]
        )
        return story.id
```

### Общий интерфейс для task-tracking систем
```python
from abc import ABC, abstractmethod
from enum import Enum

class TaskSystem(Enum):
    TRELLO = "trello"
    CLICKUP = "clickup"
    SHORTCUT = "shortcut"

class TaskManagementInterface(ABC):
    @abstractmethod
    async def create_lead(self, data: LeadData) -> str:
        pass
    
    @abstractmethod
    async def update_lead_status(self, lead_id: str, status: str) -> bool:
        pass
    
    @abstractmethod
    async def add_comment(self, lead_id: str, comment: str) -> bool:
        pass

class TaskManagementFactory:
    @staticmethod
    def get_integration(system: TaskSystem, config: dict) -> TaskManagementInterface:
        if system == TaskSystem.TRELLO:
            return TrelloIntegration(config["api_key"], config["token"])
        elif system == TaskSystem.CLICKUP:
            return ClickUpIntegration(config["api_token"])
        elif system == TaskSystem.SHORTCUT:
            return ShortcutIntegration(config["api_token"])
        raise ValueError(f"Unsupported task system: {system}")
```

## Архитектура приложения

### Backend структура
```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── chat.py
│   │   │   ├── leads.py
│   │   │   └── analytics.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── events.py
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   ├── integrations/
│   │   ├── task_management/
│   │   │   ├── base.py
│   │   │   ├── trello.py
│   │   │   ├── clickup.py
│   │   │   └── shortcut.py
│   │   └── llm/
│   │       ├── anything_llm.py
│   │       └── chat_manager.py
│   └── services/
│       ├── lead_service.py
│       └── chat_service.py
└── main.py
```

### Frontend структура
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── providers.tsx
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageInput.tsx
│   │   └── Message.tsx
│   ├── leads/
│   │   ├── LeadForm.tsx
│   │   └── LeadList.tsx
│   └── ui/
│       ├── Button.tsx
│       └── Input.tsx
├── lib/
│   ├── api.ts
│   ├── types.ts
│   └── utils.ts
└── styles/
    └── globals.css
```

## Интеграция AnythingLLM

### Инициализация и конфигурация
```python
from anything_llm import AnythingLLM
from langchain.chains import ConversationChain

class SalesAssistant:
    def __init__(self):
        self.llm = AnythingLLM(
            host="localhost",
            port=3001,
            collection="sales_knowledge"
        )
        
        self.conversation_chain = ConversationChain(
            llm=self.llm,
            memory=self.get_conversation_memory(),
            prompt=self.get_sales_prompt()
        )

    def get_sales_prompt(self):
        return """
        You are an experienced sales assistant. Use the following context 
        to help customers with their inquiries. Always be helpful and 
        professional, and try to move the conversation towards a sale 
        when appropriate.

        Context: {context}
        Current conversation: {history}
        Human: {input}
        Assistant:"""

    async def process_message(self, message: str, context: dict = None):
        # Получаем релевантный контекст из базы знаний
        relevant_docs = await self.llm.similarity_search(message)
        
        # Добавляем контекст в промпт
        response = await self.conversation_chain.predict(
            input=message,
            context=self._format_context(relevant_docs)
        )
        
        return response
```

### Обработка документации
```python
class KnowledgeBaseManager:
    def __init__(self, anything_llm_client):
        self.client = anything_llm_client

    async def upload_product_catalog(self, catalog_data: dict):
        """Загрузка и индексация каталога продуктов"""
        formatted_data = self._format_catalog(catalog_data)
        await self.client.add_documents(
            collection="products",
            documents=formatted_data
        )

    async def upload_sales_scripts(self, scripts_data: dict):
        """Загрузка скриптов продаж"""
        formatted_data = self._format_scripts(scripts_data)
        await self.client.add_documents(
            collection="sales_scripts",
            documents=formatted_data
        )

    def _format_catalog(self, catalog_data):
        # Форматирование каталога для индексации
        pass

    def _format_scripts(self, scripts_data):
        # Форматирование скриптов для индексации
        pass
```

## Рекомендации по развертыванию

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sales_bot
      - REDIS_URL=redis://redis:6379
      - ANYTHING_LLM_URL=http://anything-llm:3001
    depends_on:
      - db
      - redis
      - anything-llm

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  anything-llm:
    image: mintplexlabs/anything-llm
    ports:
      - "3001:3001"
    volumes:
      - ./knowledge_base:/app/documents
      - anything-llm-data:/app/data

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=sales_bot
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres-data:
  anything-llm-data:
```

### Мониторинг и логирование
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

# Инструментация FastAPI
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

# Логирование чат-взаимодействий
class ChatLogger:
    async def log_interaction(
        self,
        user_message: str,
        assistant_response: str,
        context_used: list,
        lead_data: dict = None
    ):
        log_entry = {
            "timestamp": datetime.utcnow(),
            "user_message": user_message,
            "assistant_response": assistant_response,
            "context_used": context_used,
            "lead_data": lead_data
        }
        await self.save_log(log_entry)
```

## Теги
#FastAPI #NextJS #AnythingLLM #RAG #Trello #ClickUp #Shortcut #SalesBot #Integration #TechnicalSpec #Architecture #AIAssistant #TaskManagement #ProjectManagement