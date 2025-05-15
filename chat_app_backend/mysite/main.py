from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import os
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4
from groq import Groq


# Setting Up MongoDB connection
MONGODB_CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client.messagelist
message = db.messagess

# Setting up FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining the data models
class Message(BaseModel):
    user_message: str
    timestamp: str
    replied: bool = False

class MessageInDB(Message):
    id: UUID = Field(default_factory=uuid4)
    sentinment: str
    user_message: str
    bot_message: str = ""
    timestamp: str
    replied: bool = False

#Groq setup

llm_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

async def calculate_sentinment(user_message: str) -> str:

    chat_completion = llm_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Calculate the sentinment of the message in triple backticks. Please respond with float value between -1 and 1, where -1 is very sad or negetive, 0 is neutral, and 1 is very happy or positive. Do not include any other text in your response. Response example: 0.5.   ```{user_message}```",
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    response = chat_completion
    return response.choices[0].message.content


async def convert_message(mood:str ,user_message: str) -> str:
    chat_completion = llm_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Convert the following message to a more {mood} tone: ```{user_message}```. Please respond with the converted message only. Do not include any other text in your response. Try not to change the meaning of the message. Don't add new information. Respond with the converted message only.",
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    response = chat_completion
    return response.choices[0].message.content


# API Endpoints
@app.post("/messages", response_model=MessageInDB)
async def create_message(message: Message):
    message_data = message.model_dump()
    message_data["sentinment"] = await calculate_sentinment(message_data["user_message"])
    message_data["id"] = str(uuid4())
    message_data["replied"] = True
    result = await db.messagess.insert_one(message_data)
    created_message = await db.messagess.find_one({"_id": result.inserted_id})
    if created_message:
        return MessageInDB(**created_message)
    else:
        raise HTTPException(status_code=404, detail="Message not Created")


@app.get("/messages", response_model=list[MessageInDB])
async def get_messages():
    messages = []
    async for message in db.messagess.find():
        messages.append(MessageInDB(**message))
    return messages

@app.post("/messages/{mood}", response_model=MessageInDB)
async def create_message_mood(mood: str, message: Message):
    message_data = message.model_dump()
    message_data["replied"] = False
    message_data["sentinment"] = await calculate_sentinment(message_data["user_message"])
    message_data["id"] = str(uuid4())
    message_data["bot_message"] = await convert_message(mood, message_data["user_message"])
    message_data["replied"] = True
    result = await db.messagess.insert_one(message_data)
    created_message = await db.messagess.find_one({"_id": result.inserted_id})
    if created_message:
        return MessageInDB(**created_message)
    else:
        raise HTTPException(status_code=404, detail="Message not Created")
