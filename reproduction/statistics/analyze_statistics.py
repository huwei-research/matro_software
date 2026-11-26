"""Recompute the manuscript tables from the published run-level records."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
METHODS = ("matro", "newuoa_full", "newuoa_standard", "cobyqa", "nelder_mead_tight", "cmaes")
LABELS = ("MATRO", "NEWUOA (full)", "NEWUOA ($2n+1$)", "COBYQA", "Nelder--Mead", "CMA-ES")
TAUS = (1e-3, 1e-5, 1e-7, 1e-9)


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


def sign_compare(a, b):
    # Lower cost wins. Fixed absolute tolerance applies to budget fractions in [0,1].
    return "win" if a < b - 1e-12 else "loss" if a > b + 1e-12 else "tie"


def analyze():
    instances = {r["instance_id"]: r for r in read_csv(DATA / "instances.csv.gz")}
    references = {r["identity_group"]: r for r in read_csv(DATA / "references.csv.gz")}
    canonical = {r["job_id"]: r for r in read_csv(HERE / "canonical_run_values.csv.gz")}
    initial = {r["instance_id"]: r for r in read_csv(DATA / "initialization.csv.gz")}
    ref_hits = {(r["job_id"], float(r["target"])): r for r in read_csv(HERE / "reference_hit_checks.csv.gz")}
    assert len(instances) == 147 and len(references) == 136
    assert set(instances) == set(initial)
    counts = Counter(row["identity_group"] for row in instances.values())
    mapping = []
    for instance_id in sorted(instances):
        s, init = instances[instance_id], initial[instance_id]
        identity = s["identity_group"]
        mapping.append(dict(instance_id=instance_id, name=s["name"], suite=s["suite"], n=s["n"],
            identity_group=identity, configurations_per_identity=counts[identity],
            initial_radius=init["radius"], coordinate_condition=init["coordinate_condition"],
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
        identity = instances[row["instance_id"]]["identity_group"]
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
            [DATA / "runs.csv.gz", DATA / "instances.csv.gz", DATA / "references.csv.gz",
             DATA / "initialization.csv.gz", DATA / "starts.csv.gz",
             HERE / "reference_hit_checks.csv.gz", HERE / "canonical_run_values.csv.gz"]}))
    benchmark_dims = []
    for dimension in sorted({int(row["n"]) for row in instances.values()}):
        benchmark_dims.append(dict(n=dimension,
            mw=sum(int(row["n"]) == dimension and row["suite"] == "mw" for row in instances.values()),
            cutest_s2mpj=sum(int(row["n"]) == dimension and row["suite"] == "cutest_s2mpj" for row in instances.values())))
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


if __name__ == "__main__":
    analyze()
    print(f"Peak resident memory: {peak_memory_bytes()} bytes", flush=True)
