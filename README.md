# study-goal

학습 목표 → 구체적 산출물 → 완료까지 강제 추적하는 Claude Code 플러그인.

## 무엇을 하나

"트랜스포머 공부하고 싶어" 같은 모호한 목표나 "[GitHub URL]에 대해 공부하고
싶어" 같은 콘텐츠 기반 학습을 받아서:

1. (필요시) URL을 페치해 콘텐츠 분석
2. 적응형 개념 체크 질문으로 현재 수준 측정
3. 종료 조건을 4지선다로 결정 (시간/양/능력/외부검증)
4. 산출물 형태 4지선다 (프로젝트/노트/문제풀이/설명자료)
5. 산출물의 구체적 스펙을 4지선다로 결정
6. 모든 결정을 `artifact.md`에 기록 + 작업하는 동안 자동 로깅
7. 학습 끝나면 완료 평가 + 토픽 루브릭 다듬기

## 핵심 기능

- **두 모드**: 일반 토픽 / 링크 기반 (URL 자동 감지)
- **다중 목표 동시 진행**: `.active`로 컨텍스트 관리
- **샛길 질문 처리**: 호기심 죽이지 않으면서 깊이 제한
- **자동 루브릭 생성**: 처음 보는 토픽이면 lazy generation으로 즉석 작성
- **자동 작업 로깅**: hook이 산출물 변경 시 artifact.md 자동 갱신
- **불변 섹션 보호**: 목표/종료조건/요구사항은 의도적 수정 외엔 안 변경

## 디렉토리 구조

플러그인:
```
study-goal-plugin/
├── .claude-plugin/plugin.json
├── skills/study-goal/
│   ├── SKILL.md
│   └── templates/
│       ├── deliverables/        # 일반 토픽 산출물 가이드
│       ├── deliverables-link/   # 링크 모드 산출물 가이드
│       └── concept-check-rubrics/_generic.md  # 루브릭 메타 가이드
├── hooks/
│   ├── hooks.json
│   └── log_progress.py          # PostToolUse 훅 (Python)
├── commands/
│   ├── start.md                 # /study-goal:start (온보딩 + 대시보드)
│   ├── new.md                   # /study-goal:new
│   ├── link.md                  # /study-goal:link <url>
│   ├── resume.md                # /study-goal:resume [slug]
│   ├── pause.md                 # /study-goal:pause [slug] [사유]
│   ├── check.md                 # /study-goal:check
│   ├── list.md                  # /study-goal:list
│   └── sidebar.md               # /study-goal:sidebar
└── README.md
```

런타임 (사용자 홈):
```
~/study-log/
├── .active                      # 활성 목표 slug (한 줄당 1개)
├── .claude-study-goal/
│   └── rubrics/                 # lazy 생성된 루브릭 누적
├── <slug-1>/
│   ├── artifact.md              # 학습 일지
│   ├── deliverable/             # 실제 산출물
│   └── _source/                 # [옵션] 링크 모드 콘텐츠 스냅샷
└── ...
```

## 설치

### 의존성
- Claude Code (최신 버전)
- Python 3 (macOS/Linux 기본 포함, hook이 사용)

### 설치 절차

```bash
# 실행 권한
chmod +x hooks/log_progress.py
```

Claude Code에서:
```
/plugin marketplace add <플러그인 폴더 절대 경로 또는 GitHub URL>
/plugin install study-goal
```

설치 후 **Claude Code 재시작** (hook 로드를 위해 필수).

### 동작 확인
설치 후 첫 실행:
```
/study-goal:start
```
온보딩 화면 + 명령어 안내가 나오면 성공.

## 사용

### 처음 사용 / 현재 상태 보기
```
/study-goal:start
```
처음이면 온보딩, 그 후엔 활성/일시중지/완료 학습 대시보드.

### 새 학습 (일반 토픽)
```
RAG 시스템에 대해 공부하고 싶어
```
또는
```
/study-goal:new
```

### 새 학습 (링크 기반)
```
https://github.com/karpathy/nanoGPT 이거 공부하고 싶어
```
또는
```
/study-goal:link https://github.com/karpathy/nanoGPT
```

### 진행 점검
```
/study-goal:check
```
또는 자연스럽게 "아까 RAG 목표 다 한 것 같은데 봐줘".

### 일시중지 / 재개
```
/study-goal:pause                       # 활성 목표 일시중지
/study-goal:pause rag-systems "주말에"    # 특정 목표 + 사유
/study-goal:resume                      # 일시중지된 목표 중에서 선택
/study-goal:resume rag-systems          # 특정 목표 재개
```
자연어로도 OK: "RAG 잠깐 멈출게", "어제 하던 거 이어서", "다시 RAG로".

### 학습 목록
```
/study-goal:list
```

### 샛길 질문 (작업 중 호기심)
```
잠깐, vector DB의 인덱싱은 어떻게 동작해?
```
Claude가 자동 감지. 또는 명시적으로:
```
/study-goal:sidebar vector DB 인덱싱
```

## 워크플로 예시

```
사용자: 트랜스포머 공부하고 싶어
Claude: "트랜스포머 아키텍처를 직접 구현할 수 있을 정도로 이해하기" 맞나요?
사용자: 응
Claude: [Step 2] self-attention에서 Q, K, V는 각각 어떤 역할인가요?
사용자: 음... Q는 질문이고 K랑 V는 잘 모르겠어요
Claude: [내부 평가: partial] 알겠어요. 다음 질문...
       (3-5개 질문 후)
       추정 수준: 중급. 이 수준이면 프로젝트 형태가 적절할 것 같아요.

[Step 3] 종료 조건: ① 5시간 투자 ② 250줄 코드 ③ scratch로 transformer
         block 작성 가능 ④ 친구에게 self-attention 설명 통과
사용자: ③

[Step 4] 산출물 형태: ① 프로젝트(추천) ② 노트 ③ 문제풀이 ④ 설명자료
사용자: ①

[Step 5] 4가지 변형:
  1. Tiny: MultiHeadAttention 1개 클래스만 (3시간)
  2. Small: encoder-only 트랜스포머, 작은 입력 forward (1일)
  3. Medium: nano-GPT 셰익스피어 학습 재현 (2-3일)
  4. Stretch: 위 + attention 시각화 도구 (1주)
사용자: 2

[Step 6] artifact.md 생성: ~/study-log/transformer-architecture/artifact.md
        deliverable/ 디렉토리 준비 완료. 작업 시작할까요?
사용자: 응. encoder block부터 짜보자

(Claude가 deliverable/encoder.py 작성 → hook이 자동으로 artifact.md에 로그 추가)

(나중에)
사용자: 잠깐, position encoding은 왜 필요한 거였지?
Claude: [샛길 모드 진입] position encoding은... [3-5문장 답변]
        artifact.md 샛길 섹션에 기록함. 본 작업 돌아갈까요?
```

## Hook의 역할

이 플러그인의 hook(`log_progress.py`)은 **기계적 로깅만** 함:
- `~/study-log/<slug>/deliverable/` 안의 파일 수정 감지
- artifact.md의 "📝 작업 로그" 섹션에 자동 append

Hook은 "산출물이 충분한가?"를 판단하지 않음. 그건 LLM(Claude)이
`/study-goal:check` 실행 시 함.

## 주의사항

- Hook은 Python 3가 필요 (대부분 시스템에 기본 설치됨)
- Hook 변경 후엔 Claude Code 재시작 필요 (hot-reload 안 됨)
- `${CLAUDE_PLUGIN_ROOT}`는 플러그인 폴더 경로로 자동 치환됨
- artifact.md의 불변 섹션은 직접 편집 가능하지만 **변경 주석** 권장:
  `<!-- YYYY-MM-DD 수정: 이유 -->`

## 한계 / 알려진 이슈

- Multi-active 모드에서 컨텍스트 추론이 가끔 틀릴 수 있음 → 애매하면 묻는 규칙
- Lazy 생성된 루브릭의 첫 버전은 검증 안 됨 → 학습 후 다듬기 옵션 활용
- 큰 GitHub 레포 (>5000줄) 페치 시 부분만 분석 가능

## 라이선스

MIT
