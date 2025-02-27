import sys
from google.cloud import bigquery

# TODO : Change to your project id
PROJECT_ID = "packt-data-eng-on-gcp"
TARGET_TABLE_ID = "{}.dwh_bikesharing.fact_trips_daily".format(PROJECT_ID)

def create_fact_table(PROJECT_ID, TARGET_TABLE_ID):
    load_date = sys.argv[1] # date format : yyyy-mm-dd
    print("\nLoad date:", load_date)

    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(
    destination=TARGET_TABLE_ID,
    write_disposition='WRITE_APPEND')

    sql = """SELECT DATE(start_date) as trip_date,
                 start_station_id,
                 COUNT(trip_id) as total_trips,
                 SUM(duration_sec) as sum_duration_sec,
                 AVG(duration_sec) as avg_duration_sec
                 FROM `{PROJECT_ID}.raw_bikesharing.trips` trips
                 JOIN `{PROJECT_ID}.raw_bikesharing.stations` stations
                 ON trips.start_station_id = stations.station_id
                 WhERE DATE(start_date) = DATE('{load_date}')
                 GROUP BY trip_date, start_station_id
                 ;""".format(PROJECT_ID=PROJECT_ID, load_date=load_date)

    query_job = client.query(sql, job_config=job_config)

    try:
        query_job.result()
        print("Query success")
    except Exception as exception:
            print(exception)

if __name__ == '__main__':
    create_fact_table(PROJECT_ID, TARGET_TABLE_ID)
