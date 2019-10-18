"""Base Test Design for LocalEGA Inbox Scenario 4.

For this test we are aiming to upload, rename and remove an encrypted file.
Scenario 4: Upload an encrypted file, rename and remove file without reconnecting.
"""

import os
import paramiko
from ruamel.yaml import YAML
from locust import Locust, TaskSet, task
from common import log_format, CONFIG_PATH

LOG = log_format('test_inbox_3')


def open_ssh_connection(hostname, user, key_path, key_pass=None, port=2222):
    """Open an ssh connection, test function."""
    try:
        client = paramiko.SSHClient()
        k = paramiko.RSAKey.from_private_key_file(key_path, password=key_pass)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, allow_agent=False, look_for_keys=False,
                       port=port, timeout=0.3, username=user, pkey=k)
        LOG.info(f'ssh connected to {hostname}:{port} with {user}')
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


def sftp_upload_rename_remove(hostname, user, remote_path, new_name, key_path, key_pass=None, port=2222):
    """SFTP Client file upload."""
    try:
        k = paramiko.RSAKey.from_private_key_file(key_path, password=key_pass)
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=user, pkey=k)
        LOG.debug(f'sftp connected to {hostname}:{port} with {user}')
        sftp = paramiko.SFTPClient.from_transport(transport)
        filename, _ = os.path.splitext(remote_path)
        sftp.put(remote_path, f'{filename}'.c4ga)
        sftp.rename(f'{filename}'.c4ga, new_name)
        sftp.remove(new_name)
        LOG.info(f'file renamed to {new_name}')
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
        with open(f'{CONFIG_PATH}/inbox_config.yaml', 'r') as stream:
            self.config = yaml.load(stream)
        # We can reuse the same settings as in scenario2
        self.key_pk = os.path.expanduser(self.config['settings']['user_key'])
        self.user = self.config['settings']['user']
        self.test_file = os.path.expanduser(self.config['scenario4']['test_file'])
        self.new_file = os.path.expanduser(self.config['scenario4']['new_file'])
        open_ssh_connection(self.locust.host, self.user, self.key_pk)

    @task
    def rename(self):
        """Test upload and rename file."""
        sftp_upload_rename_remove(self.locust.host, self.user,
                                  self.test_file, self.new_file, self.key_pk)


class InboxTest(Locust):
    """Test LocalEGA Inbox.

    For this kind of test we need a normal locust.
    """

    task_set = InboxBehavior
    min_wait = 5000
    max_wait = 30000
