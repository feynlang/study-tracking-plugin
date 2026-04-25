#!/usr/bin/env python3
"""
PostToolUse hook for study-goal plugin.

~/study-log/<slug>/deliverable/ 안의 파일이 수정되면
~/study-log/<slug>/artifact.md의 "📝 작업 로그" 섹션 끝에 한 줄 append.

규칙:
- 불변 섹션(목표/콘텐츠/개념체크/종료조건/요구사항)은 절대 건드리지 않음
- artifact.md 자체 수정은 무시 (무한 루프 방지)
- .claude-study-goal/, .active 같은 메타 파일 무시
- _source/ 안 변경 무시
- "🔍 샛길 질문" 섹션이 있어도 작업 로그 섹션 끝에 정확히 삽입
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = data.get("tool_input") or {}
    tool_name = data.get("tool_name", "")
    file_path = tool_input.get("file_path") or tool_input.get("path")

    if not file_path:
        sys.exit(0)

    home = Path(os.path.expanduser("~"))
    study_dir = home / "study-log"
    file_path = Path(file_path)

    # study-log 안의 변경만 추적
    try:
        rel_to_study = file_path.relative_to(study_dir)
    except ValueError:
        sys.exit(0)

    # 메타 디렉토리/파일 무시
    parts = rel_to_study.parts
    if not parts:
        sys.exit(0)
    if parts[0] in (".claude-study-goal", ".active"):
        sys.exit(0)

    # deliverable/ 하위만 추적 (slug/deliverable/...)
    if len(parts) < 3 or parts[1] != "deliverable":
        sys.exit(0)

    slug = parts[0]
    goal_dir = study_dir / slug
    artifact_file = goal_dir / "artifact.md"

    if not artifact_file.exists():
        sys.exit(0)

    content = artifact_file.read_text(encoding="utf-8")

    if "## 📝 작업 로그" not in content:
        sys.exit(0)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    rel_path = file_path.relative_to(goal_dir)
    new_line = f"- {timestamp} — `{tool_name}` on `{rel_path}`"

    # "🔍 샛길 질문" 섹션이 있으면 그 직전에 삽입
    sidebar_marker = "## 🔍 샛길 질문"

    if sidebar_marker in content:
        lines = content.split("\n")
        out_lines = []
        inserted = False
        for i, line in enumerate(lines):
            if not inserted and line.startswith(sidebar_marker):
                # 직전 빈 줄이 있으면 그 위에, 없으면 바로 위에 삽입
                if out_lines and out_lines[-1] == "":
                    # 빈 줄 유지하면서 그 앞에 삽입
                    last_empty = out_lines.pop()
                    out_lines.append(new_line)
                    out_lines.append(last_empty)
                else:
                    out_lines.append(new_line)
                    out_lines.append("")
                inserted = True
            out_lines.append(line)
        new_content = "\n".join(out_lines)
    else:
        # 그냥 끝에 append
        if not content.endswith("\n"):
            content += "\n"
        new_content = content + new_line + "\n"

    artifact_file.write_text(new_content, encoding="utf-8")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # hook 실패가 사용자 작업을 막지 않도록 항상 0
        sys.exit(0)
