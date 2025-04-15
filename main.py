from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "https://dev.d31rmunseydxdz.amplifyapp.com",  # ← これを追加！
    "http://localhost:5173"  # 開発中のローカルVue用（任意）
]

# CORS（Vueと通信するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET = os.getenv("BUCKET_NAME")

@app.get("/presigned-url")
def get_presigned_url(filename: str):
    key = f"pre-sign-create-data/DispItemData/DispItem/TypeA/StrImg/other/{filename}"
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET,
            'Key': key,
            'ContentType': 'image/png'
        },
        ExpiresIn=300
    )
    return {"url": url}
