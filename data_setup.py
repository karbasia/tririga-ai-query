import kuzu

db = kuzu.Database('./location_data')
conn = kuzu.Connection(db)

conn.execute("CREATE NODE TABLE Space(id STRING, name STRING, spaceClass STRING, area FLOAT, PRIMARY KEY (id))")
conn.execute("CREATE NODE TABLE Floor(id STRING, name STRING, level INT32, PRIMARY KEY (id))")
conn.execute("CREATE NODE TABLE Building(id STRING, name STRING, PRIMARY KEY (id))")
conn.execute("CREATE REL TABLE SpaceChildOfFloor(FROM Space TO Floor, MANY_ONE)")
conn.execute("CREATE REL TABLE FloorChildOfBuilding(FROM Floor TO Building, MANY_ONE)")
conn.execute("CREATE REL TABLE SpaceChildOfBuilding(FROM Space TO Building, MANY_ONE)")

conn.execute('COPY Space FROM "./test_data/space.csv";')
conn.execute('COPY Floor FROM "./test_data/floor.csv";')
conn.execute('COPY Building FROM "./test_data/building.csv";')
conn.execute('COPY SpaceChildOfFloor FROM "./test_data/space_to_floor.csv";')
conn.execute('COPY FloorChildOfBuilding FROM "./test_data/floor_to_building.csv";')
conn.execute('COPY SpaceChildOfBuilding FROM "./test_data/space_to_building.csv";')