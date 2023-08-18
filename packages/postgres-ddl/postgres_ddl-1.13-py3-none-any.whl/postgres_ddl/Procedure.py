#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class Procedure(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = (data.get("oid") or 0)
        assert self.Oid > 0, \
            "Procedure oid is null"

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Procedure schema is null"

        self.Name = (data.get("proc") or "").strip()
        assert len(self.Name) > 0, \
            "Procedure name is null"

        self.ArgsInTypes = (data.get("args_in_types") or "").strip()

        self.NameWithParams = f"{self.Schema}.{self.Name}({self.ArgsInTypes})"

        self.ArgsIn = (data.get("args_in") or "").strip()

        self.Language = (data.get("lang") or "").strip()
        assert len(self.Language) > 0, \
            "Procedure language is null"

        self.HasDuplicate = data.get("has_duplicate") or False

        self.Code = (data.get("code") or "").strip()
        assert len(self.Code) > 0, \
            "Procedure code is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.NameWithParams,
                "owner_name"    : data.get("owner")
            }
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.NameWithParams,
                "comment"       : data.get("comment")
            }
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.NameWithParams
            self.Grants.append(Grant(self.GetObjectName(), grant))

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "procedure"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        if self.HasDuplicate:
            return f"{self.Schema}.{self.Name}({self.ArgsInTypes}).sql"
        else:
            return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "PROCEDURE"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.Schema}.{self.Name}({self.ArgsInTypes});"

    def DDL_ArgsIn(self):
        if len(self.ArgsIn or "") == 0:
            return "()" + Config.NL
        else:
            args = self.ArgsIn.replace(",", f",{Config.NL}{Config.Indent[:-1]}")
            r = "("
            r += Config.NL
            r += f"{Config.Indent}{args}"
            r += Config.NL
            r += ") "
            return r

    def DDL_Create(self):
        r = f"-- Procedure: {self.Schema}.{self.Name}({self.ArgsInTypes})"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE OR REPLACE {self.GetTag()} {self.Schema}.{self.Name}"
        r += self.DDL_ArgsIn()
        r += Config.NL
        r += f'LANGUAGE "{self.Language}" AS'
        r += Config.NL
        r += "$BODY$"
        r += Config.NL
        r += self.Code
        r += Config.NL
        r += "$BODY$;"
        r += Config.NL
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
        return [self.Schema, "procedure"]

    def GetFileName(self):
        if self.HasDuplicate:
            return f"{self.Name}({self.ArgsInTypes}).sql"
        else:
            return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for g in self.Grants:
            result[g.GetObjectName()] = g
        return result

    def Diff(self, another):
        if (
            self.ArgsIn     != another.ArgsIn     or
            self.ArgsOut    != another.ArgsOut    or
            self.Code       != another.Code       or
            self.Cost       != another.Cost       or
            self.Language   != another.Language   or
            self.Rows       != another.Rows       or
            self.Volatility != another.Volatility
        ):
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
        else:
            return []
