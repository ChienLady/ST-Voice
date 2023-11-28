from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["access-control-allow-origin"] = "*"
    return response

@app.post("/voice/v1/stt")
async def proxy(request: Request):
    # target_url = "domain"
    # async with httpx.AsyncClient() as client:
    #     response = await client.request(
    #         request.method, target_url + request.url.path, headers=dict(request.headers), data=await request.body()
    #     )
    # return StreamingResponse(content=response.content, status_code=response.status_code, headers=dict(response.headers))
    return {
        "text": "alo alo"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app)
    
