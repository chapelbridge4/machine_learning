import sqlite3

class TestDb:
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
    
    # Create Table
    def create_table(self, table_name: str, columns: list):
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(create_table_query)
        self.connection.commit()
    
    # Read Data
    def read_data(self, table_name: str, columns: list = None, condition: str = None):
        if columns is None:
            columns_str = "*"
        else:
            columns_str = ', '.join(columns)
        
        query = f"SELECT {columns_str} FROM {table_name}"
        
        if condition:
            query += f" WHERE {condition}"
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # Update Data
    def update_data(self, table_name: str, set_values: dict, condition: str):
        set_values_str = ', '.join([f"{key} = ?" for key in set_values.keys()])
        update_query = f"UPDATE {table_name} SET {set_values_str} WHERE {condition}"
        
        self.cursor.execute(update_query, tuple(set_values.values()))
        self.connection.commit()
    
    # Delete Data
    def delete_data(self, table_name: str, condition: str):
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(delete_query)
        self.connection.commit()
    
    # Shutdown
    def shutdown(self):
        self.connection.close()