#!/usr/bin/env python3
"""从两个根级权威入口同步公司排序的展示与效果管理文件。

权威入口：
1. 00_运行与榜单注册表.csv：当前运行、榜单和原始结果路径。
2. 00_当前评估.json：当前正式评估包及其规范化数据路径。

本脚本只写管理文件，不会修改任何 01_研究方案.md 或 02_排序结果.md。
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "00_运行与榜单注册表.csv"
EVALUATION_POINTER = ROOT / "00_当前评估.json"
STATUS_TABLE = ROOT / "00_方案状态总表.csv"
BLOCK_START = "<!-- AUTO-CURRENT-RUN:START -->"
BLOCK_END = "<!-- AUTO-CURRENT-RUN:END -->"

HISTORY_FIELDS = [
    "schema_version",
    "method_id",
    "source_scheme_id",
    "run_role",
    "run_id",
    "ranking_generated_date",
    "evaluation_id",
    "evidence_type",
    "horizon",
    "evaluation_start",
    "evaluation_end",
    "holding_days",
    "ranked_count",
    "valid_count",
    "top_bucket_n",
    "bottom_bucket_n",
    "top_bucket_return_pct",
    "universe_return_pct",
    "top_universe_excess_pct",
    "top_bottom_spread_pct",
    "spearman_rank_ic",
    "category_neutral_rank_ic",
    "top_bucket_max_drawdown_pct",
    "source",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def resolve_root_path(relative: str) -> Path:
    if not relative:
        raise ValueError("权威入口包含空路径")
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts:
        raise ValueError(f"只允许公司排序根目录内的相对路径：{relative}")
    resolved = (ROOT / Path(*posix.parts)).resolve()
    resolved.relative_to(ROOT.resolve())
    return resolved


def relative_link(source_dir: Path, target: Path) -> str:
    return os.path.relpath(target, source_dir).replace("\\", "/")


def number(value: object) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(str(value))
    except (TypeError, ValueError):
        return None


def ratio_pct(value: object) -> str:
    parsed = number(value)
    if parsed is None:
        return ""
    return f"{parsed * 100:.6f}".rstrip("0").rstrip(".")


def signed(value: object, digits: int = 3) -> str:
    parsed = number(value)
    if parsed is None:
        return "-"
    return f"{parsed:+.{digits}f}"


def signed_pct_ratio(value: object, digits: int = 1) -> str:
    parsed = number(value)
    if parsed is None:
        return "-"
    return f"{parsed * 100:+.{digits}f}%"


def current_result_markdown(
    method_id: str,
    rows: list[dict[str, str]],
    method_dir: Path,
    summary_path: Path,
    report_path: Path,
    registry_path: Path,
) -> str:
    first = rows[0]
    result_lines = []
    for row in rows:
        target = resolve_root_path(row["result_path"])
        label = row["list_name"] if len(rows) > 1 else "完整排序结果"
        result_lines.append(f"- {label}：[打开原始结果]({relative_link(method_dir, target)})")
    return "\n".join(
        [
            f"# {method_id} {first['method_name']}：当前排序结果",
            "",
            "> 本文件是稳定展示入口；完整内容只保存在迭代版本的原始结果文件中，不在这里复制。",
            "",
            f"- 当前状态：{first['status']}",
            f"- 当前运行：`{first['run_id']}`",
            f"- 结果生成日：{first['run_date']}",
            f"- 样本：每张榜预期 {first['expected_row_count']} 家公司",
            *result_lines,
            f"- 当前效果摘要：[打开]({relative_link(method_dir, summary_path)})",
            f"- 本轮正式评估：[打开]({relative_link(method_dir, report_path)})",
            f"- 权威运行注册表：[打开]({relative_link(method_dir, registry_path)})",
            "",
            "后续更新只需变更根目录权威注册表并重新同步；历史研究方案和历史排序结果保持原样。",
            "",
        ]
    )


def management_block(
    method_id: str,
    rows: list[dict[str, str]],
    method_dir: Path,
    report_path: Path,
) -> str:
    first = rows[0]
    result_links = "；".join(
        f"[{row['list_name']}]({relative_link(method_dir, resolve_root_path(row['result_path']))})" for row in rows
    )
    return "\n".join(
        [
            BLOCK_START,
            "## 当前运行",
            "",
            f"- 生命周期：{first['lifecycle']}",
            f"- 当前状态：{first['status']}",
            f"- 当前用途：{first['role']}",
            f"- 当前运行：`{first['run_id']}`；结果生成日：{first['run_date']}",
            f"- 当前结果：{result_links}",
            f"- 当前评估：[3个月与6个月生成前历史回看]({relative_link(method_dir, report_path)})",
            "- 证据边界：本轮3个月和6个月均发生在当前排名生成前，只作历史回看；生命周期状态不会因此自动升级或降级。",
            "",
            BLOCK_END,
        ]
    )


def update_status_markdown(path: Path, title: str, block: str) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8-sig")
        if BLOCK_START in text and BLOCK_END in text:
            before, rest = text.split(BLOCK_START, 1)
            _, after = rest.split(BLOCK_END, 1)
            updated = before.rstrip() + "\n\n" + block + after
        else:
            lines = text.splitlines()
            insert_at = 1 if lines and lines[0].startswith("# ") else 0
            updated_lines = lines[:insert_at] + ["", block, ""] + lines[insert_at:]
            updated = "\n".join(updated_lines)
    else:
        updated = "\n".join(
            [
                f"# {title}",
                "",
                block,
                "",
                "## 管理边界",
                "",
                "当前文件只记录生命周期、运行入口和证据边界；研究逻辑以各版本的研究方案为准，历史文件保持原样。",
                "",
            ]
        )
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def migrate_history(rows: list[dict[str, str]], method_id: str) -> list[dict[str, object]]:
    if not rows:
        return []
    if "schema_version" in rows[0]:
        return [dict(row) for row in rows]
    migrated: list[dict[str, object]] = []
    for row in rows:
        run_id = row.get("run_id", "")
        end = row.get("evaluation_end", "")
        migrated.append(
            {
                "schema_version": "2",
                "method_id": row.get("method_id", method_id),
                "source_scheme_id": row.get("source_scheme_id", ""),
                "run_role": row.get("run_role", ""),
                "run_id": run_id,
                "ranking_generated_date": row.get("generated_date", ""),
                "evaluation_id": f"legacy_{method_id}_{run_id}_{end}",
                "evidence_type": row.get("evidence_type", ""),
                "horizon": "历史短窗",
                "evaluation_start": row.get("evaluation_start", ""),
                "evaluation_end": end,
                "holding_days": row.get("holding_days", ""),
                "ranked_count": row.get("ranked_count", ""),
                "valid_count": row.get("ranked_count", ""),
                "top_bucket_n": "10",
                "bottom_bucket_n": "10",
                "top_bucket_return_pct": row.get("top10_return_pct", ""),
                "universe_return_pct": row.get("universe_return_pct", ""),
                "top_universe_excess_pct": row.get("universe_excess_pct", ""),
                "top_bottom_spread_pct": row.get("top10_bottom10_spread_pct", ""),
                "spearman_rank_ic": row.get("spearman_rank_ic", ""),
                "category_neutral_rank_ic": "",
                "top_bucket_max_drawdown_pct": row.get("top10_max_drawdown_pct", ""),
                "source": row.get("source", ""),
            }
        )
    return migrated


def current_history_rows(
    method_id: str,
    registry_rows: list[dict[str, str]],
    metric: dict[str, str],
    evaluation: dict[str, object],
    starts: dict[str, str],
) -> list[dict[str, object]]:
    first = registry_rows[0]
    run_role = "三榜等权派生综合" if method_id == "06" else "当前独立自洽运行"
    rows: list[dict[str, object]] = []
    for horizon, suffix in (("3M", "3m"), ("6M", "6m")):
        top = number(metric.get(f"top20_mean_{suffix}"))
        universe = number(metric.get(f"universe_mean_{suffix}"))
        rows.append(
            {
                "schema_version": "2",
                "method_id": method_id,
                "source_scheme_id": method_id,
                "run_role": run_role,
                "run_id": first["run_id"],
                "ranking_generated_date": first["run_date"],
                "evaluation_id": evaluation["evaluation_id"],
                "evidence_type": evaluation["evidence_type"],
                "horizon": horizon,
                "evaluation_start": starts[horizon],
                "evaluation_end": evaluation["price_as_of"],
                "holding_days": "",
                "ranked_count": metric.get("ranked_n", first["expected_row_count"]),
                "valid_count": metric.get(f"valid_n_{suffix}", ""),
                "top_bucket_n": "20",
                "bottom_bucket_n": "20",
                "top_bucket_return_pct": ratio_pct(top),
                "universe_return_pct": ratio_pct(universe),
                "top_universe_excess_pct": ratio_pct(top - universe if top is not None and universe is not None else None),
                "top_bottom_spread_pct": ratio_pct(metric.get(f"top20_bottom20_spread_{suffix}")),
                "spearman_rank_ic": metric.get(f"rank_ic_{suffix}", ""),
                "category_neutral_rank_ic": metric.get(f"category_neutral_rank_ic_{suffix}", ""),
                "top_bucket_max_drawdown_pct": "",
                "source": evaluation["method_metrics_path"],
            }
        )
    return rows


def effect_summary_markdown(
    method_id: str,
    registry_rows: list[dict[str, str]],
    metric: dict[str, str],
    summary_dir: Path,
    report_path: Path,
    history_path: Path,
    evaluation: dict[str, object],
) -> str:
    first = registry_rows[0]
    verdict = "方向混合"
    ic3 = number(metric.get("rank_ic_3m"))
    ic6 = number(metric.get("rank_ic_6m"))
    if ic3 is not None and ic6 is not None:
        if ic3 >= 0.1 and ic6 >= 0.1:
            verdict = "两个回看窗口均为正向"
        elif ic3 <= -0.1 and ic6 <= -0.1:
            verdict = "两个回看窗口均为反向"
    lines = [
        f"# {method_id} {first['method_name']}：当前效果摘要",
        "",
        f"- 当前运行：`{first['run_id']}`；结果生成日：{first['run_date']}。",
        f"- 当前状态：{first['status']}。",
        f"- 当前评估：{evaluation['title']}；股价截至 {evaluation['price_as_of']}。",
        f"- 证据性质：{evaluation['evidence_type']}，不能当作生成后样本外证明。",
        "- 个股口径：每家公司独立使用复权股价；190/192家公司有完整3个月和6个月数据。",
        "",
        "| 窗口 | Top20 | 全样本 | Top20-全样本 | Top20-Bottom20 | Rank IC | 行业中性IC |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, suffix in (("3个月", "3m"), ("6个月", "6m")):
        top = number(metric.get(f"top20_mean_{suffix}"))
        universe = number(metric.get(f"universe_mean_{suffix}"))
        excess = top - universe if top is not None and universe is not None else None
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    signed_pct_ratio(top),
                    signed_pct_ratio(universe),
                    signed_pct_ratio(excess),
                    signed_pct_ratio(metric.get(f"top20_bottom20_spread_{suffix}")),
                    signed(metric.get(f"rank_ic_{suffix}")),
                    signed(metric.get(f"category_neutral_rank_ic_{suffix}")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 当前解释",
            "",
            f"- 历史回看方向：{verdict}。这一判断只描述当前排名与已经发生的价格横截面是否同向。",
            f"- 管理用途：{first['role']}",
            "- 生命周期处理：本轮不自动改变既有状态；等待从当前结果生成日以后开始积累的未见样本。",
            "",
            f"完整方法比较见[本轮整体分析]({relative_link(summary_dir, report_path)})；逐次记录见[效果历史.csv]({relative_link(summary_dir, history_path)})。",
            "",
        ]
    )
    return "\n".join(lines)


def sync_status_table(registry_by_method: dict[str, list[dict[str, str]]], evaluation: dict[str, object]) -> None:
    rows = read_csv(STATUS_TABLE)
    fields = list(rows[0].keys()) if rows else []
    extra = [
        "current_run_id",
        "current_run_date",
        "current_result_path",
        "current_evaluation_id",
        "current_evaluation_path",
        "current_evidence_type",
    ]
    for field in extra:
        if field not in fields:
            fields.append(field)
    for row in rows:
        current = registry_by_method.get(row.get("method_id", ""), [])
        if not current:
            continue
        first = current[0]
        row.update(
            {
                "current_run_id": first["run_id"],
                "current_run_date": first["run_date"],
                "current_result_path": first["result_path"],
                "current_evaluation_id": str(evaluation["evaluation_id"]),
                "current_evaluation_path": str(evaluation["report_path"]),
                "current_evidence_type": str(evaluation["evidence_type"]),
            }
        )
    write_csv(STATUS_TABLE, rows, fields)


def main() -> None:
    registry_rows = [row for row in read_csv(REGISTRY) if row.get("is_current", "").lower() == "true"]
    if not registry_rows:
        raise RuntimeError("运行与榜单注册表没有 current=true 的行")
    if any(row.get("schema_version") != "1" for row in registry_rows):
        raise RuntimeError("只支持运行与榜单注册表 schema_version=1")

    evaluation = json.loads(EVALUATION_POINTER.read_text(encoding="utf-8-sig"))
    if int(evaluation.get("schema_version", 0)) != 1:
        raise RuntimeError("只支持当前评估 schema_version=1")

    normalized_path = resolve_root_path(str(evaluation["normalized_rankings_path"]))
    method_metrics_path = resolve_root_path(str(evaluation["method_metrics_path"]))
    price_returns_path = resolve_root_path(str(evaluation["price_returns_path"]))
    report_path = resolve_root_path(str(evaluation["report_path"]))
    for required in (normalized_path, method_metrics_path, price_returns_path, report_path):
        if not required.is_file():
            raise FileNotFoundError(required)

    registry_by_method: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sorted(registry_rows, key=lambda item: int(item["display_order"])):
        plan = resolve_root_path(row["plan_path"])
        result = resolve_root_path(row["result_path"])
        method_dir = resolve_root_path(row["method_path"])
        if not plan.is_file() or not result.is_file() or not method_dir.is_dir():
            raise FileNotFoundError(f"注册表路径无效：{row['list_id']}")
        if plan.name != "01_研究方案.md" or result.name != "02_排序结果.md":
            raise RuntimeError(f"只允许标准研究方案和结果文件：{row['list_id']}")
        registry_by_method[row["method_id"]].append(row)

    if len(registry_by_method) != int(evaluation["method_count"]):
        raise RuntimeError("注册表方法数与当前评估指针不一致")
    if len(registry_rows) != int(evaluation["list_count"]):
        raise RuntimeError("注册表榜单数与当前评估指针不一致")

    normalized = read_csv(normalized_path)
    normalized_counts: dict[str, int] = defaultdict(int)
    for row in normalized:
        normalized_counts[row["list_id"]] += 1
    for row in registry_rows:
        expected = int(row["expected_row_count"])
        if normalized_counts[row["list_id"]] != expected:
            raise RuntimeError(
                f"{row['list_id']} 规范化排名为 {normalized_counts[row['list_id']]} 行，预期 {expected}"
            )

    method_metrics = {row["method_id"]: row for row in read_csv(method_metrics_path)}
    missing_metrics = sorted(set(registry_by_method) - set(method_metrics))
    if missing_metrics:
        raise RuntimeError(f"缺少方法层评估：{', '.join(missing_metrics)}")

    price_rows = read_csv(price_returns_path)
    valid_price = next((row for row in price_rows if row.get("ret_3m_status") == "ok" and row.get("ret_6m_status") == "ok"), None)
    if not valid_price:
        raise RuntimeError("没有可用的3个月和6个月价格起点")
    starts = {"3M": valid_price["ret_3m_start"], "6M": valid_price["ret_6m_start"]}

    for method_id, rows in registry_by_method.items():
        first = rows[0]
        method_dir = resolve_root_path(first["method_path"])
        effects_dir = method_dir / "效果评估"
        effects_dir.mkdir(parents=True, exist_ok=True)
        current_result_path = method_dir / "01_当前排序结果.md"
        summary_path = effects_dir / "当前效果摘要.md"
        history_path = effects_dir / "效果历史.csv"
        status_path = method_dir / "00_方案状态.md"

        current_result_path.write_text(
            current_result_markdown(method_id, rows, method_dir, summary_path, report_path, REGISTRY),
            encoding="utf-8",
        )
        update_status_markdown(
            status_path,
            f"{method_id} {first['method_name']}",
            management_block(method_id, rows, method_dir, report_path),
        )

        old_history = read_csv(history_path) if history_path.exists() else []
        history = migrate_history(old_history, method_id)
        history = [
            row
            for row in history
            if not (
                row.get("evaluation_id") == evaluation["evaluation_id"]
                and row.get("run_id") == first["run_id"]
                and row.get("horizon") in {"3M", "6M"}
            )
        ]
        history.extend(current_history_rows(method_id, rows, method_metrics[method_id], evaluation, starts))
        write_csv(history_path, history, HISTORY_FIELDS)

        summary_path.write_text(
            effect_summary_markdown(
                method_id,
                rows,
                method_metrics[method_id],
                summary_path.parent,
                report_path,
                history_path,
                evaluation,
            ),
            encoding="utf-8",
        )

    sync_status_table(registry_by_method, evaluation)
    print(
        f"Synced {len(registry_by_method)} methods, {len(registry_rows)} lists, "
        f"evaluation={evaluation['evaluation_id']}"
    )


if __name__ == "__main__":
    main()
