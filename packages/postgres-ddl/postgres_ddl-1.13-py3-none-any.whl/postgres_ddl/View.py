#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL
from postgres_ddl.TableIndex import TableIndex

class View(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.IsMaterialized = data.get("is_materialized")
        self.IsMaterialized = self.IsMaterialized if self.IsMaterialized is not None else False

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "View oid is null"

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "View schema is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "View name is null"

        self.Definition = (data.get("definition") or "").strip()
        assert len(self.Definition) > 0, \
            "View definition is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : "TABLE",
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner_name")
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

        self.ColumnComments = []
        for comment in data.get("column_comments") or []:
            comment["instance_type"] = "COLUMN"
            comment["instance_name"] = ".".join([self.GetFullName(), comment.get("name")])
            self.ColumnComments.append(Comment(self.GetObjectName(), comment))

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = "TABLE"
            grant["instance_name"] = self.GetFullName()
            self.Grants.append(Grant(self.GetObjectName(), grant))

        self.Indexes = []
        for idx in (data.get("indexes") or []):
            idx["schema"] = self.Schema
            idx["table"] = self.Name
            idx = TableIndex(self.GetObjectName(), idx)
            self.Indexes.append(idx)

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        if self.IsMaterialized:
            return "matview"
        else:
            return "view"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Schema}.{self.Name}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "MATERIALIZED VIEW" if self.IsMaterialized else "VIEW"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- View: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL

        if self.IsMaterialized:
            r += f"CREATE {self.GetTag()} {self.GetFullName()} AS"
        else:
            r += f"CREATE OR REPLACE {self.GetTag()} {self.GetFullName()} AS"
        r += Config.NL
        r += self.Definition
        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create()
        r += Config.NL + Config.NL

        for grant in self.Grants:
            r += grant.DDL_Create()
            r += Config.NL
        r += Config.NL

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create()
            r += Config.NL + Config.NL

        for comment in self.ColumnComments:
            r += comment.DDL_Create()
            r += Config.NL + Config.NL

        for ind in sorted(self.Indexes, key=lambda x: x.GetFullName()):
            r += ind.DDL_Create(f"{Config.NL}{Config.Indent}")
            r += Config.NL + Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return [self.Schema, "view"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for v in self.Grants:
            result[v.GetObjectName()] = v
        for v in self.Indexes:
            result[v.GetObjectName()] = v
        return result

    def Diff(self, another):
        if self.Definition != another.Definition:
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
