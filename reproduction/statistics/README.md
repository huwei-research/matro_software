# MATRO v14.1 统计复现

论文正文与附录为唯一PDF稿件。原独立补充材料中的分布、统计定义、等目标权重结果和参考值敏感性统一保存在[analysis.md](analysis.md)，配套数值、TeX表与生成脚本保留。

## 复算

从项目根目录运行：

```powershell
python -X utf8 paper/revisions/v14_1/statistics/analyze_statistics.py
```

Python 3.10以上，无第三方依赖；默认仅读取本目录与相邻`../data/`精简输入。约3秒、峰值工作集约63MiB，建议预留128MiB。程序复算四精度、六方法、两种参考值，不运行优化器。

| 文件 | 内容 |
|---|---|
| `analysis.md` | 完整统计定义、实例分布及参考值敏感性说明和表格 |
| `table_paired_summary.tex` | 正文表1：2940实例–起点对等权的成功率与求值次数 |
| 其他`table_*.tex` | 统计导出表；保留用于复核，不生成独立PDF |
| `instance_distribution.csv` | 147实例按维度与来源的分布 |
| `configuration_mapping.csv.gz` | 实例、目标函数身份与初始化关联 |
| `../data/initialization.csv.gz`、`../data/starts.csv.gz` | 初始化与全部2940起点 |
| `../data/runs.csv.gz`、`../data/references.csv.gz` | 四精度首次达标记录与参考值 |
| `canonical_run_values.csv.gz`、`reference_hit_checks.csv.gz` | 完整精度初值与参考值敏感性所需精确命中次数 |
| `objective_level_results.csv.gz`、`objective_summary.csv` | 逐目标统计与两种权重的汇总 |
| `matro_full_objective_wtl.csv` | 两方法逐目标的较少/相等/更多计数及成功率比较 |
| `reference_sensitivity.csv`、`reference_changes_by_identity.csv.gz` | 参考值变化的整体及逐函数影响 |

截断计数在失败时取全部预算`500*(n+1)`。正文表1按实例–起点对等权；等目标统计先平均每个目标的配置与起点，再平均136个目标。三个指标表使用未舍入值分别标示最大成功率与最小求值次数，绝对容差为1e-12。

本目录小于1MiB；完整逐次查询与模型历史位于`results/received_selection_20261104/archives/01_experiments.zip`，来源及成员位置见`provenance_source.json`、`reference_recovery_receipt.json`和`reference_query_members.csv.gz`。日常复算无需读取20.7GB归档。
