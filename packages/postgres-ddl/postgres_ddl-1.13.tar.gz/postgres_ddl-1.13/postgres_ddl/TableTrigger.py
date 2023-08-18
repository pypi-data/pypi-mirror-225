#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TableTrigger(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Trigger schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Trigger table is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Trigger name is null"

        self.IsDisabled = data.get("is_disabled") or False

        self.Definition = data.get("definition") or ""
        assert len(self.Definition) > 0, \
            "Trigger definition is null"

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table_trigger"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "TRIGGER"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.Name} ON {self.Schema}.{self.Table};"

    def DDL_Create(self):
        dfn = self.Definition
        dfn = dfn.replace(" BEFORE",  f"{Config.NL}{Config.Indent}BEFORE")
        dfn = dfn.replace(" AFTER",   f"{Config.NL}{Config.Indent}AFTER")
        dfn = dfn.replace(" ON",      f"{Config.NL}{Config.Indent}ON")
        dfn = dfn.replace(" FOR",     f"{Config.NL}{Config.Indent}FOR")
        dfn = dfn.replace(" EXECUTE", f"{Config.NL}{Config.Indent}EXECUTE")

        r = f"-- Trigger: {self.Name} ON {self.Schema}.{self.Table}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += dfn + ";"

        if self.IsDisabled:
            r += Config.NL + Config.NL
            r += self.DDL_Enabled()

        return r.strip()

    def DDL_Enabled(self):
        if self.IsDisabled:
            return f"ALTER TABLE {self.Schema}.{self.Table} DISABLE {self.GetTag()} {self.Name};"
        else:
            return f"ALTER TABLE {self.Schema}.{self.Table} ENABLE {self.GetTag()} {self.Name};"

    def Diff(self, another):
        result = []

        if self.Definition != another.Definition:
            result.append(another.DDL_Drop())
            result.append(self.DDL_Create())

        if self.IsDisabled != another.IsDisabled:
            result.append(self.DDL_Enabled())

        return result
