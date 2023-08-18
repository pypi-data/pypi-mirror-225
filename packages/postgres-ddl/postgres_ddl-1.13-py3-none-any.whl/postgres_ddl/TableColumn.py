#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TableColumn(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Column schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Column table is null"

        self.Name = (data.get("name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Column name is null"

        self.Type = (data.get("type") or "").strip()
        assert len(self.Type) > 0, \
            "Column type is null"

        self.NotNull = data.get("not_null") or False

        self.DefaultValue = (data.get("default_value") or "").strip()

        self.OrderNum = data.get("order_num") or 0
        assert self.OrderNum > 0, \
            "Column order num is null"

        self.OrderNumLast = data.get("max_order_num") or 0
        assert self.OrderNumLast > 0, \
            "Column max order num is null"

        self.IsLast = (self.OrderNum == self.OrderNumLast)

        self.Comment = data.get("comment")
        if self.Comment is not None:
            self.Comment = re.sub("[\n\r]{1,}", Config.NL, self.Comment, re.MULTILINE | re.IGNORECASE)

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table_column"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Table}.{self.Name}"

    def GetTag(self):
        return "COLUMN"

    def DDL_Create(self):
        not_null = "" if not self.NotNull else " NOT NULL"
        dflt = "" if len(self.DefaultValue) <= 0 else " DEFAULT " + self.DefaultValue

        r = f"ALTER TABLE {self.Schema}.{self.Table} ADD {self.GetTag()} {self.Name} {self.Type}{not_null}{dflt};"

        if self.Comment is not None and self.Comment.strip() != "":
            r += Config.NL
            r += self.DDL_Comment()

        return r

    def DDL_NotNull(self):
        if self.NotNull:
            return f"ALTER TABLE {self.Schema}.{self.Table} ALTER {self.GetTag()} {self.Name} SET NOT NULL;"
        else:
            return f"ALTER TABLE {self.Schema}.{self.Table} ALTER {self.GetTag()} {self.Name} DROP NOT NULL;"

    def DDL_Default(self):
        if self.DefaultValue is None or self.DefaultValue.strip() == "":
            return f"ALTER TABLE {self.Schema}.{self.Table} ALTER {self.GetTag()} {self.Name} DROP DEFAULT;"
        else:
            return f"ALTER TABLE {self.Schema}.{self.Table} ALTER {self.GetTag()} {self.Name} SET DEFAULT {self.DefaultValue};"

    def DDL_Drop(self):
        return f"ALTER TABLE {self.Schema}.{self.Table} DROP {self.GetTag()} IF EXISTS {self.Name};"

    def DDL_Comment(self):
        if self.Comment is not None and self.Comment.strip() != "":
            return f"COMMENT ON {self.GetTag()} {self.Schema}.{self.Table}.{self.Name}{Config.NL}{Config.Indent}IS '{self.Comment}';"
        return None

    def DDL_Type(self):
        return f"ALTER TABLE {self.Schema}.{self.Table} ALTER {self.GetTag()} {self.Name} TYPE {self.Type};"

    def DDL_Inner(self, add_comma=False, add_comment=False):
        if not add_comma:
            add_comma = not self.IsLast

        return f"{Config.Indent}%s %s%s%s%s%s" % (
            self.Name,
            self.Type,
            "" if not self.NotNull else " NOT NULL",
            "" if len(self.DefaultValue) <= 0 else " DEFAULT " + self.DefaultValue,
            "" if not add_comma else ",",
            "" if not add_comment or self.Comment is None else f" -- %s" % (self.Comment.replace(Config.NL, " "))
        )

    def Diff(self, another):
        result = []

        if self.Comment != another.Comment:
            result.append(self.DDL_Comment())

        if self.DefaultValue != another.DefaultValue:
            result.append(self.DDL_Default())

        if self.NotNull != another.NotNull:
            result.append(self.DDL_NotNull())

        if self.Type != another.Type:
            result.append(self.DDL_Type())

        return result
