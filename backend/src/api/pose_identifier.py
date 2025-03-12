import logging
import os
import shutil
import json 
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from google import genai
from dotenv import load_dotenv
from common.constants import ALL_CONFIGS, GEMINI_API_KEY
from utils.logging import setup_logger
from prompts.pose_identifier import TEMPLATE
from data_models.pose_identification import PoseIdentificationResponse

import PIL.Image
load_dotenv()

logger = setup_logger(__name__)

router = APIRouter(prefix="/api", tags=["Pose Identifier"])

# Load the model settings
MODEL_SETTINGS = ALL_CONFIGS.get_config("all", "llm")

# Ensure the temporary directory exists
UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/identify-pose/")
async def identify_pose(file: UploadFile = File(...)):
    """
    Upload an image and ask Gemini to describe it.
    """
    try:
        # Check if the file is an image
        # if not file.content_type.startswith("image/"):
        #     raise HTTPException(status_code=400, detail="File must be an image")

        # Save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.debug("File Path: ")
        logger.debug(file_path)
            
        image = PIL.Image.open(file_path)
                
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[TEMPLATE, image],
            config={
                'response_mime_type': 'application/json',
                'response_schema': PoseIdentificationResponse
            }
        )
        
        logger.debug(response.text)
             
        try: 
            parsed_response = json.loads(response.text)
            logger.info(parsed_response)
            if not isinstance(parsed_response, dict):
              raise Exception("Response is not a dict")
            
        except Exception as e: 
            logger.error("Response is not valid JSON: " + str(e))
            return JSONResponse(content={"detail": "Unable to parse response from LLM" + str(e)})
        
                

        # Clean up the temporary file
        os.remove(file_path)

        # Return the response
        return JSONResponse(content=parsed_response)

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

