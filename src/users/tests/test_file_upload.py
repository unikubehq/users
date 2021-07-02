import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from users.tests.factories.users import UnikubeUserFactory


def get_image_content():
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="  # noqa
    )


class AvatarUploadTests(TestCase):
    def setUp(self):
        self.unikube_user = UnikubeUserFactory.create()

    def test_image_upload(self):
        url = reverse("user_avatar_image_upload", kwargs={"pk": self.unikube_user.pk})
        image = SimpleUploadedFile(name="avatar.jpg", content=get_image_content(), content_type="image/jpeg")
        post_data = {"avatar_image": image}
        response = self.client.post(url, data=post_data)
        self.assertEquals(response.status_code, 200)
        self.unikube_user.refresh_from_db()
        self.assertTrue(self.unikube_user.avatar_image)
