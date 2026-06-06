#!/usr/bin/env python3
"""Static AI SDLC controls for the org-level agent fleet.

No network, no third-party dependencies. This is intentionally conservative:
it validates inventory parity, skill coverage, eval coverage, CODEOWNERS and
control evidence so governance drift fails before templates are adopted.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_CODEOWNERS = [
    ".github/workflows/",
    ".github/scripts/",
    ".github/ai-sdlc/",
    ".claude/skills/",
    "workflow-templates/",
    "CLAUDE.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def agent_names_from_skills() -> set[str]:
    return {
        path.name.removeprefix("agent-")
        for path in (ROOT / ".claude" / "skills").iterdir()
        if path.is_dir() and path.name.startswith("agent-")
    }


def labels_from_labels_yml() -> set[str]:
    text = read("workflow-templates/labels.yml")
    return set(re.findall(r'name:\s+"agent:([^"]+)"', text))


def issue_template_options() -> set[str]:
    text = read(".github/ISSUE_TEMPLATE/agent_task.yml")
    in_agent_dropdown = False
    options: set[str] = set()
    for line in text.splitlines():
        if re.match(r"\s+id:\s+agent\s*$", line):
            in_agent_dropdown = True
            continue
        if in_agent_dropdown and re.match(r"\s+id:\s+", line):
            break
        if in_agent_dropdown:
            match = re.match(r"\s+-\s+([a-z][a-z0-9_-]*)\s*$", line)
            if match:
                options.add(match.group(1))
    return options


def validate_inventory() -> set[str]:
    skills = agent_names_from_skills()
    labels = labels_from_labels_yml()
    issue_options = issue_template_options()
    bom = load_json(".github/ai-sdlc/ai-bom.json")
    bom_agents = {agent["name"] for agent in bom["agents"]}

    if skills != labels:
        fail(f"skill/label mismatch: skills={sorted(skills)} labels={sorted(labels)}")
    if skills != issue_options:
        fail(f"skill/issue-template mismatch: skills={sorted(skills)} issue={sorted(issue_options)}")
    if skills != bom_agents:
        fail(f"skill/AI-BOM mismatch: skills={sorted(skills)} bom={sorted(bom_agents)}")

    for agent in sorted(skills):
        for suffix in [".yml", ".properties.json"]:
            path = ROOT / "workflow-templates" / f"agent-{agent}{suffix}"
            if not path.exists():
                fail(f"missing workflow template artifact: {path.relative_to(ROOT)}")
        skill_path = ROOT / ".claude" / "skills" / f"agent-{agent}" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            fail(f"missing frontmatter: {skill_path.relative_to(ROOT)}")
        if f"name: agent-{agent}" not in text:
            fail(f"skill frontmatter name mismatch: {skill_path.relative_to(ROOT)}")
        if "disable-model-invocation: true" not in text:
            fail(f"skill must disable nested model invocation: {skill_path.relative_to(ROOT)}")
    return skills


def validate_evals(agents: set[str]) -> None:
    evals = load_json(".github/ai-sdlc/evals.json")
    required_categories = set(evals["required_categories"])
    minimum = int(evals["minimum_cases_per_agent"])
    by_agent: dict[str, list[dict]] = defaultdict(list)
    ids: set[str] = set()
    for case in evals["cases"]:
        if case["id"] in ids:
            fail(f"duplicate eval id: {case['id']}")
        ids.add(case["id"])
        if case["agent"] not in agents:
            fail(f"eval references unknown agent: {case['id']} -> {case['agent']}")
        if not case.get("must") or not case.get("must_not"):
            fail(f"eval case must define must and must_not: {case['id']}")
        by_agent[case["agent"]].append(case)

    for agent in sorted(agents):
        cases = by_agent[agent]
        categories = {case["category"] for case in cases}
        if len(cases) < minimum:
            fail(f"not enough eval cases for {agent}: {len(cases)} < {minimum}")
        if not required_categories.issubset(categories):
            fail(f"missing eval categories for {agent}: required={sorted(required_categories)} actual={sorted(categories)}")


def validate_controls() -> None:
    matrix = load_json(".github/ai-sdlc/control-matrix.json")
    ids: set[str] = set()
    for control in matrix["controls"]:
        if control["id"] in ids:
            fail(f"duplicate control id: {control['id']}")
        ids.add(control["id"])
        if control["status"] != "implemented":
            fail(f"control is not implemented: {control['id']} status={control['status']}")
        if not control.get("standards"):
            fail(f"control missing standards: {control['id']}")
        for evidence in control.get("evidence", []):
            if not (ROOT / evidence).exists():
                fail(f"missing evidence for {control['id']}: {evidence}")


def validate_codeowners() -> None:
    text = read(".github/CODEOWNERS")
    for path in REQUIRED_CODEOWNERS:
        if path not in text:
            fail(f"CODEOWNERS missing protected path: {path}")


def main() -> None:
    agents = validate_inventory()
    validate_evals(agents)
    validate_controls()
    validate_codeowners()
    print(f"AI SDLC validation passed for {len(agents)} agents.")


if __name__ == "__main__":
    main()
