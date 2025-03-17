from django.test import TestCase

# # Create your tests here.
# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import Asset

# class AssetTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.asset = Asset.objects.create(
#             name="Test Asset",
#             description="Test Description",
#             created_at="2023-01-01"
#         )

#     def test_asset_list_view(self):
#         url = reverse('asset_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Asset")
