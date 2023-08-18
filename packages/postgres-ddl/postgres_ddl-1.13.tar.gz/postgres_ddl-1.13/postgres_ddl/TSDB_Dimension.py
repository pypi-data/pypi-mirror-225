#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class TSDB_Dimension(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.TSDB_Schema = (data.get("tsdb_schema") or "timescaledb").strip().lower()
        assert len(self.TSDB_Schema) > 0, \
            f"{self.GetObjectTypeComment()} TSDB schema is null"

        self.Column = (data.get("column_name") or "").strip().lower()
        assert len(self.Column) > 0, \
            f"{self.GetObjectTypeComment()} column name is null"

        self.OrderNum = data.get("order_num") or 0

        self.SlicesNum = data.get("num_slices") or 0

        self.FncPart = (data.get("fnc_part") or "").strip().lower()

        self.FncIntNow = (data.get("fnc_int_now") or "").strip().lower()

        self.Interval = (data.get("interval") or "").strip().lower()

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "tsdb_dimension"

    def GetObjectTypeComment(self):
        return "TSDB dimension"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Relation}.{self.Column}"

    def DDL_Create(self):
        params = [
            ["hypertable", self.Parent, True],
            ["column_name", self.Column, True],
        ]

        if len(self.Interval) > 0:
            params.append(["chunk_time_interval", self.Interval, False])

        if len(self.FncPart) > 0:
            params.append(["partitioning_func", self.FncPart, True])

        if self.SlicesNum > 0:
            params.append(["number_partitions", self.SlicesNum, False])

        r = f"select {self.TSDB_Schema}.add_dimension("
        r += Config.NL
        r += self.FillFunctionParams(params)
        r += Config.NL
        r += ");"
        return r

    def Diff(self, another):
        if self.Value != another.Value:
            return [
                self.DDL_Create()
            ]
        else:
            return []
