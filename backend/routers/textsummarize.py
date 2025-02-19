import os
from fastapi import UploadFile, File, HTTPException, APIRouter
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from pypdf import PdfReader
from io import BytesIO

load_dotenv()

router = APIRouter(prefix="/summarize", tags=["summarize"])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)

def read_pdf_file(file_contents: BytesIO):
    try:
        pdf_reader = PdfReader(file_contents)

        text=''
        for page in pdf_reader.pages :
            text += page.extract_text()

        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error readig PDF: {str(e)}')
    
@router.post('/')
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are allowed')
    
    try:
        contents = await file.read()
        file_contents = BytesIO(contents)
        text = read_pdf_file(file_contents)
        doc = [Document(page_content=text)]

        prompt = '''
        Write a concise summary of the following text delimited by triple bacquotes.
        Return your response in bullet points which covers the key points of the text
        ```{text}```
        BULLET POINT SUMMARY :
        '''

        prompt_template = PromptTemplate(template=prompt, input_variables=['text'])

        summary_chain = load_summarize_chain(
            llm = llm,
            chain_type='stuff',
            prompt=prompt_template
        )

        output = summary_chain.invoke(doc)
        return {'summary': output['output_text']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error processing file: {str(e)}')
