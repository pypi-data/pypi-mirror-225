import os
import sys
# noinspection PyPackageRequirements
from unittest.mock import patch


cur_file_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = f'{cur_file_dir}/../fabrique_nodes_core'
sys.path.append(lib_dir)
os.chdir(cur_file_dir)

import tests.import_spoofer  # noqa: F401

from fabrique_nodes_core.crypto import Crypto
from fabrique_nodes_core.db.fake_db import FakeDB


@patch('fabrique_nodes_core.crypto.DB', new=FakeDB)
def test_aggregators():
    crypto = Crypto('_user_id_')
    assert crypto.db.pem_exists('_user_id_')
    assert crypto.private_key_pem
    assert crypto.public_key_pem
