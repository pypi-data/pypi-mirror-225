#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TableIndex(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Index schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Index table is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Index name is null"

        self.Definition = (data.get("definition") or "")
        assert len(self.Definition) > 0, \
            "Index definition is null"

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table_index"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "INDEX"

    def DDL_Create(self, separator=" "):
        definition = self.Definition
        definition = definition.replace(" ON ",    separator+"ON ")
        definition = definition.replace(" USING ", separator+"USING ")
        definition = definition.replace(" (",      separator+"(")
        definition = definition.replace(" WHERE",  separator+"WHERE")
        definition = definition + ";"

        r = f"-- Index: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += definition

        return r.strip()

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def Diff(self, another):
        if self.Definition != another.Definition:
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
        else:
            return []
