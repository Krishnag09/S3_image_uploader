import unittest
from unittest.mock import MagicMock
from resources import ImageUpload


class ImageUploadTest(unittest.TestCase):
    def setUp(self):
        self.app = ImageUpload.test_client()
        self.app.testing = True

    def test_upload_image_to_s3(self):
        # Create a test image file
        with open('test_image.jpg', 'rb') as image_file:
            data = {'image': (image_file, 'test_image.jpg')}
            response = self.app.post(
                '/api/upload', data=data, content_type='multipart/form-data')
        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Image uploaded successfully'})
        pass


if __name__ == '__main__':
    unittest.main()
