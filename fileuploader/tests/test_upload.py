import unittest
from unittest.mock import MagicMock
from fileuploader.api.resources import ImageUpload
from fileuploader import create_app


class ImageUploadTest(unittest.TestCase):
    def setUp(self):
        # Create a Flask test client from the app created using create_app
        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_image_to_s3(self):
        # Mock the behavior of ImageUpload class
        ImageUpload.post = MagicMock(
            return_value={'message': 'Image uploaded successfully'})

        # Create a test image file
        with open('fileuploader/tests/test.png', 'rb') as image_file:
            data = {'image': (image_file, 'test_image.jpg')}
            response = self.app.post(
                '/api/upload', data=data, content_type='multipart/form-data')

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {'message': 'Image uploaded successfully'})
        pass
    def test_invalid_file_formar(self):
        ImageUpload.post = MagicMock(
            return_value={'message': 'Image uploaded successfully'})
        
        #use a file with invalid format
        with open('fileuploader/tests/test.txt', 'rb') as image_file:
            data = {'image': (image_file, 'test_image.txt')}
            response = self.app.post(
                '/api/upload', data=data, content_type='multipart/form-data')
    def test_inalid_image_content(self):
        ImageUpload.post = MagicMock(
            return_value={'message': 'Image uploaded successfully'})
        
        #use a file with invalid format
        with open ('fileuploader/tests/invalidtest.jpg', 'rb') as image_file:
            data = {'image': (image_file, 'test_image.png')}
            response = self.app.post(
                '/api/upload', data=data, content_type='multipart/form-data')
    
