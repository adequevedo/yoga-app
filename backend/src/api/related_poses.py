import logging
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from utils.logging import setup_logger
import requests
from typing import List
from common.constants import SEARCH_ENGINE_URL, SEARCH_ENGINE_API_KEY, SEARCH_ENGINE_CX


load_dotenv()

logger = setup_logger(__name__)

router = APIRouter(prefix="/api", tags=["Related Poses"])

def get_image_urls(query: str) -> List[str]:
    """
    Queries the programmable search engine and returns a list of image URLs.

    Args:
        query: The search query (yoga pose name).

    Returns:
        A list of image URLs.
    """
    try:
        response = requests.get(
            SEARCH_ENGINE_URL, 
            params={
                "key": SEARCH_ENGINE_API_KEY,
                "q": query, 
                "exactTerms": "yoga",
                "cx": SEARCH_ENGINE_CX,
                "searchType": "image",
                "safe": "active"            
            }
        )
        response.raise_for_status()  
        
        search_results = response.json()
        return search_results["items"][0]["link"]
        

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during search request for '{query}': {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing search results for '{query}': {e}")
        raise


@router.post("/pose-images/")
async def pose_images(poses: List[str] = Body(...)):
    """
    Given a list of poses, return an image for each pose.

    Args:
        poses: A list of yoga pose names (strings).

    Returns:
        A JSON response containing a dictionary where keys are pose names and values are lists of image URLs.
    """
    try:
        if not poses:
            raise HTTPException(status_code=400, detail="Poses list cannot be empty.")
        
        logger.info("request for poses: " + str(poses))

        results = {}
        for pose in poses:
            try:
                image_url = get_image_urls(pose)
                results[pose] = image_url
            except Exception as e:
                logger.warning(f"Could not fetch image for pose '{pose}': {e}")
                results[pose] = [] 
            

        return JSONResponse(content=results)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error fetching image(s): {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching image(s): {e}")

