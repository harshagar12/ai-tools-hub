import pytest
import os
from src.components.photo_editor import PhotoEditor

@pytest.fixture
def photo_editor():
    """Fixture for PhotoEditor instance"""
    return PhotoEditor()

def test_transform_image(photo_editor, tmp_path):
    """Test image transformation"""
    # Create a temporary image for testing
    test_image_path = tmp_path / "test_image.jpg"
    test_image = Image.new('RGB', (100, 100), color='red')
    test_image.save(test_image_path)
    
    transformed_url = photo_editor.transform_image(
        str(test_image_path), 
        "grayscale"
    )
    
    assert transformed_url is not None
    assert isinstance(transformed_url, str)

def test_text_overlay(photo_editor, tmp_path):
    """Test text overlay functionality"""
    test_image_path = tmp_path / "test_image.jpg"
    test_image = Image.new('RGB', (100, 100), color='blue')
    test_image.save(test_image_path)
    
    transformed_url = photo_editor.add_text_overlay(
        str(test_image_path), 
        "Test Overlay"
    )
    
    assert transformed_url is not None
    assert isinstance(transformed_url, str)