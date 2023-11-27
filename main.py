from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
import io
from fastapi.responses import FileResponse
import os
from random import randint
import uuid
from concurrent.futures import ThreadPoolExecutor
import asyncio
import subprocess
import base64


# create directory
import os.path
from os import path
if path.exists('/content/images') == False:
  os.mkdir('/content/images')

IMAGEDIR = "/content/images/"

if path.exists('/content/videos') == False:
  os.mkdir('/content/videos')

VIDEODIR = "/content/videos/"

app = FastAPI()

@app.get("/")
async def read_root():
  return {"status": "Api connected"}


@app.post("/upload/")
async def create_upload_file(file_sourse: UploadFile = File(...), file_traget: UploadFile = File(...), is_face_enhancer: bool = False):

    try:
        # Validate file type and get file_sourse image
        if not file_sourse.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Only JPEG or PNG files are allowed.")

        file_sourse.filename = f"{uuid.uuid4()}.jpg"
        contents = await file_sourse.read()

        file_path_sourse = os.path.join(IMAGEDIR, file_sourse.filename)
        # Save the file
        with open(os.path.join(IMAGEDIR, file_sourse.filename), "wb") as f:
            f.write(contents)

        # Validate file type and get file_traget image
        if not file_traget.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Only JPEG or PNG files are allowed.")

        file_traget.filename = f"{uuid.uuid4()}.jpg"
        contents = await file_traget.read()

        file_path_traget = os.path.join(IMAGEDIR, file_traget.filename)
        # Save the file
        with open(os.path.join(IMAGEDIR, file_traget.filename), "wb") as f:
            f.write(contents)

        # get output_path
        output_filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(IMAGEDIR, output_filename)

        # Run the image processing script asynchronously
        await process_image(file_path_sourse,file_path_traget,output_path,is_face_enhancer)
        with open(output_path, "rb") as f:
          encoded_image = base64.b64encode(f.read())

        return {"base64": encoded_image}
        # return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def process_image(file_path_sourse,file_path_traget,output_path,is_face_enhancer): # Replace with the actual path to the uploaded file
  cmd = [
    "python",
    "run.py",
    "--target",
    file_path_traget,
    "--source",
    file_path_sourse,
    "-o",
    output_path,
    "--execution-provider",
    "cuda",
    "--frame-processor",
    "face_swapper",
    "face_enhancer",
  ] if is_face_enhancer else [
    "python",
    "run.py",
    "--target",
    file_path_traget,
    "--source",
    file_path_sourse,
    "-o",
    output_path,
    "--execution-provider",
    "cuda",
    "--frame-processor",
    "face_swapper",
  ]
  try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("Command executed successfully:")
    print("Output:", result.stdout)
  except subprocess.CalledProcessError as e:
    print("Error executing command:")
    print("Return code:", e.returncode)
    print("Error output:", e.stderr)

    # try:
    #     # Execute the image processing script asynchronously
    #     cmd = f"python /content/roop/run.py --target /content/bb.jpg --source {file_path} -o /content/swapped1.jpg --execution-provider cuda --frame-processor face_swapper"
    #     process = await asyncio.create_subprocess_shell(cmd, check=True)
    #     await process.communicate()
    # except Exception as e:
    #     # Handle errors during image processing
    #     raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


# video swap
@app.post("/video_swap/")
async def video_swap(file_sourse: UploadFile = File(...), file_traget: UploadFile = File(...), is_face_enhancer: bool = False):

    try:
        # Validate file type and get file_sourse image
        if not file_sourse.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Only JPEG or PNG files are allowed.")

        file_sourse.filename = f"{uuid.uuid4()}.jpg"
        contents = await file_sourse.read()

        file_path_sourse = os.path.join(IMAGEDIR, file_sourse.filename)
        # Save the file
        with open(os.path.join(IMAGEDIR, file_sourse.filename), "wb") as f:
            f.write(contents)

        # Validate file type and get file_traget video
        if not file_traget.filename.lower().endswith(('.mp4')):
            raise HTTPException(status_code=400, detail="Only mp4 files are allowed.")

        file_traget.filename = f"{uuid.uuid4()}.mp4"
        contents = await file_traget.read()

        file_path_traget = os.path.join(VIDEODIR, file_traget.filename)
        # Save the file
        with open(os.path.join(VIDEODIR, file_traget.filename), "wb") as f:
            f.write(contents)

        # get output_path
        output_filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(VIDEODIR, output_filename)

        # Run the image processing script asynchronously
        await process_video(file_path_sourse,file_path_traget,output_path,is_face_enhancer)
        with open(output_path, "rb") as f:
          encoded_image = base64.b64encode(f.read())

        return {"base64": encoded_image}
        # return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def process_video(file_path_sourse,file_path_traget,output_path, is_face_enhancer): # Replace with the actual path to the uploaded file

  cmd = [
    "python",
    "run.py",
    "--target",
    file_path_traget,
    "--source",
    file_path_sourse,
    "-o",
    output_path,
    "--execution-provider",
    "cuda",
    "--frame-processor",
    "face_swapper",
    "face_enhancer",
  ] if is_face_enhancer else [
    "python",
    "run.py",
    "--target",
    file_path_traget,
    "--source",
    file_path_sourse,
    "-o",
    output_path,
    "--execution-provider",
    "cuda",
    "--frame-processor",
    "face_swapper",
  ]
  try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("Command executed successfully:")
    print("Output:", result.stdout)
  except subprocess.CalledProcessError as e:
    print("Error executing command:")
    print("Return code:", e.returncode)
    print("Error output:", e.stderr)

    # try:
    #     # Execute the image processing script asynchronously
    #     cmd = f"python /content/roop/run.py --target /content/bb.jpg --source {file_path} -o /content/swapped1.jpg --execution-provider cuda --frame-processor face_swapper"
    #     process = await asyncio.create_subprocess_shell(cmd, check=True)
    #     await process.communicate()
    # except Exception as e:
    #     # Handle errors during image processing
    #     raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")





@app.get("/show/")
async def read_random_file():
    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)
    path = f"{IMAGEDIR}{files[random_index]}"
    return FileResponse(path)




from pyngrok import ngrok
# Create tunnel
public_url = ngrok.connect(8000)


import nest_asyncio
# Allow for asyncio to work within the Jupyter notebook cell
nest_asyncio.apply()


import uvicorn
# Run the FastAPI app using uvicorn
print(public_url)
uvicorn.run(app)
