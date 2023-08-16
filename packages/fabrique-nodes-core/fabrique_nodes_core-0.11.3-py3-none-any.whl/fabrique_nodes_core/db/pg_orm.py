from psycopg2.pool import ThreadedConnectionPool
import os
import sys
import time
import json


cur_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f'{cur_file_dir}/..')

import config as cfg
from db.data_model import (
    create_project_sql_str,
    create_pub_keys_str,
    create_priv_keys_str,
    ProjectRecordModel,
    ProjectMetaModel,
    proj_field_names,
    proj_meta_field_names
)

project_meta_model_fields = proj_meta_field_names.copy() + ['name']

from expiringdict import ExpiringDict


def create_pool():
    return ThreadedConnectionPool(
        cfg.POSTGRE_MIN_CONNECTIONS,
        cfg.POSTGRE_MAX_CONNECTIONS,
        host=cfg.POSTGRE_HOSTNAME,
        port=cfg.POSTGRE_PORT,
        database=cfg.POSTGRE_DATABASE,
        user=cfg.POSTGRE_USER,
        password=cfg.POSTGRE_PASSWORD
    )


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseDB:
    def __init__(self):
        self.cache = ExpiringDict(max_len=1000, max_age_seconds=cfg.POSTGRE_CACHE_SECONDS)
        self.conn_pool = create_pool()

    def execute(self, sql_str: str, params: tuple = (), commit: bool = False) -> list:
        conn = self.conn_pool.getconn()
        records = []
        with conn.cursor() as cur:
            cur.execute(sql_str, params)
            if not commit:
                records = cur.fetchall()
        if commit:
            conn.commit()
        self.conn_pool.putconn(conn)
        return records

    def execute_many(self, sql_str_list: list[str], params_list: list[tuple]):
        conn = self.conn_pool.getconn()
        try:
            with conn.cursor() as cur:
                for sqlstr, params in zip(sql_str_list, params_list):
                    cur.execute(sqlstr, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.conn_pool.putconn(conn)

    def fetch_one(self, sql_str: str, params: tuple = ()) -> list:
        cached = self.cache.get(sql_str)
        if cached:
            return cached

        conn = self.conn_pool.getconn()
        record = None
        with conn.cursor() as cur:
            cur.execute(sql_str, params)
            record = cur.fetchone()
        self.conn_pool.putconn(conn)
        try:
            cached[sql_str] = record
        except TypeError:
            pass
        return record


class CoreDB(BaseDB, metaclass=Singleton):
    def __init__(self):
        print('init_DB')
        super().__init__()

    def create_tables(self):
        self.execute_many([create_pub_keys_str,
                           create_priv_keys_str,
                           create_project_sql_str], [(), (), ()])

    def project_exists(self, project_id: str):
        rec = self.fetch_one("""
            SELECT rec_id FROM projects
            WHERE project_id = %s
        """, (project_id, )
        )
        if not rec:
            return False
        return True

    def pem_exists(self, user_id):
        rec = self.fetch_one("""
            SELECT user_id FROM user_pub_keys
            WHERE user_id = %s
        """, (user_id, )
        )
        if not rec:
            return False
        return True

    def get_public_pem(self, user_id: str) -> str:
        rec = self.fetch_one("""
            SELECT key_pem FROM user_pub_keys
            WHERE user_id = %s
        """, (user_id, )
        )
        if not rec:
            return None
        return rec[0]

    def get_private_pem(self, user_id: str) -> str:
        rec = self.fetch_one("""
            SELECT key_pem FROM user_priv_keys
            WHERE user_id = %s
        """, (user_id, )
        )
        if not rec:
            return None
        return rec[0]

    def write_key_pems(self, user_id: str, public_key_pem: str, private_key_pem: str):

        pub_key_sql = """
            INSERT INTO user_pub_keys (user_id, key_pem)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET key_pem = EXCLUDED.key_pem;
        """

        priv_key_sql = """
            INSERT INTO user_priv_keys (user_id, key_pem)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET key_pem = EXCLUDED.key_pem;
        """

        self.execute_many([pub_key_sql, priv_key_sql],
                          [(user_id, public_key_pem), (user_id, private_key_pem)])

    def write_project(self, rec: ProjectRecordModel, prev_ver=None, upsert=False, field_names=proj_field_names):
        timestamp_ms = int(time.time() * 1000)
        rec.created_ts = rec.created_ts or timestamp_ms
        rec.updated_ts = rec.updated_ts or timestamp_ms

        rec.prev_rec_id = rec.project_id + prev_ver if prev_ver else ''
        prev_ver = prev_ver or '0.0.0'
        auto_ver = prev_ver.split('-')[0] + f'-auto-{rec.created_ts}'

        rec.version = rec.version or auto_ver
        rec.rec_id = rec.rec_id or rec.project_id + rec.version
        rec.company_id = rec.company_id or rec.user_id
        rec.creator_id = rec.creator_id or rec.user_id

        values = []
        for field in field_names:
            val = getattr(rec, field)
            val = json.dumps(val) if field in ['data', 'samples'] else val
            values.append(val)

        insert_query = f"""
            INSERT INTO projects (
                {', '.join(field_names)}
            )
            VALUES ({', '.join(['%s']*len(field_names))})
        """

        update_query = f"""
            ON CONFLICT (rec_id)
            DO UPDATE SET
                {', '.join([f'{f} = EXCLUDED.{f}' for f in field_names])}
        """ if upsert else ''

        self.execute(insert_query + update_query, tuple(values), commit=True)

        return {'rec_id': rec.rec_id, 'project_id': rec.project_id, 'version': rec.version}

    def get_last_project_by_id(self, project_id: str, user_id: str) -> ProjectRecordModel:
        if user_id:
            rec = self.fetch_one(f"""
                SELECT {', '.join(proj_field_names)} FROM projects
                WHERE project_id = %s AND (user_id = %s OR is_public = True)
                ORDER BY updated_ts DESC
            """, (project_id, user_id)
            )
        else:
            rec = self.fetch_one(f"""
                SELECT {', '.join(proj_field_names)} FROM projects
                WHERE project_id = %s AND is_public = True
                ORDER BY updated_ts DESC
            """, (project_id, )
            )
        if not rec:
            return None
        return ProjectRecordModel(**dict(zip(proj_field_names, rec)))

    def get_project_rec(self, user_id: str,
                        rec_id: str = '', project_id: str = '', version: str = '') -> ProjectRecordModel:
        if not rec_id:
            rec_id = project_id + version
        if not user_id:  # public
            rec = self.fetch_one(f"""
                SELECT {', '.join(proj_field_names)} FROM projects
                WHERE rec_id = %s AND is_public = True
                ORDER BY updated_ts DESC
            """, (rec_id, )
            )
        else:
            rec = self.fetch_one(f"""
                SELECT {', '.join(proj_field_names)} FROM projects
                WHERE rec_id = %s AND user_id = %s
                ORDER BY updated_ts DESC
            """, (rec_id, user_id)
            )
        if not rec:
            return None
        return ProjectRecordModel(**dict(zip(proj_field_names, rec)))

    def upd_project(self, rec: ProjectRecordModel, user_id: str):
        last_ver_rec = self.get_last_project_by_id(rec.project_id, user_id)
        rec.prev_rec_id = last_ver_rec.rec_id
        return self.write_project(rec, last_ver_rec.version, upsert=True)

    def set_status(self, rec_id: str, status: str):
        self.execute("""
            UPDATE projects
            SET status = %s
            WHERE rec_id = %s
            """, (status, rec_id),
            commit=True
        )

    def set_desired_status(self, rec_id: str, desired_status: str):
        self.execute("""
            UPDATE projects
            SET desired_status = %s
            WHERE rec_id = %s
            """, (desired_status, rec_id),
            commit=True
        )

    def list_public_projects(self) -> list[str]:
        """DEPRECATED"""
        recs = self.execute("""
        WITH ranked_projects AS (
            SELECT
                rec_id,
                project_id,
                is_public,
                ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY updated_ts DESC) AS rn
            FROM
                projects
            WHERE
                is_public = True
        )
        SELECT
            rec_id
        FROM
            ranked_projects
        WHERE
            rn = 1;
        """)

        return [rec[0] for rec in recs]

    def list_user_projects(self, user_id: str) -> list[str]:
        """DEPRECATED"""
        recs = self.execute("""
        WITH ranked_projects AS (
            SELECT
                rec_id,
                project_id,
                user_id,
                ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY updated_ts DESC) AS rn
            FROM
                projects
            WHERE
                user_id = %s
        )
        SELECT
            rec_id
        FROM
            ranked_projects
        WHERE
            rn = 1;
        """, (user_id, ))

        return [rec[0] for rec in recs]

    def list_deploy_projects(self) -> list[str]:
        recs = self.execute("""
        SELECT
            rec_id
        FROM
            projects
        WHERE
            desired_status = 'deploy' or desired_status = 'forced_deploy';
        """)

        return [rec[0] for rec in recs]

    def get_project_versions(self, project_id: str, user_id: str):
        """DEPRECATED"""
        recs = self.execute("""SELECT
                rec_id,
                version
            FROM
                projects
            WHERE
                user_id = %s AND project_id= %s
            ORDER BY updated_ts DESC
            """, (user_id, project_id)
        )
        return {
            'rec_ids': [r[0] for r in recs],
            'versions': [r[1] for r in recs]
        }

    def get_public_projects_records(self) -> list[ProjectRecordModel]:
        """DEPRECATED"""
        rec_ids = self.list_public_projects()
        records = []
        for rec_id in rec_ids:
            rec = self.get_project_rec('', rec_id)
            if not rec:
                continue
            records.append(rec)
        return records

    def get_user_projects_records(self, user_id: str) -> list[ProjectRecordModel]:
        """DEPRECATED"""
        rec_ids = self.list_user_projects(user_id)
        records = []
        for rec_id in rec_ids:
            rec = self.get_project_rec(user_id, rec_id)
            if not rec:
                continue
            records.append(rec)
        return records

    def delete_project(self, user_id: str, rec_id: str = '', project_id: str = '', version: str = ''):
        if not rec_id:
            rec_id = project_id + version
        self.execute('DELETE FROM projects WHERE rec_id = %s and user_id = %s;', (rec_id, user_id), commit=True)

    def list_deployed_user_projects(self, user_id) -> list[str]:
        """DEPRECATED"""

        recs = self.execute("""
        SELECT
            rec_id, status, desired_status, version, project_id
        FROM
            projects
        WHERE
            desired_status = 'deploy' or desired_status = 'forced_deploy' and user_id = %s;
        """, (user_id,))

        return [{rec[0]: {'status': rec[1], 'desired_status': rec[2], 'version': rec[3], 'project_id': rec[4]}}
                for rec in recs]

    def update_only_data_and_samples(self, rec: ProjectRecordModel, prev_ver=None, upsert=False):
        field_names = [f for f in proj_field_names if f not in ['status', 'desired_status']]
        return self.write_project(rec, prev_ver=prev_ver, upsert=upsert, field_names=field_names)

    def drop_tables(self):
        self.execute("DROP TABLE IF EXISTS projects;", commit=True)
        self.execute("DROP TABLE IF EXISTS user_pub_keys;", commit=True)
        self.execute("DROP TABLE IF EXISTS user_priv_keys;", commit=True)
        self.execute("DROP TYPE IF EXISTS project_status_enum;", commit=True)
        self.execute("DROP TYPE IF EXISTS project_desired_status_enum;", commit=True)
        self.execute("DROP TYPE IF EXISTS project_type;", commit=True)


class DB(CoreDB, metaclass=Singleton):
    def list_user_projects_meta(self, user_id: str) -> list[ProjectMetaModel]:
        recs = self.execute(f"""
        WITH ranked_projects AS (
            SELECT
                {', '.join(proj_meta_field_names)},
                data->>'name' AS name,
                ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY updated_ts DESC) AS rn
            FROM
                projects
            WHERE
                user_id = %s
        )
        SELECT
            {', '.join(project_meta_model_fields)}
        FROM
            ranked_projects
        WHERE
            rn = 1
        ORDER BY updated_ts DESC;
        """, (user_id, ))

        return [ProjectMetaModel(**dict(zip(project_meta_model_fields, rec))) for rec in recs]

    def list_public_projects_meta(self) -> list[ProjectMetaModel]:

        recs = self.execute(f"""
        WITH ranked_projects AS (
            SELECT
                {', '.join(proj_meta_field_names)},
                data->>'name' AS name,
                ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY updated_ts DESC) AS rn
            FROM
                projects
            WHERE
                is_public = True
        )
        SELECT
            {', '.join(project_meta_model_fields)}
        FROM
            ranked_projects
        WHERE
            rn = 1
        ORDER BY updated_ts DESC;
        """)

        return [ProjectMetaModel(**dict(zip(project_meta_model_fields, rec))) for rec in recs]

    def list_deployed_user_projects_meta(self, user_id) -> list[ProjectMetaModel]:

        recs = self.execute(f"""
        SELECT
            {', '.join(proj_meta_field_names)},
            data->>'name' AS name
        FROM
            projects
        WHERE
            desired_status = 'deploy' or desired_status = 'forced_deploy'  and user_id = %s
        ORDER BY updated_ts DESC;
        """, (user_id,))

        return [ProjectMetaModel(**dict(zip(project_meta_model_fields, rec))) for rec in recs]

    def list_versions_meta(self, project_id: str, user_id: str):

        recs = self.execute(f"""SELECT
                {', '.join(proj_meta_field_names)},
                data->>'name' AS name
            FROM
                projects
            WHERE
                user_id = %s AND project_id= %s
            ORDER BY updated_ts DESC
            """, (user_id, project_id)
        )
        return [ProjectMetaModel(**dict(zip(project_meta_model_fields, rec))) for rec in recs]

    def admin_list_all_records(self) -> list[str]:

        recs = self.execute(f"""
        WITH ranked_projects AS (
            SELECT
                {', '.join(proj_meta_field_names)},
                data->>'name' AS name,
                ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY updated_ts DESC) AS rn
            FROM
                projects
        )
        SELECT
            {', '.join(project_meta_model_fields)}
        FROM
            ranked_projects
        WHERE
            rn = 1;
        """)

        return [ProjectMetaModel(**dict(zip(project_meta_model_fields, rec))) for rec in recs]

    def admin_get_project_rec(self, rec_id) -> ProjectRecordModel:
        rec = self.fetch_one(f"""
            SELECT {', '.join(proj_field_names)} FROM projects
            WHERE rec_id = %s
            ORDER BY updated_ts DESC
        """, (rec_id, )
        )
        if not rec:
            return None
        return ProjectRecordModel(**dict(zip(proj_field_names, rec)))

    def admin_delete_project_rec(self, rec_id) -> ProjectRecordModel:
        self.execute('DELETE FROM projects WHERE rec_id = %s;', (rec_id,), commit=True)

    def admin_write_project(self, rec: ProjectRecordModel, field_names=proj_field_names):
        timestamp_ms = int(time.time() * 1000)
        rec.created_ts = rec.created_ts or timestamp_ms
        rec.updated_ts = rec.updated_ts or timestamp_ms

        rec.prev_rec_id = rec.prev_rec_id or ''
        rec.version = rec.version or 'auto'
        rec.rec_id = rec.rec_id or rec.project_id + rec.version
        rec.company_id = rec.company_id or rec.user_id
        rec.creator_id = rec.creator_id or rec.user_id
        rec.samples = rec.samples or {}

        values = []

        for field in field_names:
            val = getattr(rec, field)
            val = json.dumps(val) if field in ['data', 'samples'] else val
            values.append(val)

        query = f"""
            INSERT INTO projects (
                {', '.join(field_names)}
            )
            VALUES ({', '.join(['%s']*len(field_names))})
            ON CONFLICT (rec_id)
            DO UPDATE SET
                {', '.join([f'{f} = EXCLUDED.{f}' for f in field_names])}
        """

        self.execute(query, tuple(values), commit=True)

        return {'rec_id': rec.rec_id, 'project_id': rec.project_id, 'version': rec.version}
