#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TableSettings(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Schema = (data.get("schema") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Table settings schema is null"

        self.Table = (data.get("table") or "").strip().lower()
        assert len(self.Table) > 0, \
            "Table settings table is null"

        setting = data.get("setting" or "").strip().lower()
        assert len(setting) > 0, \
            "Table settings value is null"
        assert setting.find('=') >= 0, \
            "Table settings value isn't contains '=' symbol"

        self.Field = setting.split('=')[0].strip().upper()
        self.Value = setting.split('=')[1].strip().upper()

    def __str__(self):
        return f"{self.Field}={self.Value}"

    def GetObjectType(self):
        return "table_setting"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Table}.{self.Field}"

    def DDL_Inner(self):
        return f"{Config.Indent}{self.Field}={self.Value}"

    def DDL_Drop(self):
        return f"ALTER TABLE {self.Schema}.{self.Table} RESET ({self.Field});"

    def DDL_Create(self):
        return f"ALTER TABLE {self.Schema}.{self.Table} SET ({self.Field} = {self.Value});"

    def Diff(self, another):
        if self.Value != another.Value:
            return [
                self.DDL_Create()
            ]
        else:
            return []
