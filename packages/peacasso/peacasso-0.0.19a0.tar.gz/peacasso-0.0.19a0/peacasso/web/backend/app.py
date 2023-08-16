import copy
from dataclasses import asdict
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from peacasso.generator import ImageGenerator
from fastapi.middleware.cors import CORSMiddleware
from peacasso.datamodel import ModelConfig, PreviewQuery, WebRequestData
from peacasso.utils import base64_to_pil, pil_to_base64, sanitize_config
import os
import traceback
import requests

logger = logging.getLogger("peacasso")

assert os.environ.get("HF_API_TOKEN") is not None, "HF_API_TOKEN not set"

# load model using env variables
model_config = ModelConfig(
    model=os.environ.get("PEACASSO_MODEL", "runwayml/stable-diffusion-v1-5"),
    revision=os.environ.get("PEACASSO_REVISION", "fp16"),
    device=os.environ.get("PEACASSO_DEVICE", "cuda:0"),
    token=os.environ.get("HF_API_TOKEN")
)
logger.info(
    ">> Loading Imagenerator pipeline with config. " + str(model_config))
generator = ImageGenerator(model_config)
logger.info(">> Imagenerator pipeline loaded.")

app = FastAPI()
# allow cross origin requests for testing on localhost: 800 * ports only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api = FastAPI(root_path="/api")
app.mount("/api", api)


root_file_path = os.path.dirname(os.path.abspath(__file__))
static_folder_root = os.path.join(root_file_path, "ui")
files_static_root = os.path.join(root_file_path, "files/")

os.makedirs(files_static_root, exist_ok=True)

# mount peacasso front end UI files
app.mount("/", StaticFiles(directory=static_folder_root, html=True), name="ui")
api.mount("/files", StaticFiles(directory=files_static_root, html=True), name="files")


@api.post("/generate")
def generate(request: WebRequestData) -> str:
    """Generate an image given some prompt"""

    # print("request received", request)

    result = None
    try:
        if request.type == "generate":
            prompt_config = request.config
            sanitized_config = asdict(sanitize_config(copy.deepcopy(prompt_config)))
            if prompt_config.init_image:
                prompt_config.init_image, _ = base64_to_pil(prompt_config.init_image)
            if prompt_config.mask_image:
                _, prompt_config.mask_image = base64_to_pil(prompt_config.mask_image)
            response = None
            try:
                result = generator.generate(prompt_config)
                images = []
                for image in result["images"]:  # convert pil image to base64 and prepend with data uri
                    images.append("data:image/png;base64, " + pil_to_base64(image))
                result["images"] = images
                response = {
                    "status": True,
                    "status_message": "success",
                    "config": sanitized_config,
                    "result": result}

            except Exception as e:
                traceback.print_exc()
                response = {
                    "status": False,
                    "status_message": str(e),
                    "config": sanitized_config,
                    "result": result}
            return response
        else:
            print("invalid request type")
            return {"status": False, "status_message": "invalid request type"}
    except Exception as e:
        traceback.print_exc()
        return {"status": False, "status_message": str(e)}


@api.post("/preview")
def preview(query: PreviewQuery) -> dict:
    """Generate preview of image given some prompt"""
    # fetch from url https://lexica.art/api/v1/search?q=query
    try:
        response = requests.get(
            "https://lexica.art/api/v1/search?q=" + query.prompt)
        if response.status_code == 200:
            data = response.json()

            return {"status": True, "status_message": "success", "result": data}

        else:
            return {"status": False,
                    "status_message": "error fetching preview image" + str(response.status_code)}
    except Exception as e:
        traceback.print_exc()
        return {"status": False, "status_message": str(e)}
