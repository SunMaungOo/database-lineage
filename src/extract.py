from database import get_connection_string,test_connection
from config import HOST_NAME,DATABASE_NAME,USER_NAME,PASSWORD,PORT,OUTPUT_FILE_PATH,IS_USE_FQN
import logging
import sys
from connector import get_view_lineage,get_procedure_lineage
from graph import merge_edges
from dataclasses import asdict
import json
from pathlib import Path
from graph import Edge
from typing import List

logger = logging.getLogger("database-lineage")

logger.setLevel(logging.DEBUG)

logger.propagate = False

formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)-8s | %(name)-15s | %(lineno)-3d | %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S' 
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def main()->int:

    connection_str = get_connection_string(host=HOST_NAME,\
                          database_name=DATABASE_NAME,\
                          user=USER_NAME,\
                          password=PASSWORD,\
                          port=PORT)
    
    logger.info("Testing connection to database")
    
    is_db_connected = test_connection(connection_str=connection_str)

    if not is_db_connected:
        logger.info("Cannot connect to the database.Please check the database configuration")
        return -1
    
    else:
        logger.info("Connection to database success")

    logger.info("Extracting view lineage")

    view_lineages = get_view_lineage(connection_str=connection_str,\
                           host=HOST_NAME,\
                           database=DATABASE_NAME,\
                           is_fqn=IS_USE_FQN)
    
    if view_lineages is None:
        logger.info("Extracting view lineage:fail")
        return -1

    logger.info("Extracting view lineage:sucesss")

    logger.info(f"View lineage Extracted:{len(view_lineages)}")


    logger.info("Extracting procedure lineage")

    procedure_lineages = get_procedure_lineage(connection_str=connection_str,\
                           host=HOST_NAME,\
                           database=DATABASE_NAME,\
                           is_fqn=IS_USE_FQN)
    
    if procedure_lineages is None:
        logger.info("Extracting procedure lineage:fail")
        return -1

    logger.info("Extracting procedure lineage:sucesss")

    logger.info(f"Procedure lineage Extracted:{len(procedure_lineages)}")

    lineages:List[List[Edge]] = list()
    lineages.append(view_lineages)
    lineages.append(procedure_lineages)
    
    lineages = merge_edges(graphs=lineages)

    logger.info(f"Total lineage Extracted:{len(lineages)}")

    try:

        Path(OUTPUT_FILE_PATH).parent.mkdir(parents=True,exist_ok=True)

        with open(OUTPUT_FILE_PATH,"w") as file:
            json.dump([asdict(lineage) for lineage in lineages],file,indent=4)

        logger.info(f"Saving lineage to {OUTPUT_FILE_PATH}:success")
    
    except:
        logger.info(f"Saving lineage to {OUTPUT_FILE_PATH}:fail")

        return 1

    return 0

if __name__=="__main__":
    sys.exit(main())