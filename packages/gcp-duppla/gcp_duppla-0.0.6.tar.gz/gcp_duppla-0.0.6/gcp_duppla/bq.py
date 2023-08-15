import os
from google.cloud import bigquery as gcp_bq
import google.auth
import pandas_gbq as pdgbq
import pandas as pd
from src import entities


class bigquery:
    def __init__(self, gcp_cred_location: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_cred_location
        self.credentials, self.project = google.auth.default(entities.SCOPES)
        pdgbq.context.credentials = self.credentials

        self.client = gcp_bq.Client(self.project, self.credentials)

        # setting the default job config
        self.job_config = gcp_bq.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=gcp_bq.SourceFormat.CSV,
        )

    # moving a file from GCS to BQ
    def gcs_to_bq(self, file_uri: str, table_id: str) -> None:
        load_job = self.client.load_table_from_uri(
            file_uri, table_id, job_config=self.job_config
        )
        load_job.result()

    # uploading a list[dict] to BQ
    def json_to_bq(self, table_id: str, df_json: list[dict]) -> None:
        errors = self.client.insert_rows_json(
            table_id, df_json, row_ids=[None] * len(df_json)
        )
        if errors == []:
            print("Files uploaded successfully.")
        else:
            print("Error inserting rows: {}".format(errors))

    # executing a query on BQ
    def exec_on_bq(self, query: str) -> None:
        job = self.client.query(query)
        return print(job.result())

    # executing a query on BQ and returning a pandas dataframe
    def bq_to_df(self, query: str) -> pd.DataFrame:
        pdgbq.context.credentials = self.credentials
        self.client = gcp_bq.Client(self.project, self.credentials)
        return pd.read_gbq(query, self.project)
