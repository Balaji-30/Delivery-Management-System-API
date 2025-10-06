import sqlite3

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRead


class Database():

    def connect_to_db(self):
        self.con=sqlite3.connect("sqlite.db",check_same_thread=False)
        self.cur=self.con.cursor()
        
    def create_table(self):
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS shipment (
                         id INTEGER PRIMARY KEY,
                         content TEXT,
                         weight REAL,
                         status TEXT
                         )
                         """)
    
    def create(self,shipment:ShipmentCreate)-> int:
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result= self.cur.fetchone()
        print('********\n',result)
        new_id= result[0]+1 if result[0] is not None else 0
        self.cur.execute(""" 
            INSERT INTO shipment VALUES
            (:id, :content, :weight, :status)
        """,
            {
                "id":new_id,
                **shipment.model_dump(),
                "status":"placed"
            })
        self.con.commit()
        return new_id
    
    def get(self, id:int)-> ShipmentRead | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id = ? 
            """, (id,)   )
        
        row=self.cur.fetchone()
     
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3],
        } if row else None

    def update(self,id:int, shipment:ShipmentUpdate)->ShipmentRead:
        self.cur.execute("""
            UPDATE shipment SET status= :status 
            WHERE id= :id
        """,{
            "id":id,
            **shipment.model_dump()
        })
        self.con.commit()
        return self.get(id)

    def delete(self, id:int):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = :id       
                         """,
                         (id,))
        self.con.commit()
    
    def close(self):
        self.con.close()
    
    def __enter__(self):
        self.connect_to_db()
        self.create_table()
        return self

    def __exit__(self, *arg):
        self.close()




# import json

# shipments={}

# print("before load:",shipments)
# with open("shipments.json") as json_file:
#     data=json.load(json_file)

#     for item in data:
#         shipments[item["id"]]=item
    

# print("after load:",shipments)

# def save():
#     with open("shipments.json","w") as json_file:
#         json.dump(
#             list(shipments.values()),
#             json_file
#         )