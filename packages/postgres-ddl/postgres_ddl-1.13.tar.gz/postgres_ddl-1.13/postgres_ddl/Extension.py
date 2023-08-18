#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class Extension(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Extension oid is null"

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Extension schema is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Extension name is null"

        self.Version = (data.get("version") or "").strip()
        assert len(self.Version) > 0, \
            "Extension version is null"

        self.Owner = (data.get("owner") or "").strip()
        assert len(self.Owner) > 0, \
            "Extension owner is null"

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "extension"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Name}"

    def GetTag(self):
        return "EXTENSION"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Extension: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"SET ROLE {self.Owner};"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}"
        r += Config.NL
        r += f'{Config.Indent}SCHEMA "{self.Schema}"'
        r += Config.NL
        r += f'{Config.Indent}VERSION "{self.Version}"'
        r += Config.NL
        r = r.strip() + ";"
        return r.strip() + Config.NL

    def GetPath(self):
        return ["_extension"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        return { self.GetObjectName() : self }

    def Diff(self, another):
        if self.DDL_Create() != another.DDL_Create():
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]

        return []
