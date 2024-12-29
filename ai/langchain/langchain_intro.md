# LangChain: Краткое введение

## Что такое LangChain?

LangChain - это фреймворк для разработки приложений на базе языковых моделей (LLM). Он позволяет создавать сложные приложения, комбинируя LLM с другими источниками данных и вычислений.

## Основные компоненты

### 1. Модели (Models)
- LLMs (GPT-4, Claude, Llama)
- Chat Models
- Text Embedding Models

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Инициализация модели
llm = OpenAI(temperature=0.7)
chat_model = ChatOpenAI(model="gpt-4")

# Простой запрос
response = llm.predict("Что такое Python?")
```

### 2. Промпты (Prompts)
- Шаблоны промптов
- Пример структуры промпта:

```python
from langchain.prompts import PromptTemplate

template = """
Ответь на вопрос {question} как {role}.
Используй следующий контекст: {context}
"""

prompt = PromptTemplate(
    input_variables=["question", "role", "context"],
    template=template
)

# Использование промпта
formatted_prompt = prompt.format(
    question="Что такое Docker?",
    role="опытный DevOps инженер",
    context="Docker - это платформа контейнеризации"
)
```

### 3. Цепочки (Chains)
Цепочки объединяют несколько компонентов в последовательность операций.

```python
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain

# Создание простой цепочки
chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# Последовательная цепочка
chain1 = LLMChain(llm=llm, prompt=prompt1)
chain2 = LLMChain(llm=llm, prompt=prompt2)
overall_chain = SimpleSequentialChain(chains=[chain1, chain2])
```

### 4. Агенты (Agents)
Агенты могут использовать инструменты и принимать решения о следующих действиях.

```python
from langchain.agents import load_tools
from langchain.agents import initialize_agent

# Загрузка инструментов
tools = load_tools(["wikipedia", "llm-math"], llm=llm)

# Инициализация агента
agent = initialize_agent(
    tools, 
    llm, 
    agent="zero-shot-react-description",
    verbose=True
)

# Использование агента
agent.run("Найди информацию о Python и посчитай, сколько лет прошло с его создания")
```

### 5. Память (Memory)
Позволяет сохранять состояние между запросами.

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)
```

## Простой пример приложения

Создадим простого ассистента для ответов на вопросы с контекстом:

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

# Инициализация модели
chat = ChatOpenAI(model="gpt-4")

# Создание шаблона промпта
template = """
Ты - полезный ассистент. Используй предоставленный контекст для ответа на вопросы.

Предыдущая беседа:
{chat_history}

Контекст: {context}
Вопрос: {question}

Твой ответ:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template=template
)

# Создание памяти
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Создание цепочки
chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

# Использование
response = chain({
    "context": "Python был создан Гвидо ван Россумом в 1991 году.",
    "question": "Кто создал Python?"
})
```

## Основные варианты использования

1. **Чат-боты**
   - Разговорные интерфейсы
   - Поддержка клиентов
   - Виртуальные ассистенты

2. **Работа с документами**
   - Анализ текста
   - Извлечение информации
   - Генерация отчетов

3. **Агенты для автоматизации**
   - Автоматизация задач
   - Анализ данных
   - Работа с API

4. **Q&A системы**
   - Поиск по документации
   - База знаний
   - Обучающие системы

## Рекомендации по началу работы

1. Начните с простых цепочек
2. Используйте готовые промпты из LangChain Hub
3. Экспериментируйте с различными моделями
4. Добавляйте функционал постепенно
5. Используйте версионирование промптов