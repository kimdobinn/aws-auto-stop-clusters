import boto3
import json
import time

def lambda_handler(event, context):
    rds_service = boto3.client('rds', region_name='ap-southeast-2')
    all_clusters = rds_service.describe_db_clusters()['DBClusters']

    excluded_rds_clusters = ['au-islhd-stg-db-cluster']
    excluded_docdb_clusters = ['au-islhd-stg-docdb-cluster']

    rds_clusters = [c for c in all_clusters if 'aurora' in c['Engine'] and c['DBClusterIdentifier'] not in excluded_rds_clusters]
    docdb_clusters = [c for c in all_clusters if 'docdb' in c['Engine'] and c['DBClusterIdentifier'] not in excluded_docdb_clusters]

    numberOfRDS = len(rds_clusters)
    numberOfDocDB = len(docdb_clusters)

    print('There are ' + str(numberOfRDS) + ' Aurora RDS clusters.')
    print('There are ' + str(numberOfDocDB) + ' DocumentDB clusters.')
    print('Booting up ' + str(numberOfRDS) + ' Aurora RDS clusters and ' + str(numberOfDocDB) + ' DocumentDB clusters...')

    for c in rds_clusters + docdb_clusters:
        cluster_info = rds_service.describe_db_clusters(DBClusterIdentifier=c['DBClusterIdentifier'])['DBClusters'][0]
        status = cluster_info['Status']
        if status == 'stopped':
            rds_service.start_db_cluster(DBClusterIdentifier=c['DBClusterIdentifier'])
        else:
            print(f"Skipping start for {c['DBClusterIdentifier']} (status: {status})")


    waitingRDS = 0
    doneRDS = 0
    waitingDocDB = 0
    doneDocDB = 0

    def updateCount(goal):
        incompleteRDS = 0
        completeRDS = 0
        incompleteDocDB = 0
        completeDocDB = 0

        for c in rds_clusters:
            cluster_info = rds_service.describe_db_clusters(DBClusterIdentifier=c['DBClusterIdentifier'])['DBClusters'][0]
            status = cluster_info['Status']
            if(status == goal):
                completeRDS += 1
            else:
                incompleteRDS += 1
        
        for c in docdb_clusters:
            cluster_info = rds_service.describe_db_clusters(DBClusterIdentifier=c['DBClusterIdentifier'])['DBClusters'][0]
            status = cluster_info['Status']
            if(status == goal):
                completeDocDB += 1
            else:
                incompleteDocDB += 1
        
        return(incompleteRDS, completeRDS, incompleteDocDB, completeDocDB)

    def printCount(goal):
        if goal == "available":
            antigoal = "starting"
        elif goal == "stopped" or goal == "stopped temporarily":
            antigoal = "stopping"

        print(str(waitingRDS + waitingDocDB) + " clusters are " + antigoal + ".")
        print(str(doneRDS + doneDocDB) + " clusters are " + goal + ".")
        print("Waiting 15 more seconds before checking again.")
        print("***************************************************")

    waitingRDS, doneRDS, waitingDocDB, doneDocDB = updateCount("available")
    printCount("available")

    while doneRDS < numberOfRDS or doneDocDB < numberOfDocDB:
        waitingRDS, doneRDS, waitingDocDB, doneDocDB = updateCount("available")
        printCount("available")
        time.sleep(15)

    printCount("available")
    print("All the clusters are available. Shutting them down now.")

    for c in rds_clusters + docdb_clusters:
        rds_service.stop_db_cluster(DBClusterIdentifier=c['DBClusterIdentifier'])

    return {
        'statusCode': 200
    }