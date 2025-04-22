import unittest
import docker
import subprocess
import time
from docker.errors import NotFound, DockerException
from test.TestUtils import TestUtils

class TestDockerCLIValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = docker.from_env()
        cls.image_name = "hello-world"
        cls.container_name = "hello_test_container"
        cls.network_name = "test_net"
        
        # Stop any existing containers
        subprocess.run(["docker-compose", "down"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Build and start containers
        subprocess.run(["docker-compose", "up", "-d", "--build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Allow services to start

    @classmethod
    def tearDownClass(cls):
        # Clean up containers
        subprocess.run(["docker-compose", "down"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def setUp(self):
        self.test_obj = TestUtils()

    def test_00_docker_daemon_running(self):
        """Check if Docker daemon is running and accessible."""
        try:
            version = self.client.version()
            result = "Version" in version
            self.test_obj.yakshaAssert("TestDockerDaemonRunning", result, "functional")
            self.assertIn("Version", version)
            if result:
                print("TestDockerDaemonRunning = Passed")
            else:
                print("TestDockerDaemonRunning = Failed")
        except DockerException as e:
            self.test_obj.yakshaAssert("TestDockerDaemonRunning", False, "functional")
            print(f"TestDockerDaemonRunning = Failed | ❌ Docker daemon not accessible: {e}")
            # No self.fail() call

    def test_01_image_exists(self):
        """Verify image exists locally."""
        try:
            images = self.client.images.list(name=self.image_name)
            result = any(self.image_name in tag for img in images for tag in img.tags)
            self.test_obj.yakshaAssert("TestImageExists", result, "functional")
            self.assertTrue(result)
            if result:
                print("TestImageExists = Passed")
            else:
                print("TestImageExists = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestImageExists", False, "functional")
            print(f"TestImageExists = Failed | Exception: {e}")
            # No self.fail() call

    def test_02_container_exists(self):
        """Verify container was created."""
        try:
            container = self.client.containers.get(self.container_name)
            result = container.name == self.container_name
            self.test_obj.yakshaAssert("TestContainerExists", result, "functional")
            self.assertEqual(container.name, self.container_name)
            if result:
                print("TestContainerExists = Passed")
            else:
                print("TestContainerExists = Failed")
        except NotFound:
            self.test_obj.yakshaAssert("TestContainerExists", False, "functional")
            print("TestContainerExists = Failed | ❌ Container was not found.")
            # No self.fail() call
        except Exception as e:
            self.test_obj.yakshaAssert("TestContainerExists", False, "functional")
            print(f"TestContainerExists = Failed | Exception: {e}")
            # No self.fail() call

    def test_03_container_started(self):
        """Check if container ran at least once."""
        try:
            container = self.client.containers.get(self.container_name)
            container.reload()
            result = container.status in ['exited', 'running']
            self.test_obj.yakshaAssert("TestContainerStarted", result, "functional")
            self.assertIn(container.status, ['exited', 'running'])
            if result:
                print("TestContainerStarted = Passed")
            else:
                print("TestContainerStarted = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestContainerStarted", False, "functional")
            print(f"TestContainerStarted = Failed | Exception: {e}")
            # No self.fail() call

    def test_04_container_logs(self):
        """Check container output contains 'Hello from Docker'."""
        try:
            container = self.client.containers.get(self.container_name)
            logs = container.logs().decode('utf-8')
            result = "Hello from Docker!" in logs
            self.test_obj.yakshaAssert("TestContainerLogs", result, "functional")
            self.assertIn("Hello from Docker!", logs)
            if result:
                print("TestContainerLogs = Passed")
            else:
                print("TestContainerLogs = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestContainerLogs", False, "functional")
            print(f"TestContainerLogs = Failed | Exception: {e}")
            # No self.fail() call

    def test_06_inspect_container_metadata(self):
        """Inspect container metadata for correct image reference."""
        try:
            container = self.client.containers.get(self.container_name)
            container_info = container.attrs
            image_used = container_info['Config']['Image']
            result = image_used == self.image_name
            self.test_obj.yakshaAssert("TestContainerMetadata", result, "functional")
            self.assertEqual(image_used, self.image_name)
            if result:
                print("TestContainerMetadata = Passed")
            else:
                print("TestContainerMetadata = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestContainerMetadata", False, "functional")
            print(f"TestContainerMetadata = Failed | Exception: {e}")
            # No self.fail() call

if __name__ == '__main__':
    unittest.main(verbosity=2)
