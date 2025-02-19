import os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WikipediaLoader

# Load environment variables
load_dotenv()

# Initialize Router
router = APIRouter(prefix="/document", tags=["document"])

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

loader = WikipediaLoader(query='Olympic Games', load_max_docs=1)
context_text = loader.load()[0].page_content

# Define prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'You are a helpful assistant',
        ),
        (
            "human",
    "Answer this question: \n {question} \n Here is some extra context: \n {context}"
        )
    ]
)

# Create processing chain
chain = prompt | llm 

@router.get("/")
async def get_document():
    try:
        response = chain.invoke(
            {
                "question": 'what is the origin of the modern olympic games?',
                "context": context_text
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
