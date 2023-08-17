"""Module for the FakeRepo testing utility class"""

import os
import shutil

TEST_HIL_ROOT_PATH      = 'hil_sdk'
TEST_HIL_ARTIFACTS_PATH = 'artifacts/main.hex'
TEST_ARTIFACT_SOURCE    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_fixtures", "main.hex"))


class FakeRepo:

    """Creates a temporary directory that looks like a fully-functioning repository directory"""

    def __init__(self, repo_id):

        """Create the initial temporary directory"""

        self.temp_dir_path = os.path.join(os.getcwd(), 'fake_repo_dir')
        shutil.rmtree(self.temp_dir_path, ignore_errors=True)
        os.mkdir(self.temp_dir_path)

        self.repo_id = repo_id

        self.reset()

    def reset(self):
        """Completely reset and restore a fake repo into the same initial temporary directory"""

        dot_eo_path = os.path.join(self.temp_dir_path, '.embedops')
        shutil.rmtree(dot_eo_path, ignore_errors=True)
        os.mkdir(dot_eo_path)

        hil_sdk_dir = os.path.join(self.temp_dir_path, TEST_HIL_ROOT_PATH)
        shutil.rmtree(hil_sdk_dir, ignore_errors=True)
        os.mkdir(hil_sdk_dir)

        artifacts_dir = os.path.join(self.temp_dir_path, os.path.dirname(TEST_HIL_ARTIFACTS_PATH))
        shutil.rmtree(artifacts_dir, ignore_errors=True)
        os.mkdir(artifacts_dir)
        shutil.copyfile(TEST_ARTIFACT_SOURCE, os.path.join(self.temp_dir_path, TEST_HIL_ARTIFACTS_PATH))

        hil_config_dir = os.path.join(dot_eo_path, 'hil')
        os.mkdir(hil_config_dir)

        self.hil_config_yml = os.path.join(hil_config_dir, 'config.yml')
        with open(self.hil_config_yml, "w") as hil_config_file:
            hil_config_file.write('hil_root_path: %s\n' % TEST_HIL_ROOT_PATH)
            hil_config_file.write('hil_artifacts: %s\n' % TEST_HIL_ARTIFACTS_PATH)

    def get_fake_repo_path(self):
        """Return the full absolute path to the fake repo"""
        return self.temp_dir_path

    def cleanup(self):
        """Cleanup all temporary files and directories"""
        shutil.rmtree(self.temp_dir_path, ignore_errors=True)

    def remove_hil_config_yml(self):
        """Delete the repo_id.yml file"""
        os.remove(self.hil_config_yml)

    def remove_hil_root_path_attr(self):
        """Invalidate the repo_id.yml file"""
        with open(self.hil_config_yml, "w") as config_file:
            config_file.write('not_hil_root_path: test\n')
            config_file.write('hil_artifacts: %s\n' % TEST_HIL_ARTIFACTS_PATH)

    def remove_hil_artifacts_path_attr(self):

        with open(self.hil_config_yml, "w") as config_file:
            config_file.write('hil_root_path: %s\n' % TEST_HIL_ROOT_PATH)
            config_file.write('not_hil_artifacts: test\n')