from db.pg_orm import DB
import sqlite3
import re

from db.data_model import (
    create_project_sql_str,
    create_pub_keys_str,
    create_priv_keys_str,
    # ProjectRecordModel,
    # proj_field_names,
)


def pg2sq(sql_str):
    # Замена ENUM
    enum_pattern = r"CREATE TYPE (\w+) AS ENUM \((.*?)\);"
    replacement = r"\1 TEXT CHECK(\1 IN (\2)),"
    sql_str = re.sub(enum_pattern, replacement, sql_str)

    # Удаление DO $$ BEGIN END $$;
    # sql_str = sql_str.replace('DO $$', '').replace('BEGIN', '').replace('END', '').replace('$$;', '')
    p_beg = sql_str.split('DO $$')[0]
    p_end = sql_str.split('$$;')[-1]

    sql_str = p_beg + p_end

    # Замена EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)
    pg_str = "version VARCHAR(255) NOT NULL DEFAULT '0.0.0-auto-' || EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::BIGINT"
    sql_str = sql_str.replace(pg_str, "version VARCHAR(255) NOT NULL DEFAULT 'auto'")

    # Замена EXTRACT(EPOCH FROM NOW())
    sql_str = sql_str.replace("EXTRACT(EPOCH FROM NOW()) * 1000", "(strftime('%s', 'now') * 1000)")

    return sql_str


class FakeDB(DB):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cache = {}
        self._create_tables()

    def _create_tables(self):
        for create_sql_str in [create_project_sql_str, create_pub_keys_str, create_priv_keys_str]:
            for sqlstr in pg2sq(create_sql_str).split(';'):
                sqlstr = sqlstr.strip()
                if not sqlstr:
                    continue
                self.execute(sqlstr)

    def _execute_sqlite(self, sql_str: str, params: tuple = (), commit: bool = False) -> list:
        sql_str = sql_str.replace('%s', '?')
        sql_str = sql_str.replace("data->>'name' AS name", "json_extract(data, '$.name') AS name")

        records = []
        cur = self.conn.cursor()
        cur.execute(sql_str, params)
        if not commit:
            records = cur.fetchall()
        if commit:
            self.conn.commit()
        return records

    def execute(self, sql_str: str, params: tuple = (), commit: bool = False) -> list:
        records = self._execute_sqlite(sql_str, params, commit)
        return records

    def execute_many(self, sql_str_list: list[str], params_list: list[tuple]):
        try:
            for sqlstr, params in zip(sql_str_list, params_list):
                self._execute_sqlite(sqlstr, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_one(self, sql_str: str, params: tuple = ()) -> list:
        cur = self.conn.cursor()
        sql_str = sql_str.replace('%s', '?')
        cur.execute(sql_str, params)
        record = cur.fetchone()
        return record
