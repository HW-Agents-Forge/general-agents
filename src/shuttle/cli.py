"""Command line interface. The only module that prints and exits."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn

from .config import CONFIG_FILE, Config, check_agents, load_config, parse_overrides, resolve_model
from .errors import ShuttleError, UsageError
from .installer import Action, Outcome, PlannedFile, install, plan
from .model import Catalog
from .registry import discover
from .targets import TARGETS, get_target
from .targets.base import reference_path, render_reference


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise UsageError(message)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="install", description="Install agents and skills for one tool.")
    parser.add_argument(
        "--target", required=True, help=f"tool to install for: {', '.join(TARGETS)}"
    )
    parser.add_argument(
        "--model",
        action="append",
        default=[],
        metavar="AGENT=MODEL",
        help="model of one agent for this run (repeatable)",
    )
    parser.add_argument("--dry-run", action="store_true", help="show what would be written")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--home", type=Path, default=None, help="substitute home directory")
    return parser


def _build_files(
    catalog: Catalog, config: Config, target_name: str, overrides: dict[str, str]
) -> list[PlannedFile]:
    target = get_target(target_name)
    files = [
        PlannedFile(
            target.agent_path(agent),
            target.render_agent(
                agent,
                resolve_model(config, target_name, agent.name, agent.tier, overrides),
                config.name,
            ),
        )
        for agent in catalog.agents
    ]
    for skill in catalog.skills:
        files.append(PlannedFile(target.skill_path(skill), target.render_skill(skill, config.name)))
        files += [
            PlannedFile(
                reference_path(target, skill, reference),
                render_reference(reference, config.name),
            )
            for reference in skill.references
        ]
    return files


def _confirm(outcomes: list[Outcome], assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        raise UsageError("not an interactive terminal: pass --yes to write without confirmation")
    count = sum(o.action in (Action.CREATE, Action.UPDATE) for o in outcomes)
    return input(f"Write {count} file(s)? [y/N] ").strip().lower() in ("y", "yes")


def _report(outcomes: list[Outcome], dry_run: bool) -> None:
    for outcome in outcomes:
        verb = f"would be {outcome.action.value}" if dry_run else outcome.action.value
        reason = f" ({outcome.reason})" if outcome.reason else ""
        print(f"{verb}: {outcome.path}{reason}")
    counts = {action: sum(o.action is action for o in outcomes) for action in Action}
    print(", ".join(f"{counts[action]} {action.value}" for action in Action))


def run(argv: Sequence[str] | None, root: Path) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(root / CONFIG_FILE, TARGETS)
    catalog = discover(root)
    check_agents(config, catalog.agent_names())
    overrides = parse_overrides(args.model, catalog.agent_names())
    files = _build_files(catalog, config, args.target, overrides)
    home = (args.home if args.home is not None else Path.home()).expanduser()

    if not args.dry_run:
        preview = plan(home, files, config.name)
        if any(o.action in (Action.CREATE, Action.UPDATE) for o in preview):
            _report(preview, dry_run=True)
            if not _confirm(preview, args.yes):
                print("Aborted.")
                return 0
    outcomes = install(home, files, config.name, dry_run=args.dry_run)
    _report(outcomes, args.dry_run)
    return 1 if any(o.action is Action.REFUSED for o in outcomes) else 0


def main(argv: Sequence[str] | None = None, root: Path | None = None) -> int:
    """Run the CLI; `root` is the repository holding agents/, skills/ and models.toml."""
    try:
        return run(argv, root if root is not None else Path.cwd())
    except ShuttleError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code


def entry_point() -> int:
    """Console script entry point (`shuttle`): the repository is the working directory."""
    return main()
