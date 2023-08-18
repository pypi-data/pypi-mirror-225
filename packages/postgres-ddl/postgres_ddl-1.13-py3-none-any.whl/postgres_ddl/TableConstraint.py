#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TableConstraint(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Constraint schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Constraint table is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Constraint name is null"

        self.Type = (data.get("type") or "").strip().lower()
        assert len(self.Type) > 0, \
            "Constraint type is null"

        self.IsForeignKey = (self.Type == "f")

        self.OrderNum = data.get("order_num") or 6

        self.SortKey = f"{self.OrderNum}_{self.GetFullName()}"

        self.Definition = (data.get("definition") or "")
        assert len(self.Definition) > 0, \
            "Constraint definition is null"

        self.UpdateAction = (data.get("update_action") or "").strip().upper()

        self.DeleteAction = (data.get("delete_action") or "").strip().upper()

        self.MatchAction = (data.get("match_action") or "").strip().upper()

        self.DeferrableType = (data.get("deferrable_type") or "").strip().upper()

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table_constraint"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Table}.{self.Name}"

    def GetTag(self):
        return "CONSTRAINT"

    def GetDefinition(self, separator=" "):
        if not self.IsForeignKey:
            return f"{self.GetTag()} {self.Name} {self.Definition}"

        definition = self.Definition
        if definition.find(" ON") > -1:
            definition = definition[0:definition.find(") ON") + 1]

        #definition = definition.replace("REFERENCES", separator+"REFERENCES")

        return separator.join([
            f"{self.GetTag()} {self.Name}",
            definition,
            self.MatchAction,
            self.UpdateAction,
            self.DeleteAction,
            self.DeferrableType
        ])

    def DDL_Inner(self):
        separator = f"{Config.NL}{Config.Indent * 2}"
        return Config.Indent + self.GetDefinition(separator)

    def DDL_Create(self):
        definition = self.GetDefinition(" ")
        return f"ALTER TABLE {self.Schema}.{self.Table} ADD {definition};"

    def DDL_Drop(self):
        return f"ALTER TABLE {self.Schema}.{self.Table} DROP {self.GetTag()} IF EXISTS {self.Name};"

    def Diff(self, another):
        if (
            self.DeferrableType != another.DeferrableType   or
            self.Definition     != another.Definition       or
            self.UpdateAction   != another.UpdateAction     or
            self.DeleteAction   != another.DeleteAction     or
            self.MatchAction    != another.MatchAction
        ):
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
        else:
            return []
