#!/bin/bash
# ~/study-log/<slug>/deliverable/ 안의 파일이 수정되면
# ~/study-log/<slug>/artifact.md의 끝에 로그 한 줄 append.
#
# 불변 섹션(목표/개념체크/종료조건/산출물요구사항)은 절대 건드리지 않음.
# artifact.md의 구조상 "작업 로그" 섹션이 항상 마지막이므로 단순 append가 안전.

INPUT=$(cat)

if ! command -v jq &> /dev/null; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

[[ -z "$FILE_PATH" ]] && exit 0

STUDY_DIR="${HOME}/study-log"
[[ "$FILE_PATH" != "$STUDY_DIR"/* ]] && exit 0

# deliverable/ 하위만 추적 (artifact.md 자체 수정은 무시)
case "$FILE_PATH" in
    "$STUDY_DIR"/*/deliverable/*) ;;
    *) exit 0 ;;
esac

GOAL_DIR=$(echo "$FILE_PATH" | sed -E "s|($STUDY_DIR/[^/]+).*|\1|")
ARTIFACT_FILE="$GOAL_DIR/artifact.md"

# artifact.md 없으면 아직 Step 6 안 끝난 상태 → 무시
[[ ! -f "$ARTIFACT_FILE" ]] && exit 0

# 작업 로그 섹션이 있는지 확인
if ! grep -q "^## 📝 작업 로그" "$ARTIFACT_FILE"; then
    exit 0
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
RELATIVE_PATH=${FILE_PATH#$GOAL_DIR/}
echo "- $TIMESTAMP — \`$TOOL_NAME\` on \`$RELATIVE_PATH\`" >> "$ARTIFACT_FILE"

exit 0
