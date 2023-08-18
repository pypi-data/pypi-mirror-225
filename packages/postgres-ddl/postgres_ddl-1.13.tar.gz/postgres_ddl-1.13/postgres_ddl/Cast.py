#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class Cast(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Cast oid is null"

        self.TypeFrom = (data.get("type_from") or "").strip()
        assert len(self.TypeFrom) > 0, \
            "Cast type_from is null"

        self.TypeTo = (data.get("type_to") or "").strip()
        assert len(self.TypeTo) > 0, \
            "Cast type_to is null"

        self.Context = (data.get("context") or "").strip()
        assert len(self.Context) > 0, \
            "Cast context is null"

        self.Func = (data.get("func") or "").strip()

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "cast"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.TypeFrom} AS {self.TypeTo}"

    def GetTag(self):
        return "CAST"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Cast: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} ({self.GetFullName()})"
        r += Config.NL

        if len(self.Func) > 0:
            r += f"{Config.Indent}WITH FUNCTION {self.Func}"
        else:
            r += f"{Config.Indent}WITHOUT FUNCTION"
        r += Config.NL

        r += f"{Config.Indent}AS {self.Context}"
        r = r.strip() + ";"
        return r.strip() + Config.NL

    def GetPath(self):
        return ["_cast"]

    def GetFileName(self):
        return f"{self.GetFullName()}.sql"

    def Export(self):
        return { self.GetObjectName() : self }

    def Diff(self, another):
        if self.DDL_Create() != another.DDL_Create():
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]

        return []
