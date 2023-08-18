from google.cloud import bigquery
from google.cloud.exceptions import NotFound


def save_data_to_bq(insert_df, dataset_id, table_id):
    try:
        client = bigquery.Client()
        # 資料表參數
        table_ref = client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job = client.load_table_from_dataframe(insert_df, table_ref, job_config=job_config)
        job.result()
    except Exception as e:
        raise e


def query_multiple_data_from_bq(sql_list, data_name):
    try:
        client = bigquery.Client()
        result_dict = {}
        for sql, alias in zip(sql_list, data_name):
            results = client.query(sql)
            df = results.to_dataframe()
            result_dict[alias] = df
    except Exception as e:
        raise e
    return result_dict


def check_table_exist(table_id):
    client = bigquery.Client()

    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
    except NotFound:
        print("Table {} is not found.".format(table_id))


def create_table(table_name, columns, types, modes=None):
    client = bigquery.Client()

    if modes:
        schema = [bigquery.SchemaField(col, t, mode=mode) for col, t, mode in zip(columns, types, modes)]
    else:
        schema = [bigquery.SchemaField(col, t, mode="REQUIRED") for col, t in zip(columns, types)]
    table = bigquery.Table(table_name, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )


def get_table_info(dataset, table_name):
    client = bigquery.Client()
    # table_id = 'your-project.your_dataset.your_table'
    full_table_id = f'{dataset}.{table_name}'
    table = client.get_table(full_table_id)
    # print("Table schema: {}".format(table.schema))
    # print("Table description: {}".format(table.description))
    # print("Table has {} rows".format(table.num_rows))
    return table.schema

