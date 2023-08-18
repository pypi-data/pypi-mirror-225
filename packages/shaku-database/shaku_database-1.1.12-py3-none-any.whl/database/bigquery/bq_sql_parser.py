import re

from typing import NamedTuple, Dict, List


class TableInfo(NamedTuple):
    unique_keys: List
    date_time_col: str


def replace_table_names(sql, replacement, table_info_dict):
    from_pattern = r"(?i)\bFROM\s+([^\s()]+)"
    join_pattern = r"(?i)\bJOIN\s+([^\s()]+)"
    for parse_name, pattern in zip(["FROM", 'JOIN'], [from_pattern, join_pattern]):
        for i in re.finditer(pattern, sql):
            group = i.group()
            table_name = group.split(" ")[-1]
            only_table_name = table_name.split(".")[-1]
            table_info = table_info_dict[only_table_name]
            sql = re.sub(pattern,
                         r"{0} ({1})".format(parse_name,
                                             replacement.format(unique_keys=",".join(table_info.unique_keys),
                                                                date_time_col=table_info.date_time_col,
                                                                table=table_name)), sql)
    return sql


def generate_sql_for_bq(sql, table_info: Dict[str, TableInfo]):
    format_sql = """
    SELECT * FROM (
          SELECT
              *,
              ROW_NUMBER()
                  OVER (PARTITION BY {unique_keys} order by {date_time_col} desc)
                  as row_number
          FROM {table}
        )
        WHERE row_number = 1
    """
    result_sql = replace_table_names(sql, format_sql, table_info)
    return result_sql
