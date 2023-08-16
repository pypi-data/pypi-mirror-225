from mct_dc import MCT
from mct_err import *
from dataclasses import dataclass
import time
import pymongo
from pymongo import MongoClient


class MONGO_DB_CONN:
    """
    Databases are databases
    Collections are tables
    Can use dict syntax to access relevant colllections
    list_collection_names
    """

    def __init__(self, mongo_url):
        self.mongo_url = mongo_url
        self.conn = None
        self.db = None
        self.known_collections = None
        self.db_types = {}
        

    def get_db(self) -> None:
        if not self.conn:
            self.conn = MongoClient(self.mongo_url)
        if not self.db:
            self.db = self.conn.adc #assuming we are naming our relevant database adc for aide de campe
        return self.db


    def check_collection_ext(self, name):
        if name not in self.known_collections:
            self.known_collections = self.db.list_collection_names()
        return name in self.known_collections

    def approve_type(self, obj_type: dataclass):
        #print("obj_type: ", obj_type, " -> name: ", obj_type.__name__.lower())

        name = obj_type.__name__.lower()
        schema = obj_type.__annotations__
        if not issubclass(obj_type, MCT): #isinstance is for instantiated objects foo
            raise MCT_TYPE_ERROR(name, "approve_type")
        
        self.db_types[name] = schema

        if not self.check_collection_ext(name):
            print("Collection was not found and will be created")
            temp = self.db[name] #should side effect create collection
        else:
            print("Collection was found")
            
        
    # CREATE
    def insert_obj(self, spec_obj: object):
        name = type(spec_obj).__name__.lower()  

        if not isinstance(spec_obj, MCT):
            raise MCT_TYPE_ERROR(name, "insert")
        elif spec_obj.__dict__["id"] != -1:
            self.update_obj(spec_obj)
            return spec_obj.__dict__["id"]

        row_id = None
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

        row_ids = []

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

        succ = False 
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

        succ = False
        return succ

    #READ
    def get_obj_by_id(self, obj_type: dataclass, id: int):
        name = obj_type.__name__.lower()

        if not issubclass(obj_type, MCT):
            raise MCT_TYPE_ERROR(name, "get_obj_by_id")
        
        results = {}
        return obj_type(*results)
        

    def get_objs_by_dict(self, obj_type: dataclass, query_filters: dict):
        #for between, just pass tuple instead of val
        name = obj_type.__name__.lower()

        if not issubclass(obj_type, MCT):
            raise MCT_TYPE_ERROR(name, "get_obj_by_id")
      
        results = []
        return [obj_type(*x) for x in results]


            

