from fastapi import APIRouter, Depends, HTTPException, Header
from ..schemas import UrlSchema 
from ..models import Url
import os
import shortuuid 
from decouple import config

router = APIRouter()

@router.post('/', response_model = dict) 
async def test(url : UrlSchema):
    # convert pydantic schema object to python dict
    url = dict(url)

    # If a customCode is supplied, that will be the shortCode, else generate a random 
    #shortCode
    if (url["customCode"]):
        shortCode = url["customCode"]
    else:
        shortCode = shortuuid.ShortUUID().random(length = 8)

    # Generate short URL by joining BASE_URL to shortCode
    shortUrl = os.path.join(config("BASE_URL"), shortCode)

    # Raise an exception if a record in the database already uses that shortCode
    urlExists = Url.objects(shortCode = shortCode)
    if len(urlExists) != 0:
        raise HTTPException(status_code = 400, detail = "Short code is invalid, It has been used.")

    try:
        # Save the new Url object to the Mongo Atlas database
        url = Url(
            longUrl = url["longUrl"],
            shortCode = shortCode,
            shortUrl = shortUrl
        )

        url.save()

        return {
            "message" : "Successfully shortened URL.",
            "shortUrl" : shortUrl,
            "longUrl" : url["longUrl"]
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code = 500, detail = "An unknown error occurred.")
