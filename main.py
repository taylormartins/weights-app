from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

# Allow the frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://weights-app.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Weight API is running! Use the Vercel frontend to upload files."}

@app.post("/calculate")
async def calculate_volume(file: UploadFile = File(...)):
    content = await file.read()
    # Decode bytes to string and split into lines
    lines = content.decode("utf-8").strip().split('\n')
    
    total_volume = 0
    detailed_results = []

    for line in lines:
        try:
            # Expected format: weight, sets, reps
            w, s, r = map(float, line.split(','))
            line_volume = w * s * r
            total_volume += line_volume
            detailed_results.append({"weight": w, "sets": s, "reps": r, "volume": line_volume})
        except ValueError:
            continue # Skip lines that don't match the format

    return {
        "total_volume": total_volume,
        "exercises": detailed_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)