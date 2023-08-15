import pyodbc as odbc


class Connection:
    def __init__(self, server, database):
        self.str = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';' + 'Trusted_Connection=yes')
