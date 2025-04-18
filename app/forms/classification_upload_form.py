# app/forms/classification_upload_form.py
from fastapi import Request, UploadFile
from typing import List
from starlette import datastructures

class ClassificationUploadForm:
    """Processes and validates image uploads for classification"""

    def __init__(self, request: Request):
        self.request = request
        self.errors: List[str] = []
        self.model_id: str = ""
        self.image: datastructures.UploadFile
        self.image_bytes: bytes

    async def load_data(self) -> None:
        form_data = await self.request.form()
        self.model_id = form_data.get("selected_model")
        self.image = form_data.get("uploaded_image")

        if self.image:
            try:
                self.image_bytes = await self.image.read()
            except Exception as e:
                self.errors.append(f"Error reading the image: {str(e)}")



    def is_valid(self) -> bool:
        # Model validation
        if not self.model_id:
            self.errors.append("Please select a model")

        # Image validation
        if not self.image or not isinstance(self.image, datastructures.UploadFile):
            self.errors.append("Upload a valid image. Is required")
        elif len(self.image_bytes) == 0:
            self.errors.append("Uploaded image is empty")

        return not self.errors