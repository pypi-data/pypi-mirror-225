import argparse
import pytest
import subprocess

from unittest.mock import patch

from src.crash_test.crashtest import CrashTest


@pytest.fixture
def mock_multipass_command_execution():
    """
    Mocks the execution of multipass commands for testing purposes
    """
    with patch('subprocess.run') as mock_subprocess_run:
        yield mock_subprocess_run


class TestCrashTest:
    # args_check (instance_name and project path are both valid)
    def test_args_check_name_and_path_valid(self, tmp_path):
        """
        Tests that when the instance name and the project path are valid the function returns True
        :param tmp_path: pathlib.Path object to create temporary path
        """
        project_folder = tmp_path / "test_project"
        project_folder.mkdir()
        args = argparse.Namespace(instance_name="valid-instance-name", project=project_folder, delete=False)
        assert CrashTest(args=args).args_check() is True

    # args_check (instance_name and project path are both invalid)
    def test_args_check_name_and_path_invalid(self):
        """
        Tests that when the instance name and the project path are invalid the function returns False
        """
        args = argparse.Namespace(instance_name="invalid_instance_name", project="invalid/path/", delete=False)
        assert CrashTest(args=args).args_check() is False

    # args_check (instance_name is valid and project path is invalid)
    def test_args_check_name_valid_path_invalid(self):
        """
        Tests that when the instance name is valid and the project path is invalid the function returns False
        """
        args = argparse.Namespace(instance_name="valid-instance-name", project="invalid/path/", delete=False)
        assert CrashTest(args=args).args_check() is False

    # args_check (instance_name is invalid and project path is valid)
    def test_args_check_name_invalid_path_valid(self, tmp_path):
        """
        Tests that when the instance name is invalid and the project path is valid the function returns False
        :param tmp_path: pathlib.Path object to create temporary path
        """
        project_folder = tmp_path / "test_project"
        project_folder.mkdir()
        args = argparse.Namespace(instance_name="invalid_instance_name", project=project_folder, delete=False)
        assert CrashTest(args=args).args_check() is False

    # execute_multipass_command
    def test_execute_multipass_command(self, mock_multipass_command_execution):
        """
        Tests that the mock was called exactly once and that that call was
        with the specified arguments
        :param mock_multipass_command_execution: function that mocks the execution of multipass commands
        """
        mock_multipass_command_execution.return_value.returncode = 0
        crash_test = CrashTest(None)
        crash_test.execute_multipass_command(["multipass", "launch", "--name", "test-instance"])
        mock_multipass_command_execution.assert_called_once_with(
            ["multipass", "launch", "--name", "test-instance"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
