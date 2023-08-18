#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.TSDB_Dimension import TSDB_Dimension

class TSDB_HyperTable(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.ID = data.get("id") or 0
        assert self.ID > 0, \
            f"{self.GetObjectTypeComment()} id is null"

        self.TSDB_Schema = (data.get("tsdb_schema") or "timescaledb").strip().lower()
        assert len(self.TSDB_Schema) > 0, \
            f"{self.GetObjectTypeComment()} TSDB schema is null"

        self.Relation = (data.get("relation") or "").strip().lower()
        assert len(self.Relation) > 0, \
            f"{self.GetObjectTypeComment()} relation is null"

        self.PartsSchema = (data.get("parts_schema") or "").strip().lower()
        assert len(self.PartsSchema) > 0, \
            f"{self.GetObjectTypeComment()} parts_schema is null"

        self.PartsPrefix = (data.get("parts_prefix") or "").strip().lower()
        assert len(self.PartsPrefix) > 0, \
            f"{self.GetObjectTypeComment()} parts_prefix is null"

        self.IsCompress = (data.get("is_compress") is True)
        self.CompressAfter = (data.get("compress_after") or "").strip().lower()
        self.CompressOrderBy = (data.get("compress_order_by") or "").strip().lower()
        self.CompressSegmentBy = (data.get("compress_segment_by") or "").strip().lower()

        self.DropAfter = (data.get("drop_after") or "").strip().lower()

        self.PartColumn = None
        self.Dimensions = []

        for row in (data.get("dimensions") or []):
            row = TSDB_Dimension(self.GetFullName(), row)
            if row.OrderNum == 1:
                self.PartColumn = row
            else:
                self.Dimensions.append(row)

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "tsdb_hypertable"

    def GetObjectTypeComment(self):
        return "TimescaleDB hypertable"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Relation

    def DDL_CreateHyperTable(self):
        params = [
            ["relation", self.Relation, True],
            ["time_column_name", self.PartColumn.Column, True],
            ["create_default_indexes", "FALSE", False],
            ["migrate_data", "FALSE", False],
            ["associated_schema_name", self.PartsSchema, True],
            ["associated_table_prefix", self.PartsPrefix, True]
        ]

        if self.PartColumn is not None:
            if len(self.PartColumn.Interval) > 0:
                params.append(["chunk_time_interval", self.PartColumn.Interval, False])
            if len(self.PartColumn.FncPart) > 0:
                params.append(["time_partitioning_func", self.PartColumn.FncPart, True])
            if self.PartColumn.SlicesNum > 0:
                params.append(["number_partitions", self.PartColumn.SlicesNum, False])
            if len(self.PartColumn.FncIntNow) > 0:
                params.append(["partitioning_func", self.PartColumn.FncIntNow, True])

        r = f"SELECT {self.TSDB_Schema}.create_hypertable("
        r += Config.NL
        r += self.FillFunctionParams(params)
        r += Config.NL
        r += ");"
        return r

    def DDL_DropRetentionPolicy(self):
        return f"SELECT {self.TSDB_Schema}.remove_retention_policy('{self.Relation}');"

    def DDL_CreateRetentionPolicy(self):
        r = f"SELECT {self.TSDB_Schema}.add_retention_policy("
        r += Config.NL
        r += self.FillFunctionParams([
            ["relation", self.Relation, True],
            ["drop_after", self.DropAfter, False],
        ])
        r += Config.NL
        r += ");"
        return r

    def DDL_DropCompressionPolicy(self):
        return f"SELECT {self.TSDB_Schema}.remove_compression_policy('{self.Relation}');"

    def DDL_CreateCompressionPolicy(self):
        r = f"SELECT {self.TSDB_Schema}.add_compression_policy("
        r += Config.NL
        r += self.FillFunctionParams([
            ["hypertable", self.Relation, True],
            ["compress_after", self.CompressAfter, False],
        ])
        r += Config.NL
        r += ");"
        return r

    def DDL_DropCompressionSettings(self):
        r = self.FillFunctionParams([
            ["timescaledb.compress", "FALSE", False],
        ], True, "=")
        return f"ALTER TABLE {self.Relation} SET({r});"

    def DDL_CreateCompressionSettings(self):
        params = [
            ["timescaledb.compress", str(self.IsCompress).upper(), False],
            ["timescaledb.compress_orderby", self.CompressOrderBy, True],
            ["timescaledb.compress_segmentby", self.CompressSegmentBy, True]
        ]

        r = f"ALTER TABLE {self.Relation} SET("
        r += Config.NL
        r += self.FillFunctionParams(params, False, "=")
        r += Config.NL
        r += ");"
        return r

    def DDL_Create(self):
        r = f"-- {self.GetObjectTypeComment()}: {self.Relation}"
        r += Config.NL + Config.NL
        r += self.DDL_CreateHyperTable()
        r += Config.NL + Config.NL

        for dim in self.Dimensions:
            r += f"-- {self.GetObjectTypeComment()} dimension: {self.Relation}.{dim.Column}"
            r += Config.NL + Config.NL
            r += dim.DDL_Create()
            r += Config.NL + Config.NL

        if self.IsCompress:
            r += f"-- {self.GetObjectTypeComment()} compression settings: {self.Relation}"
            r += Config.NL + Config.NL
            r += self.DDL_CreateCompressionSettings()
            r += Config.NL + Config.NL

        if len(self.CompressAfter) > 0:
            r += f"-- {self.GetObjectTypeComment()} compression policy: {self.Relation}"
            r += Config.NL + Config.NL
            r += f"-- {self.DDL_DropCompressionPolicy()}"
            r += Config.NL + Config.NL
            r += self.DDL_CreateCompressionPolicy()
            r += Config.NL + Config.NL

        if len(self.DropAfter) > 0:
            r += f"-- {self.GetObjectTypeComment()} retention policy: {self.Relation}"
            r += Config.NL + Config.NL
            r += f"-- {self.DDL_DropRetentionPolicy()}"
            r += Config.NL + Config.NL
            r += self.DDL_CreateRetentionPolicy()
            r += Config.NL + Config.NL

        return r.strip() + Config.NL

    def Diff(self, another):
        result = []

        self_create_hypertable = self.DDL_CreateHyperTable()
        if self_create_hypertable != another.DDL_CreateHyperTable():
            result.append(self_create_hypertable)

        self_create_compression_settings = self.DDL_CreateCompressionSettings()
        if self_create_compression_settings != another.DDL_CreateCompressionSettings():
            result.append(self.DDL_DropCompressionSettings())
            result.append(self_create_compression_settings)

        self_create_compression_policy = self.DDL_CreateCompressionPolicy()
        if self_create_compression_policy != another.DDL_CreateCompressionPolicy():
            result.append(self.DDL_DropCompressionPolicy())
            result.append(self_create_compression_policy)

        self_create_retention_policy = self.DDL_CreateRetentionPolicy()
        if self_create_retention_policy != another.DDL_CreateRetentionPolicy():
            result.append(self.DDL_DropRetentionPolicy())
            result.append(self_create_retention_policy)

        return result
