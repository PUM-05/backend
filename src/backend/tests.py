import os
from pathlib import Path
import string
from django.test import TestCase
from api.models import Category


class APITests(TestCase):

    def setUp(self) -> None:
        """
        Creates static files for testing.
        """
        self.test_files = [
            "/test_file_1.txt",
            "/test_sub_dir/test_file_2.txt",
            "/test_sub_dir/test_sub_sub_dir/test_file_3.txt"
        ]

        for test_file in self.test_files:
            file_path = "src/static" + test_file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(test_file)

    def tearDown(self) -> None:
        """
        Deletes static files that were created for testing.
        """
        for test_file in self.test_files:
            file_path = "src/static" + test_file
            os.remove(file_path)

            # Delete empty directories
            folders = test_file.split("/")[1:-1]
            for index in range(len(folders), 0, -1):
                folder_path = "src/static/" + "/".join(folders[(index-1):])

                if os.path.isdir(folder_path) and not os.listdir(folder_path):
                    os.rmdir(folder_path)

    def test_get_root_file(self) -> None:
        """
        Tests that files in the root directory can be retrieved.
        """
        response = self.client.get(self.test_files[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), self.test_files[0])

    def test_get_sub_dir_file(self) -> None:
        """
        Tests that files in sub directories can be retrieved.
        """
        response = self.client.get(self.test_files[1])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), self.test_files[1])

        response = self.client.get(self.test_files[2])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), self.test_files[2])
