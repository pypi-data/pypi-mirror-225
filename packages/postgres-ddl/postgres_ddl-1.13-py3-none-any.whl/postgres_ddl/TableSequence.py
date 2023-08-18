#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class TableSequence(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Sequence schema is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Sequence name is null"

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

    def DDL_Create(self):
        r = f"-- Sequence: {self.GetFullName()}"
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
