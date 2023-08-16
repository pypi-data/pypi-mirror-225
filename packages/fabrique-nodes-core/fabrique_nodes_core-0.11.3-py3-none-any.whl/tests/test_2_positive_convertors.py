import os
import sys
# noinspection PyPackageRequirements
import pytest
# noinspection PyPackageRequirements
import json

cur_file_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = f'{cur_file_dir}/../fabrique_nodes_core'
sys.path.append(lib_dir)
os.chdir(cur_file_dir)

import tests.import_spoofer  # noqa: F401

from fabrique_nodes_core.convertors import jsons2model, schema2model, model2schema, model2ports
# from fabrique_nodes_core import Port, NodeConfig, BaseNode


def file2str(pth):
    with open(pth) as fp:
        txt = fp.read()
    return txt


street_schema = file2str(f'{cur_file_dir}/data/street_schema/schema.json')
street_data = file2str(f'{cur_file_dir}/data/street_schema/data.json')
nested_3f_7p = file2str(f'{cur_file_dir}/data/nested_3f_7p.json')

person_data = file2str(f'{cur_file_dir}/data/Person.json')

pets_jsons = [file2str(f'{cur_file_dir}/data/pet_jsons/{fn}') for fn
              in sorted(os.listdir(f'{cur_file_dir}/data/pet_jsons')) if '.json' in fn]


def badly_serialize_ports(ports):
    # deleted_schema_ports = []
    for port in ports:
        port.schema_ = ''

    return json.dumps([port.__dict__ for port in ports], default=str)


@pytest.fixture(params=["pet", "street"])
def jsons_schemas(request):
    if request.param == 'pet':
        jsons = pets_jsons
        expected_values = '''{"type": "object", "properties": {"name": {"title": "Name", "type": "string"}, "age": {"title": "Age", "type": "integer"}, "nickname": {"title": "Nickname", "type": "string"}, "job": {"$ref": "#/definitions/Job"}, "bones": {"title": "Bones", "type": "array", "items": {"$ref": "#/definitions/Bone"}}}, "required": ["name", "age"], "definitions": {"Job": {"title": "Job", "type": "object", "properties": {"type": {"title": "Type", "type": "string"}, "salary": {"title": "Salary", "type": "integer"}}, "required": ["type", "salary"]}, "Bone": {"title": "Bone", "type": "object", "properties": {"location": {"title": "Location", "type": "string"}, "size": {"title": "Size", "type": "string"}}, "required": ["location", "size"]}}}'''  # noqa: E501
    else:
        jsons = [street_data, ]
        expected_values = """{"type": "object", "properties": {"number": {"title": "Number", "type": "number"}, "street_name": {"title": "Street Name", "type": "string"}, "street_type": {"title": "Street Type", "type": "string"}}, "required": ["number", "street_name", "street_type"]}"""  # noqa: E501
    return jsons, expected_values


@pytest.fixture()
def schemas_models():
    street_schema
    expected_schema = '''{"title": "Model", "type": "object", "properties": {"number": {"title": "Number", "type": "number"}, "street_name": {"title": "Street Name", "type": "string"}, "street_type": {"$ref": "#/definitions/StreetType"}}, "definitions": {"StreetType": {"title": "StreetType", "description": "An enumeration.", "enum": ["Street", "Avenue", "Boulevard"]}}}'''  # noqa: E501
    return street_schema, expected_schema


@pytest.fixture(params=["pet", "street", "nested_3f_7p"])
def data_for_ports(request):
    if request.param == 'pet':
        jsons = pets_jsons
        schema = None
        expected_value = '''[{"id_": "root", "name": "", "type_": "object", "visible": true, "required": true, "special": false, "code": "", "schema_": ""}, {"id_": "name", "name": "name", "type_": "string", "visible": true, "required": true, "special": false, "code": "name", "schema_": ""}, {"id_": "age", "name": "age", "type_": "integer", "visible": true, "required": true, "special": false, "code": "age", "schema_": ""}, {"id_": "nickname", "name": "nickname", "type_": "string", "visible": true, "required": false, "special": false, "code": "nickname", "schema_": ""}, {"id_": "job", "name": "job", "type_": "object", "visible": true, "required": false, "special": false, "code": "job", "schema_": ""}, {"id_": "job.type", "name": "job.type", "type_": "string", "visible": true, "required": false, "special": false, "code": "job.type", "schema_": ""}, {"id_": "job.salary", "name": "job.salary", "type_": "integer", "visible": true, "required": false, "special": false, "code": "job.salary", "schema_": ""}, {"id_": "bones", "name": "bones", "type_": "array", "visible": true, "required": false, "special": false, "code": "bones", "schema_": ""}]'''  # noqa: E501
    elif request.param == 'street':
        jsons = [street_data, ]
        schema = street_schema
        expected_value = '''[{"id_": "root", "name": "", "type_": "object", "visible": true, "required": true, "special": false, "code": "", "schema_": ""}, {"id_": "number", "name": "number", "type_": "number", "visible": true, "required": false, "special": false, "code": "number", "schema_": ""}, {"id_": "street_name", "name": "street_name", "type_": "string", "visible": true, "required": false, "special": false, "code": "street_name", "schema_": ""}, {"id_": "street_type", "name": "street_type", "type_": "string", "visible": true, "required": false, "special": false, "code": "street_type", "schema_": ""}]'''  # noqa: E501
    else:
        jsons = [nested_3f_7p, ]
        schema = None
        expected_value = '''[{"id_": "root", "name": "", "type_": "object", "visible": true, "required": true, "special": false, "code": "", "schema_": ""}, {"id_": "f0_depth3", "name": "f0_depth3", "type_": "object", "visible": true, "required": true, "special": false, "code": "f0_depth3", "schema_": ""}, {"id_": "f0_depth3.f0_depth2", "name": "f0_depth3.f0_depth2", "type_": "object", "visible": true, "required": true, "special": false, "code": "f0_depth3.f0_depth2", "schema_": ""}, {"id_": "f0_depth3.f0_depth2.f0_depth1", "name": "f0_depth3.f0_depth2.f0_depth1", "type_": "string", "visible": true, "required": true, "special": false, "code": "f0_depth3.f0_depth2.f0_depth1", "schema_": ""}, {"id_": "f1_depth2", "name": "f1_depth2", "type_": "object", "visible": true, "required": true, "special": false, "code": "f1_depth2", "schema_": ""}, {"id_": "f1_depth2.f1_depth1", "name": "f1_depth2.f1_depth1", "type_": "string", "visible": true, "required": true, "special": false, "code": "f1_depth2.f1_depth1", "schema_": ""}, {"id_": "f2_depth1", "name": "f2_depth1", "type_": "string", "visible": true, "required": true, "special": false, "code": "f2_depth1", "schema_": ""}]'''   # noqa: E501

    return schema, jsons, expected_value, request.param


# @pytest.mark.skip("SKIP")
def test_jsons2models(jsons_schemas):
    jsons, expected_schema = jsons_schemas
    schema = model2schema(jsons2model(jsons))
    reserialized = json.dumps(json.loads(schema))
    print(reserialized)
    assert reserialized == expected_schema


# @pytest.mark.skip("SKIP")
def test_schemas2models(schemas_models):
    schema, expected_model = schemas_models
    assert json.dumps(schema2model(schema).schema()) == expected_model


# @pytest.mark.skip("SKIP")
def test_port_gen(data_for_ports):
    '''required fields, types'''
    schema, jsons, expected_value, _ = data_for_ports
    if schema:
        ports_out = model2ports(schema2model(schema))
    else:
        ports_out = model2ports(jsons2model(jsons))

    value = badly_serialize_ports(ports_out)
    assert value == expected_value, value


def test_port_gen_nill():
    '''required fields, types'''

    ports_out = model2ports(jsons2model([person_data, ]))
    value = badly_serialize_ports(ports_out)
    assert value == """[{"id_": "root", "name": "", "type_": "object", "visible": true, "required": true, "special": false, "code": "", "schema_": ""}, {"id_": "firstName", "name": "firstName", "type_": "string", "visible": true, "required": true, "special": false, "code": "firstName", "schema_": ""}, {"id_": "lastName", "name": "lastName", "type_": "string", "visible": true, "required": true, "special": false, "code": "lastName", "schema_": ""}, {"id_": "isAlive", "name": "isAlive", "type_": "bool", "visible": true, "required": true, "special": false, "code": "isAlive", "schema_": ""}, {"id_": "age", "name": "age", "type_": "integer", "visible": true, "required": true, "special": false, "code": "age", "schema_": ""}, {"id_": "address", "name": "address", "type_": "object", "visible": true, "required": true, "special": false, "code": "address", "schema_": ""}, {"id_": "address.streetAddress", "name": "address.streetAddress", "type_": "string", "visible": true, "required": true, "special": false, "code": "address.streetAddress", "schema_": ""}, {"id_": "address.city", "name": "address.city", "type_": "string", "visible": true, "required": true, "special": false, "code": "address.city", "schema_": ""}, {"id_": "address.state", "name": "address.state", "type_": "string", "visible": true, "required": true, "special": false, "code": "address.state", "schema_": ""}, {"id_": "address.postalCode", "name": "address.postalCode", "type_": "string", "visible": true, "required": true, "special": false, "code": "address.postalCode", "schema_": ""}, {"id_": "phoneNumbers", "name": "phoneNumbers", "type_": "array", "visible": true, "required": true, "special": false, "code": "phoneNumbers", "schema_": ""}, {"id_": "children", "name": "children", "type_": "array", "visible": true, "required": true, "special": false, "code": "children", "schema_": ""}, {"id_": "spouse", "name": "spouse", "type_": "any", "visible": true, "required": false, "special": false, "code": "spouse", "schema_": ""}]"""   # noqa: E501
