"""Python reference results for the sequence lesson (bio_sequence_analysis.py, ip3r_analysis.py), offline parts only.

The NCBI download steps need the network; here a sequence the user pastes is analysed with the scripts' own methods.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TOP = 5  # most common repeats listed per length


def clean(seq: str) -> str:
    """Upper-case, RNA U -> T, keep only A/C/G/T (the scripts' tables assume these letters)."""
    return "".join(c for c in seq.upper().replace("U", "T") if c in "ACGT")


def sequence(p):
    from bio_sequence_analysis import NCBISequenceAnalyzer
    a = NCBISequenceAnalyzer("offline@example.org")    # no NCBI call is made
    a.sequence = clean(p["seq"])
    a.gene_info = {"name": "mRNA" if p.get("mrna") else ""}
    r = a.analyze_sequence()
    reps = {}
    for k, d in r["repeats"].items():
        top = sorted(d.items(), key=lambda kv: -kv[1])[:TOP]
        reps[str(k)] = {"distinct": len(d), "top": [list(t) for t in top]}
    s, w = a.sequence, 100
    windows = [(s[i:i + w].count("G") + s[i:i + w].count("C")) / w for i in range(0, len(s) - w, w)]
    return {"length": r["length"], "gc_content": r["gc_content"],
            "counts": [s.count(n) for n in "ATGC"],
            "codons": {**r["codon_analysis"], "most_common": [list(t) for t in r["codon_analysis"]["most_common"]]},
            "repeats": reps, "gc_windows": windows, "patterns": r["mathematical_patterns"]}


def ip3r(p):
    from ip3r_analysis import IP3RAnalyzer
    a = IP3RAnalyzer("offline@example.org")
    s = clean(p["seq"])
    return {"cds": list(a.find_cds(s)), "protein": a.cds_protein(s)[1],
            "domains": a.analyze_domains(s), "sites": a.find_calcium_binding_sites(s)}
