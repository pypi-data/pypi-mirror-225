import base64
import os


def b64_encryption(filepath):
    filepath = filepath.replace("'", "")
    absolute_filepath = os.path.expanduser(filepath)
    with open(absolute_filepath, 'rb') as f:
        contents = f.read()
        encryption = str(base64.b64encode(contents))
        encryption = encryption[2:(len(encryption) - 1)]
        pass
    return encryption
