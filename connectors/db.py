import json
import kuzu
from pandas import DataFrame

class GraphDBBackend():

    def __init__(self, file_name: str) -> None:
        if file_name is None:
            raise("Please specify a file name")
        
        self.db = kuzu.Database(file_name)
        self.conn = kuzu.Connection(self.db)
        self.__generate_schema()

    def execute_query(self, query: str) -> dict:
        response = ""
        try:
            qr = self.conn.execute(query)
            df: DataFrame = qr.get_as_df()
            response = json.loads(df.to_json(orient='records'))
        except:
            response = {"error": "Sorry, I did not understand your question. Please try rephrasing your question."}

        return response
    
    def __generate_schema(self):
        node_properties = []
        node_table_names = self.conn._get_node_table_names()
        for table_name in node_table_names:
            current_table_schema = {"properties": [], "label": table_name}
            properties = self.conn._get_node_property_names(table_name)
            for property_name in properties:
                property_type = properties[property_name]["type"]
                list_type_flag = ""
                if properties[property_name]["dimension"] > 0:
                    if "shape" in properties[property_name]:
                        for s in properties[property_name]["shape"]:
                            list_type_flag += "[%s]" % s
                    else:
                        for i in range(properties[property_name]["dimension"]):
                            list_type_flag += "[]"
                property_type += list_type_flag
                current_table_schema["properties"].append(
                    (property_name, property_type)
                )
            node_properties.append(current_table_schema)

        relationships = []
        rel_tables = self.conn._get_rel_table_names()
        for table in rel_tables:
            relationships.append(
                "(:%s)-[:%s]->(:%s)" % (table["src"], table["name"], table["dst"])
            )

        # rel_properties = []
        # for table in rel_tables:
        #     table_name = table["name"]
        #     current_table_schema = {"properties": [], "label": table_name}
        #     query_result = self.conn.execute(f"CALL table_info('{table_name}') RETURN *;")
        #     while query_result.has_next():
        #         row = query_result.get_next()
        #         prop_name = row[1]
        #         prop_type = row[2]
        #         current_table_schema["properties"].append(
        #             (prop_name, prop_type)
        #         )      
        #     rel_properties.append(current_table_schema)

        self.schema = (
            f"Node properties: {node_properties}\n"
            # f"Relationships properties: {rel_properties}\n"
            f"Relationships: {relationships}\n"
        )

        print(self.schema)