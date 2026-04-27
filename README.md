# study-goal

학습 목표 → 구체적 산출물 → 완료까지 추적하는 Claude Code 플러그인.

## 무엇을 하나

"트랜스포머 공부하고 싶어" 같은 모호한 목표를 받아서:

1. 산출물 타입을 4가지 중에 고르게 함 (프로젝트 / 노트 / 문제풀이 / 설명자료)
2. 선택한 타입의 4가지 변형 중에 하나 고르게 함 (스코프별)
3. 체크가능한 완료 조건을 작성해 `~/study-log/<goal>/criteria.md`에 저장
4. 작업하는 동안 산출물 파일 변경을 자동 로깅
5. 나중에 "다 됐어?" 물으면 criteria 기준으로 평가

## 구조

```
study-goal/
├── .claude-plugin/
│   └── plugin.json          # 플러그인 메타데이터
├── skills/
│   └── study-goal/
│       ├── SKILL.md         # 메인 워크플로
│       └── templates/       # 산출물 타입별 변형 생성 가이드
│           ├── project.md
│           ├── notes.md
│           ├── problems.md
│           └── explain.md
├── hooks/
│   ├── hooks.json           # hook 등록 설정
│   ├── log_progress.sh      # 파일 수정 시 log.md 자동 갱신
│   └── session_summary.sh   # 세션 종료 시 한 줄 추가
├── commands/
│   ├── new.md               # /study-goal:new 명령어
│   └── check.md             # /study-goal:check 명령어
└── README.md
```

## 설치

### 의존성

- Claude Code (최신 버전)
- `jq` (hook이 사용. macOS: `brew install jq`)

### 로컬 설치 (개발/테스트용)

이 폴더 전체를 어딘가에 두고:

```bash
chmod +x hooks/*.sh
```

Claude Code에서:

```
/plugin marketplace add <이 폴더의 절대 경로>
/plugin install study-goal
```

또는 GitHub 레포로 푸시한 뒤:

```
/plugin marketplace add <github-username>/study-goal
/plugin install study-goal
```

설치 후 **Claude Code를 재시작**해야 hook이 로드됨.

### 동작 확인

```
/study-goal:new
```

명령이 보이면 설치 성공. 새 세션 안에서 "X 공부하고 싶어"라고
말해도 스킬이 자동 트리거되어야 함.

## 사용

**새 목표 시작**:
```
/study-goal:new
```
또는 그냥 자연스럽게 "RAG 공부하고 싶어".

**진행 점검**:
```
/study-goal:check
```
또는 "아까 그 RAG 목표 다 한 것 같은데 봐줘".

## Hook의 역할 분담

이 플러그인의 hook은 **기계적인 일만 함** — 파일 수정 로깅, 세션
종료 표시. "이 산출물이 충분한가?"는 LLM의 판단이 필요해서 SKILL.md
Mode 2에서 사용자가 요청할 때 처리함.

Hook은 매 도구 호출마다 실행되므로 비싼 작업은 넣지 않는 게 좋음.

## 주의사항

- Hook 변경 후엔 Claude Code 재시작 필요 (hot-reload 안 됨)
- `${CLAUDE_PLUGIN_ROOT}`는 플러그인 폴더 경로로 자동 치환됨
- `~/study-log/` 경로는 사용자 환경에 의존 (필요시 수정)

## 라이선스

MIT
