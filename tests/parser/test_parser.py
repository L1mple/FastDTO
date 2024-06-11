import pytest

from fastdto.common.dto import ColumnDTO
from fastdto.common.enums import ColumnTypeEnum, PythonTypeEnum
from fastdto.core.dsl.parse.service import parse_query
from tests.utils import patch_schema_for_test

test_schema = {
    "buildings": {
        "building_id": ColumnTypeEnum.INTEGER,
        "building_name": ColumnTypeEnum.VARCHAR,
        "location": ColumnTypeEnum.VARCHAR,
    },
    "employees": {
        "employee_id": ColumnTypeEnum.INTEGER,
        "name": ColumnTypeEnum.VARCHAR,
        "position": ColumnTypeEnum.VARCHAR,
        "building_id": ColumnTypeEnum.INTEGER,
    },
}


@patch_schema_for_test(user_schema=test_schema)
@pytest.mark.parametrize(
    "sql_query, parse_result",
    [
        (
            "SELECT * FROM buildings",
            [
                ColumnDTO(name="building_id", python_type=PythonTypeEnum.INT),
                ColumnDTO(name="building_name", python_type=PythonTypeEnum.STR),
                ColumnDTO(name="location", python_type=PythonTypeEnum.STR),
            ],
        )
    ],
)
def test_parser(sql_query, parse_result):
    """Test example for users."""
    result = parse_query(
        query=sql_query,
    )
    assert result.result_columns == parse_result
