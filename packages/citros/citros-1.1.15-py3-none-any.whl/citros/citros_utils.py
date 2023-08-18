
import threading
import base64
import os
import stat
import psutil
import subprocess
import re
import shutil
import threading
import time
import csv
import hashlib
from datetime import datetime

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
from cryptography.hazmat.backends import default_backend as crypto_default_backend


class citros_utils():
    def __init__(self, citros):
        self.citros = citros      
        self.log = citros.log

        self.stop_flag = threading.Event()
        self.thread = None

    ########################## encode/decode base64 ###########################
    
    def encode64(self, original_string : str):
        """
        Encodes a given string into base64.
        """
        encoded_string = base64.b64encode(original_string.encode()).decode()
        return encoded_string
    

    def decode64(self, encoded_string : str):
        """
        Decodes a given base64 string back to its original form.
        """
        decoded_string = base64.b64decode(encoded_string).decode()
        return decoded_string

    ################################## hash ###################################

    def compute_sha256_hash(self, file_path):
        """
        Computes the SHA-256 hash of a file.
        """
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    ################################## ssh ####################################
    
    def check_ssh_key_pair(self):
        """
        Checks the existence of SSH key pairs in the user's SSH directory.

        Returns:
            str or None: The type of the existing key pair ('id_ed25519' or 'id_rsa') if found, 
            or None if no key pair is found.
        """
        ssh_dir = os.path.expanduser('~/.ssh')

        if os.path.exists(os.path.join(ssh_dir, 'citros_ed25519')) and \
           os.path.exists(os.path.join(ssh_dir, 'citros_ed25519.pub')):
            return 'citros_ed25519'
        elif os.path.exists(os.path.join(ssh_dir, 'citros_rsa')) and \
             os.path.exists(os.path.join(ssh_dir, 'citros_rsa.pub')):
            return 'citros_rsa'
        else:
            return None


    def create_ssh_key_pair(self, key_type='ed25519', key_comment=""):
        """
        Creates an SSH key pair of either RSA or Ed25519 type.
        Creates or updates ssh config file accordingly.
        Args:
            key_type (str, optional): The type of SSH key pair to create, either 'rsa' or 'ed25519'. 
                Defaults to 'ed25519'.
            key_comment (str, optional): Comment to append to the public key. If not provided, 
                the Citros user's email is used. Defaults to an empty string.

        Returns:
            str: The public key in OpenSSH format with the comment appended.

        Raises:
            ValueError: If an unsupported key_type is provided.
        """
        if not key_comment:
            key_comment = self.citros.get_username_and_hostname()

        rsa_name = 'citros_rsa'
        ed_name = 'citros_ed25519'

        if key_type == 'rsa':
            key = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=2048
            )
            private_key_path = os.path.join('~/.ssh', rsa_name)
            public_key_path = os.path.join('~/.ssh', f'{rsa_name}.pub')
        elif key_type == 'ed25519':
            key = ed25519.Ed25519PrivateKey.generate()
            private_key_path = os.path.join('~/.ssh', ed_name)
            public_key_path = os.path.join('~/.ssh', f'{ed_name}.pub')
        else:
            raise ValueError("Invalid key_type! Choose either 'rsa' or 'ed25519'.")

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.OpenSSH,
            crypto_serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

        ssh_dir = os.path.expanduser('~/.ssh')
        os.makedirs(ssh_dir, exist_ok=True)

        private_key_path = os.path.expanduser(private_key_path)
        public_key_path = os.path.expanduser(public_key_path)

        # Write the private key to a file
        with open(private_key_path, 'wb') as priv_file:
            priv_file.write(private_key)

        os.chmod(private_key_path, stat.S_IRUSR | stat.S_IWUSR)

        # Write the public key to a file
        with open(public_key_path, 'wb') as pub_file:
            pub_file.write(public_key + f' {key_comment}'.encode())

        # Create or update ssh config file
        file_name = ed_name if key_type == 'ed25519' else rsa_name
        self.setup_ssh_config(self.citros.CITROS_GIT_DOMAIN, file_name)

        return public_key.decode() + f' {key_comment}'
    

    def setup_ssh_config(self, host_name, file_name):
        """
        Creates a `config` file under the user's .ssh dir (if it doesn't already exit),
        and appends the Host/IdentityFile lines with the given host and key file names
        (or overwrites if the Host exists but the IdentityFile is different).
        """
        config_file_path = os.path.expanduser("~/.ssh/config")
        
        # Check if config file exists, create if not
        if not os.path.exists(config_file_path):
            open(config_file_path, 'w').close()
        
        # Read content of the config file
        with open(config_file_path, 'r') as file:
            lines = file.readlines()

        # Construct the strings to match
        host_string = f"Host {host_name}\n"
        identity_string = f"\tIdentityFile ~/.ssh/{file_name}\n"

        # Check if the hostname exists in the file
        if host_string in lines:
            host_index = lines.index(host_string)
            # Check if the next line has the correct filename
            if lines[host_index+1] != identity_string:
                # Overwrite filename if different
                lines[host_index+1] = identity_string
        else:
            # Append host and filename if hostname not in file
            lines.extend([host_string, identity_string])

        # Write back to the config file
        with open(config_file_path, 'w') as file:
            file.writelines(lines)
    

    def check_ssh_key_uploaded(self, key_file_name):
        """
        Checks if an SSH key has been uploaded to the 'git.citros.io' server.
        
        Args:
            key_file_name (str): The file name of the private key in the user's SSH directory.

        Returns:
            bool: True if the SSH key has been uploaded, False otherwise.

        Raises:
            ValueError: If the key file does not exist in the SSH directory or the file name 
            does not include 'ed25519' or 'rsa'.
        """
        hostname = self.citros.CITROS_GIT_DOMAIN
        username = self.citros.CITROS_GIT_USER

        ssh_dir = os.path.expanduser('~/.ssh')
        private_key_path = os.path.join(ssh_dir, key_file_name)

        if not os.path.exists(private_key_path):
            self.log.error(f"ssh key file {key_file_name} does not exist in {ssh_dir}.")
            raise ValueError(f"{key_file_name}")

        if 'ed25519' not in key_file_name and 'rsa' not in key_file_name:
            self.log.error(f"ssh key file name must include `ed25519` or `rsa`. The name {key_file_name} is invalid.")
            raise ValueError(f"{key_file_name}")

        ssh_command = ['ssh', '-i', private_key_path, '-o', 'StrictHostKeyChecking=no', f'{username}@{hostname}', 'info']
        
        try:
            output = subprocess.check_output(ssh_command, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        self.log.debug(f"ssh output = {output}")

        if 'Permission denied' in output: 
            return False    # The key has not been uploaded yet
        else:
            return True
        

    def is_repo_ready(self, slug, proj_name):
        hostname = self.citros.CITROS_GIT_DOMAIN
        username = self.citros.CITROS_GIT_USER

        ssh_command = ['ssh', '-o', 'StrictHostKeyChecking=no', f'{username}@{hostname}', 'info']
        
        try:
            output = subprocess.check_output(ssh_command, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        expected = f"{slug}/{proj_name}"

        self.log.debug(f"SSH info output:\n[{output}]\n")

        return expected in output
    
    ############################# stats sampling ##############################

    def _sample_system_statistics(self):
        cpu_usage = psutil.cpu_percent()

        memory_info = psutil.virtual_memory()

        total_memory = memory_info.total
        available_memory = memory_info.available
        used_memory = memory_info.used
        memory_percent = memory_info.percent

        return cpu_usage, total_memory, available_memory, used_memory, memory_percent
    

    def _write_statistics_to_file(self, file_name):
        with open(file_name, 'a') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(self._sample_system_statistics())


    def _stats_collection_loop(self, interval, file_name):
        while not self.stop_flag.is_set():
            self._write_statistics_to_file(file_name)
            time.sleep(interval)


    def start_collecting_stats(self, interval, file_name):
        with open(file_name, 'w') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(['cpu usage (%)', 'total memory', 'available memory', 'used memory', 'memory usage (%)'])

        self.stop_flag.clear()
        self.thread = threading.Thread(target=self._stats_collection_loop, args=(interval, file_name))
        self.thread.start()


    def stop_collecting_stats(self):
        if self.thread is not None:
            self.stop_flag.set()
            self.thread.join()

    ########################### file and format utils ######################### 

    def is_valid_file_name(self, name : str):
        # check for empty name, invalid characters and trailing periods or spaces.
        if not name or \
           re.search(r'[\\/*?:"<>|]', name) or \
           name[-1] == '.' or name[-1] == ' ':
            self.log.warning(f"invalid file or folder name: {name}")
            return False

        return True


    def get_foramtted_datetime(self):
        now = datetime.now()
        formatted = now.strftime('%Y-%m-%d-%H-%M-%S')

        # Use only the last two digits of the year
        formatted = formatted[2:]
        
        return formatted
    

    def copy_files(self, file_paths, target_directory, create_dir=False):
        if create_dir:
            # Create the target directory if it does not exist
            os.makedirs(target_directory, exist_ok=True)

        for file_path in file_paths:
            if os.path.isfile(file_path):
                shutil.copy(file_path, target_directory)
            else:
                self.log.error(f"copy_files: File does not exist: {file_path}")

    
    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError(f"Cannot convert {s} to a bool")


###############################################################################

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator
