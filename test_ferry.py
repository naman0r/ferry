"""Offline checks for ferry. Run: python3 test_ferry.py"""
import os
import tempfile
from importlib.machinery import SourceFileLoader

ferry = SourceFileLoader("ferry", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ferry")).load_module()

assert ferry.remote_path("") == "Ferry"
assert ferry.remote_path("a b/c.txt") == "Ferry/a b/c.txt"
assert ferry.remote_path("../x") == "x"
assert ferry.remote_path("~") == "."
assert ferry.remote_path("~/developer/x") == "developer/x"
assert ferry.remote_path("/tmp/x") == "/tmp/x"

with tempfile.TemporaryDirectory() as d:
    src = os.path.join(d, "src")
    os.makedirs(os.path.join(src, "sub", ".ferry-partial"))
    open(os.path.join(src, "sub", "f.txt"), "w").write("hi")
    open(os.path.join(src, ".DS_Store"), "w").write("x")
    os.symlink("sub/f.txt", os.path.join(src, "ln"))
    m = ferry.manifest([src, os.path.join(d, "missing")])
    assert m[os.path.join(d, "missing")] is None
    assert m[src] == {
        ".": "dir",
        "sub": "dir",
        "ln": "link:sub/f.txt",
        "sub/f.txt": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
    }, m[src]

    same = {"dst": dict(m[src])}
    assert ferry.mismatches(same, same) == []
    changed = {"dst": dict(m[src], **{"sub/f.txt": "0"})}
    assert ferry.mismatches(same, changed) == ["dst/sub/f.txt"]
    assert sorted(ferry.mismatches(same, {"dst": None})) == ["dst", "dst/ln", "dst/sub", "dst/sub/f.txt"]
    # Extra files already sitting at the destination are not a failure.
    assert ferry.mismatches(same, {"dst": dict(m[src], extra="1")}) == []

print("ok")
