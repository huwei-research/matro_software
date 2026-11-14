"""Check the paper's compact tables without loading raw optimization archives."""
from pathlib import Path
import csv
import gzip
import hashlib
import json
from collections import Counter

HERE = Path(__file__).resolve().parent


def rows(name):
    path = HERE / name
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


instances = list(rows("selected147_instances.csv.gz"))
ids = {row["instance_id"] for row in instances}
assert len(ids) == len(instances) == 147
assert Counter(row["suite"] for row in instances) == {"mw": 41, "cutest_s2mpj": 106}
assert min(int(row["n"]) for row in instances) == 2
assert max(int(row["n"]) for row in instances) == 12
starts = list(rows("starts.csv.gz"))
assert len(starts) == 2940
assert Counter(row["instance_id"] for row in starts) == {key: 20 for key in ids}
initialization = list(rows("initialization.csv.gz"))
assert {row["instance_id"] for row in initialization} == ids
assert Counter(row["source"] for row in initialization) == {
    "completed_development": 54, "new_per_instance_calibration": 93}

totals, success, keys = Counter(), Counter(), set()
pair_inputs = {}
for row in rows("runs.csv.gz"):
    key = row["instance_id"], row["start_id"], row["method"], row["target"]
    assert key not in keys
    keys.add(key)
    assert row["instance_id"] in ids
    target = float(row["target"])
    totals[row["method"], target] += 1
    budget, n = int(row["budget"]), int(row["n"])
    assert budget == 500 * (n + 1)
    assert float(row["f0"]) > float(row["reference"])
    hit = float(row["hit"]) if row["hit"] else float("inf")
    solved = row["success"] == "True"
    assert solved == (hit <= budget)
    if solved:
        assert 1 <= hit <= int(row["actual_calls"])
        success[row["method"], target] += 1
    pk = row["instance_id"], row["start_id"]
    inputs = row["n"], row["budget"], row["radius"], row["f0"], row["reference"]
    assert pk not in pair_inputs or pair_inputs[pk] == inputs
    pair_inputs[pk] = inputs
assert len(keys) == 70560 and len(pair_inputs) == 2940
assert set(totals.values()) == {2940} and len(totals) == 24
expected = {
    "matro": [2848, 2827, 2787, 2676],
    "newuoa_full": [2845, 2820, 2560, 2353],
    "newuoa_standard": [2858, 2752, 2481, 2301],
    "cobyqa": [2852, 2770, 2604, 2354],
    "nelder_mead_tight": [2808, 2745, 2571, 2373],
    "cmaes": [2680, 2606, 2454, 2314],
}
targets = (1e-3, 1e-5, 1e-7, 1e-9)
for method, counts in expected.items():
    assert [success[method, t] for t in targets] == counts

main = {"mw_07", "mw_12", "mw_19", "mw_27"}
condition = list(rows("conditioning_summary.csv"))
condition_counts = {}
for kappa, wanted in [(10000., [151, 6]), (100000., [105, 0])]:
    computed = []
    for variant in ("dynamic_full", "sphere"):
        selected = [r for r in condition if r["instance_id"] in main
                    and float(r["kappa"]) == kappa and r["variant"] == variant]
        assert len(selected) == 4
        computed.append(round(sum(float(r["success"]) * 40 for r in selected)))
    assert computed == wanted
    condition_counts[str(kappa)] = computed

shape = list(rows("shape_summary.csv"))
assert all(int(r["successes"]) == 20 for r in shape if r["instance_id"] in main)
coverage = json.loads((HERE / "coverage_metrics.json").read_text())
assert abs(coverage["rms_ratio"] - 7.528053427440278) < 1e-12
assert abs(coverage["area_sphere"] - coverage["area_ellipse"]) < 1e-14

manifest = json.loads((HERE / "source_manifest.json").read_text())
checked_hashes = 0
for entry in manifest["sources"]:
    relative = Path(entry["destination"])
    if relative.parts[0] == "data":
        current = HERE / relative.name
        assert hashlib.sha256(current.read_bytes()).hexdigest() == entry["output_sha256"]
        checked_hashes += 1
peak_bytes = None
try:
    import psutil
    info = psutil.Process().memory_info()
    peak_bytes = getattr(info, "peak_wset", info.rss)
    assert peak_bytes < manifest["verification_memory_budget_bytes"]
except ImportError:
    pass
result = dict(passed=True, instances=147, starts=2940, unique_runs=17640,
              run_target_rows=70560, counts=expected,
              condition_success_counts=condition_counts,
              verified_compact_source_hashes=checked_hashes,
              process_peak_working_set_bytes=peak_bytes)
(HERE / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
