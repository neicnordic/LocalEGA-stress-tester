import os
import paramiko
from ruamel.yaml import YAML
from locust import Locust, TaskSet, task
import logging

# Keeping it simple with the logging formatting

formatting = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatting)

LOG = logging.getLogger("test_inbox")


def open_ssh_connection(hostname, user, key_path, key_pass=None, port=2222):
    """Open an ssh connection, test function."""
    try:
        client = paramiko.SSHClient()
        k = paramiko.RSAKey.from_private_key_file(key_path, password=key_pass)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, allow_agent=False, look_for_keys=False, port=port, timeout=0.3, username=user, pkey=k)
        LOG.info(f'ssh connected to {hostname}:{port} with {user} | PASS |')
    except paramiko.BadHostKeyException as e:
        LOG.error(f'Something went wrong {e}')
        raise Exception('BadHostKeyException on ' + hostname)
    except paramiko.AuthenticationException as e:
        LOG.error(f'Something went wrong {e}')
        raise Exception('AuthenticationException on ' + hostname)
    except paramiko.SSHException as e:
        LOG.error(f'Something went wrong {e}')
        raise Exception('SSHException on ' + hostname)

    return client


def sftp_upload(hostname, user, file_path, key_path, key_pass=None, port=2222):
    """SFTP Client file upload."""
    try:
        k = paramiko.RSAKey.from_private_key_file(key_path, password=key_pass)
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=user, pkey=k)
        LOG.debug(f'sftp connected to {hostname}:{port} with {user}')
        sftp = paramiko.SFTPClient.from_transport(transport)
        filename, _ = os.path.splitext(file_path)
        sftp.put(file_path, f'{filename}.c4ga')
        LOG.info(f'file uploaded {filename}.c4ga | PASS |')
    except Exception as e:
        LOG.error(f'Something went wrong {e}')
        raise e
    finally:
        LOG.debug('sftp done')
        transport.close()


class InboxBehavior(TaskSet):
    """Test Tasks for LocalEGA Inbox."""

    def setup(self):
        """Test if the inbox is reachable."""
        yaml = YAML(typ='safe')
        with open('../stress_tests/config.yaml', 'r') as stream:
            self.config = yaml.load(stream)
        self.key_pk = os.path.expanduser(self.config['localega']['user_key'])
        open_ssh_connection(self.locust.host, 'dummy', self.key_pk)

    @task
    def upload(self):
        """Test one upload.

        The only endpoint that has some sort of caching.
        """
        file = '../stress_tests/config.yaml'
        sftp_upload(self.locust.host, file, 'dummy', self.key_pk)


class InboxTest(Locust):
    """Test LocalEGA Inbox.

    For this kind of test we need a normal locust.
    """

    task_set = InboxBehavior
    min_wait = 5000
    max_wait = 30000
