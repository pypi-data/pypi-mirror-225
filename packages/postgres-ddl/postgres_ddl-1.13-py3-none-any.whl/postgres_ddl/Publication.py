#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Owner import Owner

class Publication(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Publication oid is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Publication name is null"

        self.IsViaRoot = bool(data.get("is_via_root") or False)
        self.IsAllTables = bool(data.get("is_all_tables") or False)

        self.Actions = (data.get("actions") or "").strip()
        assert len(self.Actions) > 0, \
            "Publication actions is null"

        self.Tables = (data.get("tables") or [])
        assert self.IsAllTables or len(self.Tables) > 0, \
            "Publication tables is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner")
            }
        )

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "publication"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Name

    def GetTag(self):
        return "PUBLICATION"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Publication: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}"

        if self.IsAllTables:
            r += f" FOR ALL TABLES"
        else:
            r += f" FOR TABLE"
            r += Config.NL
            r += f",{Config.NL}".join([f"{Config.Indent}{t}" for t in self.Tables])
        r += Config.NL

        r += "WITH ("
        r += Config.NL
        r += f"{Config.Indent}publish = '{self.Actions}',"
        r += Config.NL
        r += f"{Config.Indent}publish_via_partition_root = {str(self.IsViaRoot).upper()}"
        r += Config.NL
        r += ");"

        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create() + Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return ["_logical"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Owner.GetObjectName()] = self.Owner
        return result

    def Diff(self, another):
        result = []

        if self.IsViaRoot != another.IsViaRoot:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} SET(publish_via_partition_root = {str(self.IsViaRoot).upper()});")

        if self.Actions != another.Actions:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} SET(publish = '{self.Actions}');")

        if self.Tables != another.Tables:
            tables = ", ".join(self.Tables)
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} SET TABLE {tables};")

        return result
