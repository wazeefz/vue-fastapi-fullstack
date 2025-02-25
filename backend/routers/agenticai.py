import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Database connection
DATABASE_URL_AIAGENT = 'postgresql://millaridzuan:Miso2706$@localhost/books_db'
engine = create_engine(DATABASE_URL_AIAGENT)

db = SQLDatabase.from_uri(DATABASE_URL_AIAGENT)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Initialize SQL Agent
sql_agent = create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True,
    max_iterations=5,
    allow_dangerous_code=False
)

# Define API Router
router = APIRouter(prefix="/agent-ai", tags=["agent-ai"])

# Define request model
class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_agent(request: QuestionRequest):
    """
    Endpoint to post a question and receive a response.
    """
    try:
        response = sql_agent.invoke(request.question)
        return {"question": request.question, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
