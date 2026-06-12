# R 临床报告工具生态

> Type: synthesis
> Sources: [gtsummary 来源页](../sources/gtsummary.md); [Pharmaverse 生态](../sources/pharmaverse.md)
> Updated: 2026-06-12

## Overview

本综合页梳理 R 语言在临床试验报告（TLF）层的主要工具生态，以 pharmaverse 为组织框架，gtsummary 为核心展示工具。

## Comparison

| 维度 | gtsummary | SAS PROC REPORT |
|------|-----------|-----------------|
| 输出格式 | gt/flextable/HTML/PDF 等多格式 | RTF/PDF（受限） |
| 与 ARD 兼容 | 是（cards/cardx） | 否 |
| 生态集成 | pharmaverse 生态深度集成 | 独立 |
| 学习曲线 | 中等（需 R 基础） | 已有 SAS 经验可直接上手 |

## Decision Notes

对于已有 SAS 经验的统计程序员，gtsummary 是迁移 R 的低摩擦入口，同时与 ARD 标准对齐，未来兼容性更好。

## Open Questions

- reporter 包与 gtsummary 的协作关系如何？（见 raw/pdfs 中相关演讲）
- pharmaverse 生态中哪些包负责 SDTM/ADaM 层？
