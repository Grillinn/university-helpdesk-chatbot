# C:\Users\91858\OneDrive\Desktop\University_Admission_Helpdesk\backend\main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import student, admin, chatbot  # Import your route modules

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing) to allow frontend to communicate with backend
origins = [
    "http://localhost",
    "http://localhost:3000",  # Default React port
    "http://localhost:8501",  # Default Streamlit port
    "*",  # Or specific origins you trust
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers from your route modules
app.include_router(student.router)
app.include_router(admin.router)
app.include_router(chatbot.router)

@app.get("/")
async def root():
    return {"message": "University Admission Helpdesk Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)