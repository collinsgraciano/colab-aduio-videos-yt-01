import os, re

d = "C:/zcode/yt-chinese-aduio-video/pipeline"
issues = []

for f in sorted(os.listdir(d)):
    if not f.endswith(".py"):
        continue
    lines = open(os.path.join(d, f), encoding="utf-8").readlines()
    for i, line in enumerate(lines, 1):
        s = line.rstrip()
        # Find lines ending with stray " like: return result"
        # Also: lines that end with " that isn't part of a string or comment
        if re.search(r'^\s*(return|raise|break|continue|pass)\s+.*\"$', s):
            # Check if the " is stray (not a legit closing of a string)
            # Simple heuristic: if line already has an odd # of quotes before the last one
            before_last = s[:-1]
            quoted_parts = re.findall(r'"(?:[^"\\]|\\.)*"', before_last)
            remaining = before_last
            for q in quoted_parts:
                remaining = remaining.replace(q, "", 1)
            # If remaining has no unmatched ", the last " is stray
            if '"' not in remaining:
                issues.append((f, i, s))

for f, n, s in issues:
    print(f"  ⚠️  {f}:{n}  {s}")

if not issues:
    print("  ✅ No stray quotes found")
else:
    print(f"\nTotal: {len(issues)} issues")