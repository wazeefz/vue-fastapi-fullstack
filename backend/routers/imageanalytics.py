import os, base64
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

router = APIRouter(prefix="/image-analytics", tags=["image-analytics"])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

def encode_image(image_content: bytes) -> str:
    return base64.b64encode(image_content).decode()
    
@router.post('/')
async def analyze_image(file: UploadFile = File(...)) -> Dict[str,str]:
    if file.content_type not in ['image/jpeg','image/png']:
        raise HTTPException(400, detail='invalid file type. Only JPEG and PNG are allowed.')
    if file.size > 5_000_000:
        raise HTTPException(400, detail='File is too large. Maximum size is 5MB.')
    try:
        contents = await file.read()
        image = encode_image(contents)

        prompt = ChatPromptTemplate.from_messages([
            ('system', '''You are a nutrition expert capable of analyzing food images
             and providing detailed nutritional advice.'''),
             ('human', [
                 """
                 """,
                 {
                     'type': 'image_url',
                     'image_url': {
                         'url': f'data:image/jpeg;base64,{image}',
                         'detail': 'high',
                     },
                 }
             ]),
        ])

        chain = prompt | llm
        res = await chain.ainvoke({})
        return {'analysis':res.content}
    except Exception as e:
        raise HTTPException(500, detail='An error occured while processing the image.')
