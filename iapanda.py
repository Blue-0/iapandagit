import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
from langchain_community.llms import Ollama 
import sqlite3
import os

llm = Ollama(model="llama3")

df = pd.read_excel('data.xlsx')
df = SmartDataframe(df, config={"llm": llm})

print( df.chat('combien il y a d'homme?'))
