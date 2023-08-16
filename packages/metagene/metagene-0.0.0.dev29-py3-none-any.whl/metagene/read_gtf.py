#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2023 Ye Chang yech1990@gmail.com
# Distributed under terms of the GNU license.
#
# Created: 2023-03-08 20:46


import polars as pl
from gtfparse import read_gtf

# returns GTF with essential columns such as "feature", "seqname", "start", "end"
# alongside the names of any optional keys which appeared in the attribute column
# df = read_gtf("Homo_sapiens.GRCh38.109.chr.gtf", result_type="polars")
# backup polars data frame to parquet file
# df.write_parquet("hg38.parquet")
# df = pl.read_parquet("hg38.parquet")
# print(df.filter(pl.col("feature") == "gene"))
#
# df0 = df.filter(
#     pl.col("feature")
#     .cast(pl.Utf8)
#     .is_in(["start_codon", "CDS", "stop_codon", "exon"])
# ).select(
#     pl.col(
#         [
#             "seqname",
#             "start",
#             "end",
#             "strand",
#             "exon_number",
#             "exon_id",
#             "transcript_id",
#             "transcript_version",
#             "feature",
#         ]
#     )
# )
# df0.write_parquet("hg38_exon.parquet")


def my_function(group_df):
    name = (
        group_df.select(pl.col("transcript_id"))[0, 0]
        + "."
        + str(group_df.select(pl.col("transcript_version"))[0, 0])
    )
    col_start = []
    col_end = []
    col_type = []
    records = []
    strand = group_df.select(pl.col("strand"))[0, 0]
    # r = []
    start_df = group_df.filter(pl.col("feature") == "start_codon")
    end_df = group_df.filter(pl.col("feature") == "start_codon")
    if start_df.shape[0] == 1 and end_df.shape[0] == 1:
        # start codon position
        cs = start_df.select(pl.col("start"))[0, 0]
        # stop codon position
        ce = start_df.select(pl.col("end"))[0, 0]

        if strand == "+":
            group_df = group_df.sort(pl.col("start"))
            # split a list of intervals into 5UTR, CDS, 3UTR
            for row in group_df.rows(named=True):
                if row["start"] <= cs <= row["end"]:
                    col_start.append(row["start"])
                    col_end.append(cs - 1)
                    col_type.append("5UTR")
                    if row["end"] > ce:
                        # cds
                        col_start.append(cs)
                        col_end.append(ce - 1)
                        col_type.append("CDS")
                        # 3 utr
                        col_start.append(ce)
                        col_end.append(row["end"])
                        col_type.append("3UTR")
                    else:
                        col_start.append(cs)
                        col_end.append(row["end"])
                        col_type.append("CDS")
                elif row["start"] <= ce <= row["end"]:
                    # cds
                    col_start.append(row["start"])
                    col_end.append(ce - 1)
                    col_type.append("CDS")
                    # 3 utr
                    col_start.append(ce)
                    col_end.append(row["end"])
                    col_type.append("3UTR")
                else:
                    col_start.append(row["start"])
                    col_end.append(row["end"])
                    col_type.append("CDS")
        elif strand == "-":
            group_df = group_df.sort(pl.col("start"), descending=True)
            for row in group_df.rows(named=True):
                if row["start"] <= cs < row["end"]:
                    col_start.append(row["start"])
                    col_end.append(cs - 1)
                    col_type.append("3UTR")
                    if row["end"] > ce:
                        # cds
                        col_start.append(cs)
                        col_end.append(ce - 1)
                        col_type.append("CDS")
                        # 5 utr
                        col_start.append(ce)
                        col_end.append(row["end"])
                        col_type.append("5UTR")
                    else:
                        col_start.append(cs)
                        col_end.append(row["end"])
                        col_type.append("CDS")
                if row["end"] > ce:
                    # cds
                    col_start.append(row["start"])
                    col_end.append(ce - 1)
                    col_type.append("CDS")
                    # 5 utr
                    col_start.append(ce)
                    col_end.append(row["end"])
                    col_type.append("5UTR")
                else:
                    col_start.append(row["start"])
                    col_end.append(row["end"])
                    col_type.append("CDS")

    return pl.DataFrame(
        [
            pl.Series("name", [name] * len(records), dtype=pl.Utf8),
            pl.Series("strand", [strand] * len(records), dtype=pl.Utf8),
            pl.Series("start", [i[0] for i in records], dtype=pl.Int64),
            pl.Series("end", [i[1] for i in records], dtype=pl.Int64),
            pl.Series("type", [i[2] for i in records], dtype=pl.Utf8),
        ]
    )


df = pl.read_parquet("hg38_exon.parquet").head(3000)
print(df)
d = df.groupby(["transcript_id", "transcript_version", "strand"]).apply(
    my_function
)
print(d)
# .select(pl.col("type")).to_series().value_counts())
# print(d[0, 1])
