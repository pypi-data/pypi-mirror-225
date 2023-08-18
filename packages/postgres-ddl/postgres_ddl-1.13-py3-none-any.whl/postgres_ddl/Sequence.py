#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class Sequence(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Sequence oid is null"

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Sequence schema is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Sequence name is null"

        self.Increment = int(data.get("increment") or 0)
        assert self.Increment != 0, \
            "Sequence increment is null"

        self.MinValue = int(data.get("minimum_value") or 0)
        self.MaxValue = int(data.get("maximum_value") or 0)

        self.IsCycle = "CYCLE" if data.get("is_cycle") is True else "NO CYCLE"

        self.Cache = (data.get("cache") or 0)
        assert self.Cache > 0, \
            "Sequence cache is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : "TABLE",
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner")
            }
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "comment"       : data.get("comment")
            }
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.GetFullName()
            self.Grants.append(Grant(self.GetObjectName(), grant))

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "sequence"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "SEQUENCE"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Sequence: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}"
        r += Config.NL
        r += f"{Config.Indent}INCREMENT {self.Increment}"
        r += Config.NL
        r += f"{Config.Indent}MINVALUE {self.MinValue}"
        r += Config.NL
        r += f"{Config.Indent}MAXVALUE {self.MaxValue}"
        r += Config.NL
        r += f"{Config.Indent}START 1"
        r += Config.NL
        r += f"{Config.Indent}CACHE {self.Cache}"
        r += Config.NL
        r += f"{Config.Indent}{self.IsCycle}"
        r = r.strip() + ";"
        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create()
        r += Config.NL + Config.NL

        for grant in self.Grants:
            r += grant.DDL_Create()
            r += Config.NL
        r += Config.NL

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create()
            r += Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return [self.Schema, "sequence"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for v in self.Grants:
            result[v.GetObjectName()] = v
        return result

    def Diff(self, another):
        result = []

        if self.Cache != another.Cache:
            result.append(f"CACHE {self.Cache}")

        if self.Increment != another.Increment:
            result.append(f"INCREMENT BY {self.Increment}")

        if self.IsCycle != another.IsCycle:
            result.append(self.IsCycle)

        if self.MinValue != another.MinValue:
            result.append(f"MINVALUE {self.MinValue}")

        if self.MaxValue != another.MaxValue:
            result.append(f"MAXVALUE {self.MaxValue}")

        if len(result) > 0:
            result = " ".join(result)
            return [f"ALTER {self.GetTag()} {self.GetFullName()} {result}"]
        else:
            return []
