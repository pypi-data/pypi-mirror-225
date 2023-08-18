#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL, ParseOptions
from postgres_ddl.UserMapping import UserMapping

class ForeignServer(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = "_foreign"

        self.Name = (data.get("server_name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Foreign server name is null"

        self.FDW = (data.get("fdw_name") or "").strip().lower()
        assert len(self.FDW) > 0, \
            "Foreign server FDW is null"

        self.Options = data.get("options")

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : "SERVER",
                "instance_name" : self.Name,
                "owner_name"    : data.get("owner_name")
            }
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : "SERVER",
                "instance_name" : self.Name,
                "comment"       : data.get("comment")
            }
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.Name
            self.Grants.append(Grant(self.GetObjectName(), grant))

        self.UserMappings = []
        for role, options in (data.get("user_mappings") or {}).items():
            self.UserMappings.append(UserMapping(
                self.GetObjectName(),
                {
                    "instance_type" : "SERVER",
                    "instance_name" : self.Name,
                    "role"          : role,
                    "options"       : options
                }
            ))

    def __str__(self):
        return self.Name

    def GetObjectType(self):
        return "foreign_server"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Name}"

    def GetTag(self):
        return "FOREIGN SERVER"

    def DDL_Drop(self):
        return f"DROP SERVER IF EXISTS {self.Name};"

    def DDL_Create(self):
        r = f"-- Server: {self.Name}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE SERVER {self.Name}"
        r += Config.NL
        r += f"FOREIGN DATA WRAPPER {self.FDW}"
        r += Config.NL
        r += "OPTIONS("
        r += Config.NL
        r += self.DDL_Options()
        r += Config.NL
        r += ");"
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

        for um in sorted(self.UserMappings, key=lambda x: x.Role):
            r += um.DDL_Create()
            r += Config.NL

        return r.strip() + Config.NL

    def DDL_Options(self):
        result = []

        for o in sorted(self.Options):
            o = ParseOptions(o)
            if o is not None:
                result.append(f"{Config.Indent}{o}")

        return f",{Config.NL}".join(sorted(result))

    def GetPath(self):
        return [self.Schema]

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
