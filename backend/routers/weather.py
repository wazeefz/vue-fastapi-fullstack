import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables
load_dotenv()

# Initialize Router
router = APIRouter(prefix="/weather", tags=["Weather"])

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Define request model
class WeatherRequest(BaseModel):
    query: str = Field(description="User's request for weather information.")

# Define response model
class WeatherReport(BaseModel):
    city: str = Field(description="Name of the city")
    temperature: float = Field(description="Current temperature in Celsius")
    conditions: List[str] = Field(description="List of weather conditions")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in km/h")

# Initialize output parser
output_parser = JsonOutputParser(pydantic_object=WeatherReport)

# Define prompt
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a weather expert machine that can tell accurate real-time information to users on weather status. Provide current
            weather information in the specified JSON format. Make realistic estimations based on the season and location."""
        ),
        (
            "human",
            "{request} \n {format_instructions}"
        )
    ]
)

# Create processing chain
chain = chat_prompt | llm | output_parser

@router.post("/", response_model=WeatherReport)
async def get_weather(request: WeatherRequest):
    """
    Get weather information based on the user's query.

    - **query**: The weather-related question asked by the user.
    - Returns: A structured weather report including temperature, conditions, humidity, and wind speed.
    """
    try:
        response = chain.invoke(
            {
                "request": request.query,
                "format_instructions": output_parser.get_format_instructions()
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
