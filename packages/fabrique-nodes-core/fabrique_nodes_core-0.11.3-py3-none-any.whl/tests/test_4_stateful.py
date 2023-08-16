import os
import sys
# noinspection PyPackageRequirements
import random

cur_file_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = f'{cur_file_dir}/../fabrique_nodes_core'
sys.path.append(lib_dir)
os.chdir(cur_file_dir)

import tests.import_spoofer  # noqa: F401

from fabrique_nodes_core.stateful.state import InmemKV


def test_aggregators():
    def agg_tester(aggregator_id, v1, v2, expected):
        collection = aggregator_id + ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm', k=10))
        key = 'key0'
        kv.connect_collection(collection, aggregator_id=aggregator_id)
        kv.upd_agg(collection, key, v1)
        kv.upd_agg(collection, key, v2)
        assert kv.get_agg(collection, key) == expected

    kv = InmemKV()
    # test sum
    agg_tester('SUM', 2.0, 3.0, 5.0)
    agg_tester('SUM', -3.0, 3.0, 0.0)
    # test mean
    agg_tester('MEAN', 2.0, 3.0, 2.5)
    agg_tester('MEAN', -2.0, -3.0, -2.5)
    # test max
    agg_tester('MAX', 2.0, 3.0, 3.0)
    agg_tester('MAX', 2.0, -3.0, 2.0)
    # test min
    agg_tester('MIN', 2.0, 3.0, 2.0)
    agg_tester('MIN', 2.0, -3.0, -3.0)
