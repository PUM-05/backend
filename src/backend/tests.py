import os
import shutil
from django.test import TestCase


class EnvironmentManager():
    STATIC_PATH = "src/static"
    CACHED_PATH = "src/cached_static"

    def __init__(self):
        self.cached_env = False
        self.test_env_active = False

    def setup_test_environment(self) -> None:
        """
        Moves the current static directory to a cached directory.
        """
        if os.path.isdir(self.STATIC_PATH):
            os.rename(self.STATIC_PATH, self.CACHED_PATH)
            self.cached_env = True

        os.makedirs(self.STATIC_PATH)
        self.test_env_active = True

    def restore_environment(self) -> None:
        """
        Restores the cached directory.
        """
        if self.test_env_active:
            shutil.rmtree(self.STATIC_PATH)

            if self.cached_env:
                os.rename(self.CACHED_PATH, self.STATIC_PATH)

        self.test_env_active = False

    def add_static_file(self, relative_static_path: str) -> None:
        """
        Adds a static file to the test environment.
        """
        if self.test_env_active:
            file_path = self.STATIC_PATH + "/" + relative_static_path

            # Create sub directories
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w+") as file:
                file.write(relative_static_path)
        else:
            raise RuntimeError("Test environment not activated.")


envManager = EnvironmentManager()


class APITests(TestCase):
    TEST_FILES = [
        "test_file_1.txt",
        "test_sub_dir/test_file_2.txt",
        "test_sub_dir/test_sub_sub_dir/test_file_3.txt"
    ]

    @classmethod
    def setUpClass(cls) -> None:
        """
        Creates static files for testing.
        """
        envManager.setup_test_environment()

        for test_file in APITests.TEST_FILES:
            envManager.add_static_file(test_file)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Deletes static files that were created for testing.
        """
        envManager.restore_environment()

    def test_get_index(self) -> None:
        """
        Tests that the index file works correctly.
        """
        response = self.client.get("")
        self.assertEqual(response.status_code, 404)

        envManager.add_static_file("index.html")

        test_paths = [
            "/",
            "/index.html",
            "/does_not_exist_but_should_return_index",
        ]

        for path in test_paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.getvalue().decode(), "index.html")

    def test_get_root_file(self) -> None:
        """
        Tests that files in the root directory can be retrieved.
        """
        response = self.client.get("/" + APITests.TEST_FILES[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), APITests.TEST_FILES[0])

    def test_get_sub_dir_file(self) -> None:
        """
        Tests that files in sub directories can be retrieved.
        """
        response = self.client.get("/" + APITests.TEST_FILES[1])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), APITests.TEST_FILES[1])

        response = self.client.get("/" + APITests.TEST_FILES[2])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.getvalue().decode(), APITests.TEST_FILES[2])
