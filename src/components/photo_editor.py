from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

class PhotoEditor:
    def __init__(self):
        """Initialize ImageKit with environment variables"""
        self.imagekit = ImageKit(
            private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT")
        )
    
    def transform_image(self, image_path, transformation_type):
        """Apply various image transformations"""
        transformations = {
            "blur": {"blur": "20"},
            "grayscale": {"effect_gray": "-"},
            "sepia": {"effect_sepia": "50"},
            "flip_horizontal": {"flip": "h"},
            "flip_vertical": {"flip": "v"}
        }
        
        try:
            with open(image_path, "rb") as file:
                upload = self.imagekit.upload_file(
                    file=file,
                    file_name=os.path.basename(image_path),
                    options=UploadFileRequestOptions(tags=[transformation_type])
                )
            
            if upload.url and transformation_type in transformations:
                transformed_url = self.imagekit.url({
                    "path": upload.file_path,
                    "transformation": [transformations[transformation_type]]
                })
                
                return transformed_url
            
            return None
        
        except Exception as e:
            print(f"Image transformation error: {str(e)}")
            return None
    
    def add_text_overlay(self, image_path, text):
        """Add text overlay to an image"""
        try:
            with open(image_path, "rb") as file:
                upload = self.imagekit.upload_file(
                    file=file,
                    file_name=os.path.basename(image_path),
                    options=UploadFileRequestOptions(tags=["text_overlay"])
                )
            
            if upload.url:
                text_overlay = {
                    "overlay_text": text,
                    "overlay_text_font_size": "30",
                    "overlay_text_color": "FFFFFF"
                }
                
                transformed_url = self.imagekit.url({
                    "path": upload.file_path,
                    "transformation": [text_overlay]
                })
                
                return transformed_url
            
            return None
        
        except Exception as e:
            print(f"Text overlay error: {str(e)}")
            return None