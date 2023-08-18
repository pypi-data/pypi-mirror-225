#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TablePolicy(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Policy schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Policy table is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Policy name is null"

        self.Command = (data.get("command") or "").strip().upper()
        assert len(self.Command) > 0, \
            "Policy command is null"

        self.Type = (data.get("type") or "").strip().upper()
        assert len(self.Type) > 0, \
            "Policy type is null"

        self.ExprUsing = data.get("expr_using") or ""
        self.ExporWithCheck = data.get("expr_with_check") or ""
        assert (len(self.ExprUsing) > 0 or len(self.ExporWithCheck) > 0), \
            "Policy expression is null"

        self.Roles = (data.get("roles") or [])
        assert len(self.Roles) > 0, \
            "Policy roles is empty"
        self.Roles = ", ".join(self.Roles)

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table_policy"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Table}.{self.Name}"

    def GetTag(self):
        return "POLICY"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.Name} ON {self.Schema}.{self.Table};"

    def DDL_Create(self):
        r = f"-- Policy: {self.Name} ON {self.Schema}.{self.Table}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.Name}"
        r += Config.NL
        r += f"{Config.Indent}ON {self.Schema}.{self.Table}"
        r += Config.NL
        r += f"{Config.Indent}AS {self.Type}"
        r += Config.NL
        r += f"{Config.Indent}FOR {self.Command}"
        r += Config.NL
        r += f"{Config.Indent}TO {self.Roles}"
        r += Config.NL

        if len(self.ExprUsing) > 0:
            r += f"{Config.Indent}USING({self.ExprUsing});"
        else:
            r += f"{Config.Indent}WITH CHECK({self.ExporWithCheck});"

        return r.strip()

    def Diff(self, another):
        result = []

        if (
            self.Command != another.Command or
            self.Type != another.Type or
            self.Roles != another.Roles or
            self.ExprUsing != another.ExprUsing or
            self.ExporWithCheck != another.ExporWithCheck
        ):
            result.append(another.DDL_Drop())
            result.append(self.DDL_Create())

        return result
