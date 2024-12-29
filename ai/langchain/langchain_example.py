from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType

# Инициализация модели
llm = OpenAI(temperature=0.7)

# Пример 1: Простая цепочка с промптом
template = """
Ты - эксперт по Python. Объясни концепцию {concept} простыми словами.
Приведи короткий пример кода.
"""

prompt = PromptTemplate(
    input_variables=["concept"],
    template=template
)

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# Использование цепочки
response = chain.run(concept="декораторы в Python")

# Пример 2: Агент с инструментами
tools = load_tools(["wikipedia", "python_repl", "terminal"], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Использование агента
result = agent.run(
    "Найди информацию о фреймворке FastAPI и создай простой пример Hello World"
)

# Пример 3: Чат-бот с памятью
chat_template = """
История беседы:
{chat_history}

Человек: {human_input}
Ассистент:"""

chat_prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=chat_template
)

memory = ConversationBufferMemory(memory_key="chat_history")

chat_chain = LLMChain(
    llm=llm,
    prompt=chat_prompt,
    memory=memory
)

# Использование чат-бота
response1 = chat_chain.predict(human_input="Привет! Расскажи о себе.")
response2 = chat_chain.predict(human_input="Какие у тебя есть возможности?")