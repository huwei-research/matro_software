"""Recompute MATRO benchmark statistics from saved records, without objectives/solvers.

Default mode uses only the small, paper data and statistics inputs.
The optional preparation modes read the historical analysis and query archive.
Python 3.10+ standard library only.  All files are relative to this script.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
METHODS = ("matro", "newuoa_full", "newuoa_standard", "cobyqa", "nelder_mead_tight", "cmaes")
LABELS = ("MATRO", "NEWUOA (full)", "NEWUOA ($2n+1$)", "COBYQA", "Nelder--Mead", "CMA-ES")
TAUS = (1e-3, 1e-5, 1e-7, 1e-9)
PREFIX = "MATRO_selection_20261030/formal_dimension_order_20261101/"


def read_csv(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)


def write_csv(name, rows, fields=None):
    rows = list(rows)
    if fields is None:
        fields = list(rows[0]) if rows else []
    path = HERE / name
    if str(path).endswith(".gz"):
        # Zero timestamp permits byte-for-byte regeneration on every machine.
        with path.open("wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as packed:
                with io.TextIOWrapper(packed, encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
                    writer.writeheader()
                    writer.writerows(rows)
    else:
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def peak_memory_bytes():
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                (name, ctypes.c_size_t) for name in ("PeakWorkingSetSize", "WorkingSetSize",
                "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        if psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            return counters.PeakWorkingSetSize
        return None
    try:
        import resource
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return value if sys.platform == "darwin" else 1024 * value
    except ImportError:
        return None


def truth(value):
    return str(value).lower() == "true"


def hit_value(value):
    return int(float(value)) if value not in (None, "", "None", "nan") else None


def threshold(reference, tau, f0):
    # The exact historical target computation, including its floating-point order.
    return reference + tau * max(0.0, f0 - reference)


def preparation(source):
    """Capture compact provenance inputs; preserve every original artifact."""
    rows = list(read_csv(source / "candidate_ranking.csv"))
    fields = ["instance_id", "suite", "name", "n", "identity_group", "expected_starts",
              "expected_runs", "available_runs", "terminal_errors", "nonfinite_queries",
              "extreme_queries", "model_nonfinite_states", "audit_errors", "any_success_fraction",
              "trivial_fraction", "discriminating_fraction", "eligible", "exclusion_reasons",
              "selection_score", "rank", "selected"]
    write_csv("candidate_inventory.csv.gz", ({k: r[k] for k in fields} for r in rows), fields)
    receipt = {"source_analysis": str(source.resolve()),
               "analysis_receipt": json.loads((source / "analysis_receipt.json").read_text(encoding="utf-8-sig")),
               "scope_receipt": json.loads((source / "scope_receipt.json").read_text(encoding="utf-8-sig")),
               "source_sha256": {name: sha256(source / name) for name in
                   ("candidate_ranking.csv", "analysis_receipt.json", "scope_receipt.json", "runs_metrics.csv.gz", "selection_rules.json")}}
    write_json("provenance_source.json", receipt)
    # All 211 terminal candidate configurations, including qualification failures.
    acc = defaultdict(lambda: [0, 0, 0.0])
    selected = {r["instance_id"] for r in read_csv(DATA / "selected147_instances.csv.gz")}
    compact = {(r["job_id"], float(r["target"])): r for r in read_csv(DATA / "runs.csv.gz")}
    canonical = {}
    for row in read_csv(source / "runs_metrics.csv.gz"):
        key = (float(row["target"]), row["method"])
        hit = hit_value(row["hit"])
        budget = int(row["budget"])
        a = acc[key]
        a[0] += 1
        a[1] += hit is not None
        a[2] += (hit if hit is not None else budget) / budget
        if row["instance_id"] in selected:
            original = compact[row["job_id"], float(row["target"])]
            assert hit_value(original["hit"]) == hit
            canonical[row["job_id"]] = {k: row[k] for k in ("job_id", "f0", "reference", "attempt")}
    records = []
    for tau in TAUS:
        for method in METHODS:
            count, solved, total = acc[tau, method]
            records.append(dict(target=tau, method=method, tasks=count, successes=solved,
                                success_rate=solved / count, mean_capped_budget_fraction=total / count))
    write_csv("candidate_pool_summary.csv", records)
    write_csv("canonical_run_values.csv.gz", [canonical[k] for k in sorted(canonical)])


def recover_reference_hits(source, archive):
    """Recover exact first hits only where reference changes alter thresholds."""
    identities = {r["instance_id"]: r["identity_group"] for r in read_csv(DATA / "selected147_instances.csv.gz")}
    refs = {r["identity_group"]: r for r in read_csv(DATA / "references.csv.gz")}
    canonical = {r["job_id"]: r for r in read_csv(HERE / "canonical_run_values.csv.gz")}
    needed = defaultdict(list)
    for row in read_csv(DATA / "runs.csv.gz"):
        declared = float(refs[identities[row["instance_id"]]]["declared_reference"])
        exact = canonical[row["job_id"]]
        pooled = float(exact["reference"])
        tau, f0 = float(row["target"]), float(exact["f0"])
        assert pooled == float(refs[identities[row["instance_id"]]]["unified_reference"])
        old, new = threshold(pooled, tau, f0), threshold(declared, tau, f0)
        if old != new:
            needed[row["job_id"]].append(dict(target=tau, pooled_threshold=old,
                declared_threshold=new, expected_pooled_hit=hit_value(row["hit"])))
    attempts = {job: canonical[job]["attempt"].replace("\\", "/") for job in needed}
    assert set(attempts) == set(needed)
    hit_rows, member_rows = [], []
    completed_queries = 0
    with zipfile.ZipFile(archive) as zipped:
        # Keep compressed-member offset order to reduce HDD seek overhead.
        ordered = sorted(needed, key=lambda j: zipped.getinfo(PREFIX + attempts[j] + "/calls.jsonl").header_offset)
        for number, job_id in enumerate(ordered, 1):
            records = needed[job_id]
            member = PREFIX + attempts[job_id] + "/calls.jsonl"
            info = zipped.getinfo(member)
            h = hashlib.sha256()
            pooled_hits = [None] * len(records)
            declared_hits = [None] * len(records)
            count = 0
            stopped_after_all_hits = False
            with zipped.open(info) as stream:
                for count, line in enumerate(stream, 1):
                    h.update(line)
                    call = json.loads(line)
                    value = float(call["f"])
                    assert int(call["nfev"]) == count, (job_id, count, call["nfev"])
                    if not math.isfinite(value):
                        continue
                    for k, record in enumerate(records):
                        if pooled_hits[k] is None and value <= record["pooled_threshold"]:
                            pooled_hits[k] = count
                        if declared_hits[k] is None and value <= record["declared_threshold"]:
                            declared_hits[k] = count
                    if all(hit is not None for hit in pooled_hits + declared_hits):
                        stopped_after_all_hits = True
                        break
            completed_queries += count
            for record, pooled_hit, declared_hit in zip(records, pooled_hits, declared_hits):
                assert pooled_hit == record["expected_pooled_hit"], (job_id, record, pooled_hit)
                assert pooled_hit is None or (declared_hit is not None and declared_hit <= pooled_hit)
                hit_rows.append(dict(job_id=job_id, target=record["target"],
                    pooled_threshold=record["pooled_threshold"], declared_threshold=record["declared_threshold"],
                    pooled_hit=pooled_hit, declared_hit=declared_hit))
            member_rows.append(dict(job_id=job_id, member=member, queries_read=count,
                stopped_after_all_hits=stopped_after_all_hits, crc32=f"{info.CRC:08x}",
                full_uncompressed_bytes=info.file_size, read_prefix_sha256=h.hexdigest()))
            if number % 500 == 0:
                print(f"Reference recovery: {number}/{len(ordered)} saved runs; {completed_queries:,} queries read", flush=True)
    write_csv("reference_hit_checks.csv.gz", sorted(hit_rows, key=lambda r: (r["job_id"], -r["target"])))
    write_csv("reference_query_members.csv.gz", sorted(member_rows, key=lambda r: r["job_id"]))
    write_json("reference_recovery_receipt.json", dict(
        archive=str(archive.resolve()), archive_bytes=archive.stat().st_size,
        source_analysis=str(source.resolve()), queried_saved_runs=len(needed),
        changed_threshold_records=len(hit_rows), saved_queries_read=completed_queries,
        exact_pooled_hit_checks=len(hit_rows), pooled_hit_mismatches=0,
        new_objective_evaluations=0, optimizer_runs=0,
        runs_input_sha256=sha256(DATA / "runs.csv.gz"),
        references_input_sha256=sha256(DATA / "references.csv.gz")))


def sign_compare(a, b):
    # Lower cost wins. Fixed absolute tolerance applies to budget fractions in [0,1].
    return "win" if a < b - 1e-12 else "loss" if a > b + 1e-12 else "tie"


def analyze():
    selected = {r["instance_id"]: r for r in read_csv(DATA / "selected147_instances.csv.gz")}
    references = {r["identity_group"]: r for r in read_csv(DATA / "references.csv.gz")}
    canonical = {r["job_id"]: r for r in read_csv(HERE / "canonical_run_values.csv.gz")}
    initial = {r["instance_id"]: r for r in read_csv(DATA / "initialization.csv.gz")}
    ref_hits = {(r["job_id"], float(r["target"])): r for r in read_csv(HERE / "reference_hit_checks.csv.gz")}
    inventories = list(read_csv(HERE / "candidate_inventory.csv.gz"))
    assert len(selected) == 147 and len(references) == 136
    assert {r["instance_id"] for r in inventories if truth(r["eligible"])} == set(selected)
    assert {r["instance_id"] for r in inventories if truth(r["selected"])} == set(selected)
    counts = Counter(r["identity_group"] for r in selected.values())
    dims = []
    for n in sorted({int(r["n"]) for r in inventories}):
        row = dict(n=n)
        for suite in ("mw", "cutest_s2mpj"):
            row[suite + "_candidates"] = sum(int(r["n"]) == n and r["suite"] == suite for r in inventories)
            row[suite + "_retained"] = sum(int(r["n"]) == n and r["suite"] == suite and truth(r["selected"]) for r in inventories)
        dims.append(row)
    write_csv("candidate_distribution.csv", dims)
    reason_patterns = Counter()
    first_reasons = Counter()
    for r in inventories:
        if not truth(r["eligible"]):
            reasons = ast.literal_eval(r["exclusion_reasons"])
            normalized = ["verified cross-library duplicate" if s.startswith("verified cross-library duplicate") else s for s in reasons]
            reason_patterns["; ".join(normalized)] += 1
            first_reasons[normalized[0]] += 1
    write_csv("exclusion_combinations.csv", [dict(reasons=k, configurations=v) for k, v in sorted(reason_patterns.items())])
    write_csv("exclusion_first_reason.csv", [dict(first_reason=k, configurations=v) for k, v in first_reasons.items()])
    mapping = []
    for instance_id in sorted(selected):
        s, init = selected[instance_id], initial[instance_id]
        identity = s["identity_group"]
        mapping.append(dict(instance_id=instance_id, name=s["name"], suite=s["suite"], n=s["n"],
            identity_group=identity, configurations_per_identity=counts[identity],
            initial_radius=init["radius"], coordinate_condition=init["coordinate_condition"],
            initialization_source=init["source"], calibration_candidate_id=init["candidate_id"],
            declared_reference=references[identity]["declared_reference"],
            pooled_reference=references[identity]["unified_reference"],
            initialization_record="../data/initialization.csv.gz", starts_record="../data/starts.csv.gz"))
    write_csv("configuration_mapping.csv.gz", mapping)
    # Equal-objective average: within each identity average all configurations and starts;
    # then average the 136 identity-level values, once per identity.
    identity_acc = defaultdict(lambda: [0, 0, 0.0])
    paired_acc = defaultdict(lambda: [0, 0, 0.0])
    sensitivity = defaultdict(lambda: [0, 0, 0, 0])
    identity_sensitivity = defaultdict(lambda: [0, 0])
    records_count = 0
    reused_identical_thresholds = 0
    seen_runs = set()
    paired_inputs = {}
    unique_records = set()
    rounded_reference_identities = set()
    rounded_initial_value_jobs = set()
    nonpositive_initial_gaps = set()
    for row in read_csv(DATA / "runs.csv.gz"):
        records_count += 1
        job, tau, method = row["job_id"], float(row["target"]), row["method"]
        assert method in METHODS and (job, tau) not in unique_records
        unique_records.add((job, tau))
        seen_runs.add(job)
        identity = selected[row["instance_id"]]["identity_group"]
        exact = canonical[job]
        assert float(exact["reference"]) == float(references[identity]["unified_reference"])
        if float(exact["reference"]) != float(row["reference"]):
            rounded_reference_identities.add(identity)
        if float(exact["f0"]) != float(row["f0"]):
            rounded_initial_value_jobs.add(job)
        if float(exact["f0"]) <= float(references[identity]["declared_reference"]):
            nonpositive_initial_gaps.add((row["instance_id"], row["start_id"]))
        budget, n = int(row["budget"]), int(row["n"])
        assert budget == 500 * (n + 1)
        paired_key = (row["instance_id"], int(row["start_id"]))
        inputs = (float(exact["f0"]), n, budget, float(row["radius"]))
        assert paired_inputs.setdefault(paired_key, inputs) == inputs
        pooled_hit = hit_value(row["hit"])
        assert (pooled_hit is not None) == truth(row["success"])
        alternative = ref_hits.get((job, tau))
        if alternative is not None:
            assert hit_value(alternative["pooled_hit"]) == pooled_hit
            assert float(alternative["pooled_threshold"]) == threshold(float(exact["reference"]), tau, float(exact["f0"]))
            assert float(alternative["declared_threshold"]) == threshold(float(references[identity]["declared_reference"]), tau, float(exact["f0"]))
            declared_hit = hit_value(alternative["declared_hit"])
        else:
            declared = float(references[identity]["declared_reference"])
            pooled = float(exact["reference"])
            f0 = float(exact["f0"])
            assert threshold(declared, tau, f0) == threshold(pooled, tau, f0)
            declared_hit = pooled_hit
            reused_identical_thresholds += 1
        assert pooled_hit is None or (declared_hit is not None and declared_hit <= pooled_hit)
        assert all(hit is None or 1 <= hit <= budget for hit in (pooled_hit, declared_hit))
        for mode, hit in (("pooled", pooled_hit), ("declared", declared_hit)):
            a = identity_acc[mode, tau, method, identity]
            b = paired_acc[mode, tau, method]
            for entry in (a, b):
                entry[0] += 1
                entry[1] += hit is not None
                entry[2] += (hit if hit is not None else budget) / budget
        d = sensitivity[tau, method]
        d[0] += 1
        d[1] += alternative is not None
        d[2] += declared_hit != pooled_hit
        d[3] += (declared_hit is not None) != (pooled_hit is not None)
        if declared_hit != pooled_hit:
            di = identity_sensitivity[tau, method, identity]
            di[0] += 1
            di[1] += (declared_hit is not None) != (pooled_hit is not None)
    assert records_count == 70560 and len(seen_runs) == 17640 and len(paired_inputs) == 2940
    objective_rows = []
    for (mode, tau, method, identity), (number, success, cost) in sorted(identity_acc.items()):
        assert number == 20 * counts[identity]
        objective_rows.append(dict(reference_mode=mode, target=tau, method=method,
            identity_group=identity, configurations=counts[identity], tasks=number,
            success_rate=success / number, mean_capped_budget_fraction=cost / number,
            mean_capped_dimension_normalized_evaluations=500 * cost / number))
    write_csv("objective_level_results.csv.gz", objective_rows)
    summaries = []
    lookup = {}
    for mode in ("pooled", "declared"):
        for tau in TAUS:
            for method in METHODS:
                subset = [r for r in objective_rows if (r["reference_mode"], r["target"], r["method"]) == (mode, tau, method)]
                number, solved, cost = paired_acc[mode, tau, method]
                summary = dict(reference_mode=mode, target=tau, method=method, identities=len(subset), tasks=number,
                    successes=solved, paired_success_rate=solved / number,
                    paired_mean_capped_budget_fraction=cost / number,
                    objective_success_rate=sum(r["success_rate"] for r in subset) / len(subset),
                    objective_mean_capped_budget_fraction=sum(r["mean_capped_budget_fraction"] for r in subset) / len(subset),
                    objective_mean_capped_dimension_normalized_evaluations=sum(r["mean_capped_dimension_normalized_evaluations"] for r in subset) / len(subset))
                summaries.append(summary)
                lookup[mode, tau, method] = summary
    write_csv("objective_summary.csv", summaries)
    wtl_rows = []
    for mode in ("pooled", "declared"):
        for tau in TAUS:
            tally = Counter()
            for identity in counts:
                a = identity_acc[mode, tau, "matro", identity]
                b = identity_acc[mode, tau, "newuoa_full", identity]
                tally["cost_" + sign_compare(a[2] / a[0], b[2] / b[0])] += 1
                tally["success_" + sign_compare(-a[1] / a[0], -b[1] / b[0])] += 1
            wtl_rows.append(dict(reference_mode=mode, target=tau, identities=136,
                **{key: tally[key] for key in ("cost_win", "cost_tie", "cost_loss", "success_win", "success_tie", "success_loss")}))
    write_csv("matro_full_objective_wtl.csv", wtl_rows)
    changes = []
    for tau in TAUS:
        for method in METHODS:
            d = sensitivity[tau, method]
            old, new = lookup["pooled", tau, method], lookup["declared", tau, method]
            changes.append(dict(target=tau, method=method, tasks=d[0], changed_thresholds=d[1],
                changed_first_hits=d[2], newly_successful_tasks=d[3],
                pooled_paired_success=old["paired_success_rate"], declared_paired_success=new["paired_success_rate"],
                pooled_objective_success=old["objective_success_rate"], declared_objective_success=new["objective_success_rate"],
                pooled_objective_capped_fraction=old["objective_mean_capped_budget_fraction"],
                declared_objective_capped_fraction=new["objective_mean_capped_budget_fraction"]))
    write_csv("reference_sensitivity.csv", changes)
    write_csv("reference_changes_by_identity.csv.gz", [dict(target=tau, method=method,
        identity_group=identity, changed_first_hits=value[0], newly_successful_tasks=value[1],
        declared_reference=references[identity]["declared_reference"],
        pooled_reference=references[identity]["unified_reference"])
        for (tau, method, identity), value in sorted(identity_sensitivity.items())])
    write_json("statistics_receipt.json", dict(
        configurations=147, identities=136, starts_per_configuration=20, solvers=6,
        paired_tasks_per_solver=2940, runs=len(seen_runs), run_target_records=records_count,
        configuration_multiplicity_histogram=dict(sorted(Counter(counts.values()).items())),
        candidate_configurations=len(inventories), eligible_configurations=sum(truth(r["eligible"]) for r in inventories),
        eligible_equals_selected=True, score_truncated_eligible_membership=False,
        distinct_references=sum(float(r["declared_reference"]) != float(r["unified_reference"]) for r in references.values()),
        exactly_equal_threshold_records=reused_identical_thresholds,
        recovered_changed_threshold_records=len(ref_hits), new_objective_evaluations=0,
        compact_reference_roundtrip_identity_count=len(rounded_reference_identities),
        compact_initial_value_roundtrip_job_count=len(rounded_initial_value_jobs),
        declared_reference_nonpositive_initial_gap_tasks=len(nonpositive_initial_gaps),
        cost_definition="first-hit/B on success, 1 on failure; B=500(n+1)",
        objective_weighting="equal within identity over configurations and starts, then equal over 136 identities",
        wtl_cost_tolerance=1e-12,
        source_hashes={p.relative_to(HERE.parent).as_posix(): sha256(p) for p in
            [DATA / "runs.csv.gz", DATA / "selected147_instances.csv.gz", DATA / "references.csv.gz",
             DATA / "initialization.csv.gz", DATA / "starts.csv.gz", HERE / "candidate_inventory.csv.gz",
             HERE / "reference_hit_checks.csv.gz", HERE / "canonical_run_values.csv.gz"]}))
    benchmark_dims = []
    for dimension in sorted({int(row["n"]) for row in selected.values()}):
        benchmark_dims.append(dict(n=dimension,
            mw=sum(int(row["n"]) == dimension and row["suite"] == "mw" for row in selected.values()),
            cutest_s2mpj=sum(int(row["n"]) == dimension and row["suite"] == "cutest_s2mpj" for row in selected.values())))
    assert [row["n"] for row in benchmark_dims] == list(range(2, 13))
    assert sum(row["mw"] for row in benchmark_dims) == 41
    assert sum(row["cutest_s2mpj"] for row in benchmark_dims) == 106
    assert sum(row["mw"] + row["cutest_s2mpj"] for row in benchmark_dims) == 147
    write_csv("instance_distribution.csv", benchmark_dims)
    tables(lookup, wtl_rows, benchmark_dims)
    print("Verified 147 configurations, 136 identities, 17,640 runs and 70,560 target records.")
    for method in METHODS:
        r = lookup["pooled", 1e-7, method]
        print(f"{method:20s} objective success={r['objective_success_rate']:.8f}; capped/(n+1)={r['objective_mean_capped_dimension_normalized_evaluations']:.8f}")


def tables(lookup, wtl, dims):
    br = " \\\\"

    def summary_table(mode, paired, filename):
        # Separate metrics into panels so units and best entries remain explicit.
        text = [r"\begin{tabular}{lrrrr}", r"\toprule"]

        def values(row):
            if paired:
                return (100 * row["paired_success_rate"],
                        500 * row["paired_mean_capped_budget_fraction"])
            return (100 * row["objective_success_rate"],
                    row["objective_mean_capped_dimension_normalized_evaluations"])

        best = {tau: (max(values(lookup[mode, tau, m])[0] for m in METHODS),
                      min(values(lookup[mode, tau, m])[1] for m in METHODS))
                for tau in TAUS}
        for index, title, digits in (
                (0, "Success rate (\\%)", 2),
                (1, "Mean normalized capped evaluations", 1)):
            if index:
                text.append(r"\midrule")
            text.append(r"\multicolumn{5}{c}{" + title + "}" + br)
            text.append(r"\cmidrule(lr){1-5}")
            text.append("Method & " + " & ".join(
                "$10^{" + str(round(math.log10(tau))) + "}$"
                for tau in TAUS) + br)
            text.append(r"\midrule")
            for method, label in zip(METHODS, LABELS):
                cells = []
                for tau in TAUS:
                    value = values(lookup[mode, tau, method])[index]
                    cell = f"{value:.{digits}f}"
                    if abs(value - best[tau][index]) <= 1e-12:
                        cell = r"\textbf{" + cell + "}"
                    cells.append(cell)
                text.append(label + " & " + " & ".join(cells) + br)
        text.extend([r"\bottomrule", r"\end{tabular}"])
        (HERE / filename).write_text("\n".join(text) + "\n", encoding="utf-8")

    summary_table("pooled", True, "table_paired_summary.tex")
    summary_table("pooled", False, "table_objective_summary.tex")
    summary_table("declared", False, "table_declared_summary.tex")
    text = [r"\begin{tabular}{rrr}", r"\toprule",
            r"Dimension $n$ & Mor\'e--Wild & CUTEst/S2MPJ" + br, r"\midrule"]
    for row in dims:
        text.append(" & ".join(str(row[key]) for key in ("n", "mw", "cutest_s2mpj")) + br)
    text.extend([r"\midrule", "Total & " + " & ".join(str(sum(row[key] for row in dims))
        for key in ("mw", "cutest_s2mpj")) + br, r"\bottomrule", r"\end{tabular}"])
    (HERE / "table_instance_distribution.tex").write_text("\n".join(text) + "\n", encoding="utf-8")
    text = [r"\begin{tabular}{lrrr}", r"\toprule", r"& \multicolumn{2}{c}{Pooled reference} & Declared reference" + br,
            r"Target & Capped-count W/T/L & Success W/T/L & Capped-count W/T/L" + br, r"\midrule"]
    index = {(r["reference_mode"], r["target"]): r for r in wtl}
    for tau in TAUS:
        pooled, declared = index["pooled", tau], index["declared", tau]
        def triple(row, kind):
            return "/".join(str(row[kind + "_" + key]) for key in ("win", "tie", "loss"))
        exponent = round(math.log10(tau))
        text.append(f"$10^{{{exponent}}}$ & {triple(pooled, 'cost')} & {triple(pooled, 'success')} & {triple(declared, 'cost')}" + br)
    text.extend([r"\bottomrule", r"\end{tabular}"])
    (HERE / "table_objective_wtl.tex").write_text("\n".join(text) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-source", type=Path, help="historical analysis directory; save compact provenance inputs")
    parser.add_argument("--recover-reference-hits", type=Path, metavar="ARCHIVE", help="read exact saved calls.jsonl members from archive; requires --prepare-source")
    args = parser.parse_args()
    if args.prepare_source:
        preparation(args.prepare_source)
    if args.recover_reference_hits:
        if not args.prepare_source:
            parser.error("--recover-reference-hits requires --prepare-source")
        recover_reference_hits(args.prepare_source, args.recover_reference_hits)
    analyze()
    print(f"Peak resident memory: {peak_memory_bytes()} bytes", flush=True)


if __name__ == "__main__":
    main()
