from src.data_types.base_dc import MCT
from ..error_types.mct_err import *
from dataclasses import dataclass
import time
import psycopg2
from psycopg2.extras import DictCursor
import os


class PSQL_DB:
    """
    Warning: PSQL automatically undercases table names, so checkext may be hairy
    """
    def __init__(self):
        self.db_types = {}
        self.object_sql_commands = {}
        self.conn = None
        self.py2psql_type_dict = {
            str: "text",
            int: "integer",
            float: "double precision",
            bool: "boolean",
        }
        self.psql2py_type_dict = {
            "text": str,
            "integer": int,
            "double precision": float,
            "boolean": bool,
        }

    def get_conn(self) -> psycopg2.extensions.connection:
        if not self.conn:
            self.conn = psycopg2.connect(
                host="localhost", database="adc", user="postgres", password=""
            )
        return self.conn

    def approve_type(self, obj_type: dataclass):
        #print("obj_type: ", obj_type, " -> name: ", obj_type.__name__.lower())

        name = obj_type.__name__.lower()
        schema = obj_type.__annotations__

        if not issubclass(obj_type, MCT): #isinstance is for instantiated objects foo
            raise MCT_TYPE_ERROR(name, "approve_type")
        
        self.db_types[name] = schema
        self.object_sql_commands[name] = {}

        if not self.table_exists(name): 
            print("Table " + name + " doesn't exist. Creating now.")
            self.create_table(name, schema)
            
        elif not self.schema_matches_table(schema, name):
            print("Table " + name + " exists but doesn't match schema. Versioning.")
            self.version_table_on_schema_conflict(name)
            self.create_table(name, schema)
        else:
            print("Table " + name + " exists and matches schema")

    # Creation
    def create_table(self, table_name: str, table_schema: dict) -> bool:
        phrase_list = ["id SERIAL PRIMARY KEY"]
        for key, val in table_schema.items():
            if val == bool:
                phrase_list.append(key + " BOOL")
            elif val == int:
                phrase_list.append(key + " INTEGER")
            elif val == float:
                phrase_list.append(key + " DOUBLE PRECISION")
            elif val == str:
                phrase_list.append(key + " TEXT")

        arg_string = ", ".join(phrase_list)
        create_query = "CREATE TABLE " + table_name + "( " + arg_string + ")"

        conn = self.get_conn()
        cursor = conn.cursor()

        succ = True
        try:
            cursor.execute(create_query)
            conn.commit()
        except Exception as e:
            succ = False
            print(e)

        return succ

    # Existence and comparison
    def table_exists(self, table_name: str) -> bool:
        conn = self.get_conn()
        cursor = conn.cursor()
        exists = False

        ext_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{}')".format(
            table_name
        )
        try:
            cursor.execute(ext_query)
            exists = cursor.fetchone()[0]
        except Exception as e:
            print(e)
            # print("Unsure whether table exists, do not overwrite")
            exists = True
        cursor.close()
        return exists

    def schema_matches_table(self, table_schema: dict, table_name: str):
        """
        Remember to handle id dict component 8/6
        """
        spec_query = (
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='"
            + table_name
            + "'"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        result = None
        try:
            cursor.execute(spec_query)
            result = cursor.fetchall()
        except Exception as e:
            print(e)

        cursor.close()

        table_schema_dict = {
            x[0]: self.psql2py_type_dict[x[1]] for x in result if x[0] != "id"
        }
        return table_schema == table_schema_dict

    def version_table_on_schema_conflict(self, table_name: str) -> tuple:
        """
        Occurs on various collisions between approved data schema, existing schema for data name, and sql table for data name
        """
        current_unix_time = int(time.time())
        new_table_name = table_name + "_" + str(current_unix_time)
        version_query = "ALTER TABLE {} RENAME TO {}".format(table_name, new_table_name)

        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(version_query)
            conn.commit()
        except Exception as e:
            print(e)
            new_table_name = table_name

        cursor.close()

        return (table_name, new_table_name)

    # CREATE
    def insert_obj(self, spec_obj: object):
        """
        Insert this object.
        Row id is tricky. Talk to Jon. Thinking hanging index of last
        """
        name = type(spec_obj).__name__.lower()  # the name is attached to the type declaration

        if not isinstance(spec_obj, MCT):
            raise MCT_TYPE_ERROR(name, "insert")
        elif spec_obj.__dict__["id"] != -1:
            #upsert pathing re jon
            self.update_obj(spec_obj)
            return spec_obj.__dict__["id"]

        if "insert" not in self.object_sql_commands[name]:  # we know dict exists
            key_string, val_string = self.feature_chains(spec_obj)
            self.object_sql_commands[name]["insert_obj"] = (
                "INSERT INTO "
                + name
                + "("
                + key_string
                + ") VALUES ("
                + val_string
                + ") RETURNING id"
            )
        insert_query = self.object_sql_commands[name]["insert_obj"]

        conn = self.get_conn()
        cursor = conn.cursor()
        row_id = None

        try:
            cursor.execute(insert_query, spec_obj.__dict__)
            row_id = cursor.fetchone()[0]
        except Exception as e:
            print(e)
            print("MCT_INS_ERR")

        conn.commit()
        cursor.close()

        spec_obj.__dict__["id"] = row_id
        return row_id


    def insert_objs(self, spec_objs: list[object]) -> list[int]:
        """
        Read about mogrify briefly - performant pregen queries 
        """
        spec_obj = spec_objs[0]
        keys = spec_obj.__annotations__.keys()
        name = type(spec_obj).__name__.lower()  # the name is attached to the type declaration

        if not all(isinstance(obj, MCT) for obj in spec_objs):
            raise MCT_TYPE_ERROR(name, "insert_objs")

        if "insert_objs" not in self.object_sql_commands[name]:  # we know dict exists
            self.object_sql_commands[name]["insert_objs"] = (
                "INSERT INTO "
                + name
                + " ("
                + self.get_obj_keys(spec_obj)
                + ") VALUES " + 
                "{}"
                + " RETURNING id"
            )
        
        mog_chain = [tuple([obj.__dict__[x] for x in keys]) for obj in spec_objs]
        premog = self.object_sql_commands[name]["insert_objs"].format(", ".join(["%s"]*len(spec_objs)))

        conn = self.get_conn()
        cursor = conn.cursor()
        insert_query = cursor.mogrify(premog, mog_chain)
        row_ids = []
        try:
            cursor.execute(insert_query)
            row_ids = cursor.fetchall()
        except Exception as e:
            print(e)
            print("MCT_MULT_INS_ERR")
        
        conn.commit()
        cursor.close()


        for i in range(len(spec_objs)):
            spec_objs[i].__dict__["id"] = row_ids[i]
        return row_ids


    # UPDATE
    def update_obj(self, spec_obj: object) -> bool:  # ?
        """
        Trying to 2-param the execute query has been mystifying.
        Going with this for now.
        """
        name = type(spec_obj).__name__.lower()

        if not isinstance(spec_obj, MCT):
            raise MCT_TYPE_ERROR(name, "update_obj")
        elif spec_obj.__dict__["id"] == -1:  
            #maybe the opposite of upsert, indate?
            raise MCT_INDEX_ERROR(name, "update_obj")

        if "update_obj" not in self.object_sql_commands[name]:
            arg_string = self.arg_chain(spec_obj)
            self.object_sql_commands[name]["update_obj"] = "UPDATE " + name + " SET " + arg_string + " WHERE id={id}"

        update_query = self.object_sql_commands[name]["update_obj"].format(**spec_obj.__dict__)

        conn = self.get_conn()
        cursor = conn.cursor()
        succ = True

        try:
            cursor.execute(update_query)
        except Exception as e:
            succ = False
            print(e)
            print("MCT_UPD_ERR")

        conn.commit()
        cursor.close()
        return succ

    # DELETE
    def delete_obj(self, spec_obj: object) -> bool:
        """
        See update w/rt 2-param exec query
        """
        name = type(spec_obj).__name__.lower()

        if not isinstance(spec_obj, MCT):
            raise MCT_TYPE_ERROR(name, "delete_obj")
        elif spec_obj.__dict__["id"] == -1:
            raise MCT_DELETED_ERROR(name)

        if "delete_obj" not in self.object_sql_commands[name]:
            self.object_sql_commands[name]["delete_obj"] = (
                "DELETE FROM " + name + " WHERE id={id}"
            )
        del_query = self.object_sql_commands[name]["delete_obj"].format(**spec_obj.__dict__)

        succ = True
        conn = self.get_conn()
        with conn.cursor() as cursor:
            try:
                cursor.execute(del_query)
            except Exception as e:
                succ = False
                print(e)
                print("MCT_DEL_ERR")

        spec_obj.__dict__["id"] = -1
        return succ

    #READ
    def get_obj_by_id(self, obj_type: dataclass, id: int):
        name = obj_type.__name__.lower()

        if not issubclass(obj_type, MCT):
            raise MCT_TYPE_ERROR(name, "get_obj_by_id")
        if name not in self.object_sql_commands:
            print("Handle this error")
            pass
        
        if "get_obj_by_id" not in self.object_sql_commands[name]:
            self.object_sql_commands[name]["get_obj_by_id"] = (
                "SELECT * FROM " + name + " WHERE id="
            )
        sel_query = self.object_sql_commands[name]["get_obj_by_id"] + str(id)
        results = {}
        
        conn = self.get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            try:
                cursor.execute(sel_query)
                results = cursor.fetchone() #if card fetchall>1 => issue
            except Exception as e:
                print(e)
                print("MCT_ID_GET_ERROR")

        return obj_type(*results)
        




    def get_objs_by_dict(self, obj_type: dataclass, query_filters: dict):
        #for between, just pass tuple instead of val
        name = obj_type.__name__.lower()

        if not issubclass(obj_type, MCT):
            raise MCT_TYPE_ERROR(name, "get_obj_by_id")
        if name not in self.object_sql_commands:
            print("Handle this error")
            pass
        
        if "get_objs_by_id" not in self.object_sql_commands[name]:
            self.object_sql_commands[name]["get_objs_by_id"] = (
                "SELECT * FROM " + name + " WHERE {}"
            )
        sel_dict_query = self.object_sql_commands[name]["get_objs_by_id"].format(self.get_filters(query_filters))
        print("sel_dict query: ", sel_dict_query)
        results = []
        
        conn = self.get_conn()
        with conn.cursor() as cursor:
            args = cursor.mogrify

            try:
                cursor.execute(sel_dict_query)
                results = cursor.fetchall()
            except Exception as e:
                print(e)
                print("MCT_GET_ERROR")
        
        return [obj_type(*x) for x in results]

    def get_obj_keys(self, spec_obj: object) -> str:
        return ", ".join([x for x in spec_obj.__annotations__.keys()])

    # Query generation tools
    def feature_chains(self, spec_obj: object) -> tuple:
        """
        Note: Objects all need to have default vals
        """
        key_list, val_list = [], []
        for key, _ in spec_obj.__dict__.items():
            if key != "id":
                key_list.append(key)
                val_list.append("%(" + key + ")s")
        return (", ".join([x for x in key_list]), ", ".join([x for x in val_list]))

    def arg_chain(self, spec_obj: object) -> str:
        val_list = []
        for key, _ in spec_obj.__dict__.items():
            if key != "id":
                val_list.append(key + "={" + key + "}")

        return ", ".join([x for x in val_list])
    
    def get_filters(self, filter_dict: dict) -> str:
        filter_arr = []
        for key, val in filter_dict.items():
            if(type(val))==str:
                filter_arr.append(key+"='"+val+"'")
            else:
                filter_arr.append(key+"="+str(val))
        return "AND ".join([x for x in filter_arr])
            

