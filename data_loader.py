import sqlite3
import os
import time
from typing import Any, Optional
import sys


def connect_to_database(db_path: str, retries: int = 5, delay: float = 2) -> Optional[sqlite3.Connection]:
    """
    Versucht, eine Verbindung zu einer SQLite-Datenbank herzustsellen. 
    Bei einem Fehler wird die Verbindung bis zu 'retries'-Mal wiederholt, mit "delay" Sekunden Verzögerung.
    """

    for attempt in range(retries):
        try:
            conn = sqlite3.connect(db_path)   
            print(f"Connected to the database '{db_path}' on attempt {attempt + 1}.")
            return conn
        
        except sqlite3.Error as e:
            print(f"Failed to connect to the database on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed.")
                return None
    
    return None

    

def main() -> None:

    db_path = '/home/daniel/work_bosch_security_systems/rosbag3DTraffic/rosbag3DTraffic_0.db'

    conn = connect_to_database(db_path=db_path)

    if conn is None:
        print("Verbindung zur Datenkbank konnte nicht hergestellt werden. Programm wird beendet.")
        sys.exit(1)

    print("Verbindung konnte erfolgreich hergestellt werden.")

    conn.close()


if __name__ == "__main__":
    main()