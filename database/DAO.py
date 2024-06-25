from database.DB_connect import DBConnect

from model.location import Location


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_providers():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct nwhl.Provider from nyc_wifi_hotspot_locations nwhl order by nwhl.Provider """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['Provider'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_nodes(provider):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select nwhl.Location , nwhl.Latitude , nwhl.Longitude
        from nyc_wifi_hotspot_locations nwhl 
        where nwhl.Provider = %s
        group by nwhl.Location """
        cursor.execute(query, (provider,))
        result = []
        for row in cursor:
            result.append(Location(**row))
        cursor.close()
        cnx.close()
        return result
