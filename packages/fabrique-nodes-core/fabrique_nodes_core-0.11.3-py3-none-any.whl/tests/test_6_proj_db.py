import os
import sys
# noinspection PyPackageRequirements
# from unittest.mock import patch
import json


cur_file_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = f'{cur_file_dir}/../fabrique_nodes_core'
sys.path.append(lib_dir)
os.chdir(cur_file_dir)

import tests.import_spoofer  # noqa: F401

from fabrique_nodes_core.db.fake_db import FakeDB as DB
from fabrique_nodes_core.db.data_model import ProjectRecordModel
# from fabrique_nodes_core.db import DB


def file2str(pth):
    with open(pth) as fp:
        txt = fp.read()
    return txt


# @patch('fabrique_nodes_core.crypto.DB', new=FakeDB)
def test_admin():
    # SAVE version to DB
    proj_data = json.loads(file2str(f'{cur_file_dir}/data/sqs_simple.json'))
    project_id = 'ProjectId'
    version = '0.0.0'
    user_id = '_user_id_'
    rec = ProjectRecordModel(project_id=project_id, version=version, data=proj_data, user_id=user_id)

    db = DB()
    db.admin_write_project(rec)

    # read from db
    saved_rec = db.admin_get_project_rec(project_id + version)
    assert saved_rec

    # read admin list
    records = db.admin_list_all_records()
    assert len(records) == 1
    assert records[0].name == rec.data['name']

    # upd project in db
    rec.data['name'] = 'sqs_renamed'
    db.admin_write_project(rec)

    # read from db
    saved_rec = db.admin_get_project_rec(project_id + version)
    assert saved_rec.data['name'] == rec.data['name']

    # admin delete from db
    db.admin_delete_project_rec(project_id + version)
    records = db.admin_list_all_records()
    assert len(records) == 0

    # write 2 versions to db and check
    db.admin_write_project(rec)
    rec.version = 'auto'
    rec.rec_id = ''
    db.admin_write_project(rec)
    versions = db.list_versions_meta(rec.project_id, rec.user_id)
    assert len(versions) == 2
    assert versions[0].name == rec.data['name']

    # list user projects
    user_projects = db.list_user_projects_meta(user_id=user_id)
    assert len(user_projects) == 1
    assert user_projects[0].name == rec.data['name']

    # list public versions
    pub_projects = db.list_public_projects_meta()
    assert len(pub_projects) == 0
    rec.is_public = True
    db.admin_write_project(rec)
    pub_projects = db.list_public_projects_meta()
    assert len(pub_projects) == 1
    assert pub_projects[0].name == rec.data['name']

    # list deployed versions
    deployed_projects = db.list_deployed_user_projects_meta(user_id)
    assert len(deployed_projects) == 0
    db.set_desired_status(versions[0].rec_id, 'deploy')
    deployed_projects = db.list_deployed_user_projects_meta(user_id)
    assert len(deployed_projects) == 1
    assert deployed_projects[0].name == rec.data['name']
