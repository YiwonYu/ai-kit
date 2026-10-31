# AI Kit

Codex CLI용 계획 승인·실험 비교·블록별 구현·자동 검증 키트이다. Python 3.10 이상과 표준 라이브러리만 사용한다.

## 시작 — 한 문장으로 초기 설정과 계획 작성

키트를 받은 후 문제 원문을 `Prob.md`에 저장하고 Codex에 다음 한 문장만 입력한다.

```text
README.md와 Prob.md를 읽고 진행해줘
```

가장 간단한 배치는 clone한 ai-kit 안에 Prob.md를 두고 그 폴더에서 Codex를 시작하는 것이다.

```bash
git clone https://github.com/YiwonYu/ai-kit.git
cd ai-kit
# 여기에 실제 문제를 담은 Prob.md를 저장한다.
codex
```

별도 문제 폴더에 ai-kit이 하위로 있다면 파일을 옮길 필요 없이 다음처럼 경로만 명시한다.

```text
ai-kit/README.md와 Prob.md를 읽고 진행해줘
```

별도의 `$solve` 호출이나 설치 지시를 반복할 필요는 없다. 이 README를 읽도록 요청받은 AI는 아래 절차로 solve 원본을 직접 읽고 적용한다. 이 문장은 초기 설정과 계획 작성에 대한 요청이며, 계획 검토 없이 모든 구현·실험을 실행하라는 승인은 아니다.

## AI 실행 지침 — README와 Prob를 읽으라는 요청을 받으면 수행

### 1. 문제·키트·작업 폴더 확인

- 사용자가 지정한 README와 Prob.md를 실제로 읽는다. Prob.md의 부모 폴더를 기본 문제 작업 폴더로 사용하되 사용자가 다른 대상을 명시하면 따른다.
- 키트 루트는 이 README와 함께 있는 AGENTS.md, `.agents/skills/solve/SKILL.md`, templates/, scripts/로 식별한다. README만 별도 복사한 경우 명시된 키트 경로 또는 현재 작업 폴더의 ai-kit/에서 원본을 확인한다. 원본이 없거나 여러 후보가 있으면 원본 위치를 확인하고 임의로 복제·추측하지 않는다.
- Prob.md가 없거나 문제·제출 조건이 불충분하면 가능한 부분을 정리하고 필요한 정보만 요청한다. 가짜 문제나 승인 내용을 만들지 않는다.
- 키트 AGENTS.md와 `.agents/skills/solve/SKILL.md`를 읽고 지금 세션의 작업에 명시적으로 적용한다. `$solve`의 자동 발견 여부에 의존하지 않는다.

### 2. 기본 하네스 연결 — 처음 한 번만

- 문제 폴더와 키트가 같으면 기존 루트 AGENTS와 solve를 그대로 사용한다.
- 별도 문제 폴더라면 루트 AGENTS.md에 실제 키트 AGENTS와 solve 원본의 상대 경로를 읽고 후속 요청에도 규칙을 유지하라는 연결 지침을 추가한다. 기존 지침을 보존하고 같은 연결을 중복 추가하지 않는다.
- 문제 폴더의 `.agents/skills/solve/SKILL.md`에 `name: solve`와 명확한 description을 가진 연결 Skill을 준비한다. 본문은 실제 키트 AGENTS와 solve 원본을 읽도록 한다. 기존 동명 Skill을 덮어쓰지 말고 충돌을 보고한다. 원본 Skill이 연결 Skill 자신을 가리키는 재귀 참조를 만들지 않는다.
- 키트 scripts/, templates/, .git는 이동하지 않는다. 도구·양식 경로는 키트 기준, 문서·결과·코드·Git 기록은 문제 폴더 기준으로 명확히 구분한다. 셸 cd만으로 기존 Codex 세션의 작업 루트가 영구 변경된다고 가정하지 않는다.
- PLAN.md, EXPERIMENTS.md, DECISIONS.md, HANDOFF.md, PROJECT_STRUCTURE.md 중 없는 검토용 문서를 양식에서 준비한다. 기존 파일은 읽고 현재 상태를 보존한다. 필요한 세부 계획 문서만 plans/에 만든다.
- 이 단계에서는 공통 지침·Skill 연결과 검토용 문서만 준비한다. 문제별 코드·verification.json 생성, 패키지 설치, 실험·테스트 실행, 원격 업로드는 하지 않는다.

### 3. 문제 분석과 계획 제시 후 멈춤

- Prob.md를 바탕으로 문제를 쉽게 설명하고 목표·제약·입출력·평가·제출 조건을 정리한다.
- baseline·대안·선택 근거, 사용할 모듈·데이터 흐름, 실험·예산, 추가할 최소 하네스와 정상·오류·경계·전체 흐름 검증을 제안한다.
- 방법 탐색·DB·web처럼 독립 단계가 필요하면 plans/로 나누고 전체 PLAN에는 연결과 선행 조건만 둔다. 비교표는 방법 설명표와 성능표 두 개로 유지한다. 약어만 있는 이름과 날짜별 누적 문서를 만들지 않는다.
- 이미 진행 중인 프로젝트면 PLAN·HANDOFF·비교표·결정과 실제 파일·Git을 대조해 이어갈 계획을 제안한다. 처음부터 초기화하지 않는다.
- 문제 폴더·키트 경로·준비한 문서·현재 계획·다음 승인 지점을 짧게 보고하고 멈춘다. 사용자 수정사항은 반영하되 명시적 승인 전 구현·실험을 시작하지 않는다.

### 4. 승인 이후와 후속 요청

- 사용자가 승인한 단계·블록 범위만 구현·실험·자동 검증한다. 각 블록의 작업·tests·실제 결과를 상세 파일에 남기고 두 비교표·결정·현재 요약을 갱신하며 로컬 Git 커밋을 남긴다.
- 블록 결과를 보고하고 다음 승인 범위가 없으면 기다린다. “새로운 method를 찾아줘” 같은 후속 요청에도 같은 계획·승인·기록 규칙을 적용한다.
- 다음 세션은 문제 폴더에서 시작하면 루트 지침·연결 Skill을 사용할 수 있다. 세션 내 새 Skill 표시를 보장하지 말고 현재 세션에서는 실제 원본을 읽어 적용한다.
- 승인 흐름은 AI 지침이며 실행 스크립트의 권한 잠금은 아니다.

## 읽기 쉬운 현재 상태

| 파일·경로 | 내용 | 갱신 방식 |
|---|---|---|
| PLAN.md | 문제 설명, 현재 목표·단계 연결·승인 | 약 60줄 이내, 현재 내용 갱신 |
| plans/<단계>.md | 방법 탐색·DB·web 세부 접근·구조·블록·tests | 단계별 현재 계획 |
| EXPERIMENTS.md | 방법 설명표 + 성능 비교표 | 두 표의 행 갱신·추가 |
| methods/<설명적인-방법>/ | METHOD.md, RESULTS.md, 설정 | 상세 원리·명령·실행 근거 |
| DECISIONS.md | 채택·보류·폐기 결정표 | 현재 상태 갱신 |
| decisions/<주제>.md | 선택 이유·대안·증거·Git 참조 | 과거 버전은 Git |
| HANDOFF.md | 현재 상태·막힌 점·다음 행동 | 약 25줄 이내 |
| PROJECT_STRUCTURE.md | 프로젝트 파일 역할·구조 계약 | 승인된 구조 변경만 반영 |
| verification.json | 요구사항과 자동 검사 연결 | 실제 프로젝트에 맞춤 |
| runs/ | 실행·검증 원본 로그 | 매 실행 보존, Git 제외 |

양식은 templates/에 있다. 실제 파일은 문제 작업 폴더에 만들며 원본 양식은 유지한다. 날짜별 추가 섹션이나 A1/N1 같은 약어만 있는 이름을 쓰지 않는다. 새 실험은 두 표를 갱신하고 상세 근거는 methods/에 둔다. 다른 데이터·분할·지표·예산의 결과를 같은 조건처럼 비교하지 않는다.

방법 탐색·DB·web은 독립 결과물·검증·승인 기준이 있으면 plans/로 나눈다. 전체 PLAN에는 연결과 선행 조건만 남긴다. 입출력 계약과 fixture를 먼저 합의하면 전체 구현 전에 일부 연결을 검증할 수 있다. 필요 없는 단계를 의무적으로 만들지 않는다.

기존에 누적된 문서가 있다면 승인 후 원본을 보존·이관하고 현재 문서에서 근거를 링크한다. 원본 실행 결과를 삭제하거나 기존 사용자 변경을 덮어쓰지 않는다.

## 자동 검증

키트 자체를 검증하려면 다음 한 명령을 사용한다.

```bash
python scripts/verify_pipeline.py --config verification.json
```

**루트 verification.json은 이 키트의 실행 도구만 검사한다. 실제 문제·DB·web 서비스가 검증된 것은 아니다.**

프로젝트에서는 승인 후 `templates/verification.json`을 참고해 요구사항과 실제 tests를 등록한다. 초안은 모든 검사가 pending이므로 실행하면 실패한다. 실제 검사로 채우기 전에는 통과하지 않는다. 기존 프로젝트 설정은 덮어쓰지 않는다.

- scope: 실제로 무엇을 검증하는지 설명
- requirements: 요구사항별 필수 check ID 연결. 없는 검사나 optional 검사로 연결하면 설정 오류
- required_categories: 누락해서는 안 되는 검사 종류
- checks: 사람이 읽는 이름, category, oracle(독립적 예상 결과·판정 근거), required, 실행 명령과 timeout
- category: structure / unit / integration / e2e / negative / boundary / other
- structure: paths의 상대 경로와 file/directory 종류 확인. 외부 경로·프로젝트 밖 symlink는 허용하지 않음
- command: shell 문자열이 아닌 인자 배열. `{python}`은 현재 Python 실행 파일로 치환
- expected_exit: 기본 0. 오류 처리 검사에서 의도한 비정상 종료를 확인할 때만 별도 지정
- pending: 미구현 검사. 필수 pending·실패·timeout·실행 오류는 전체 실패

예시 검사 한 항목(실제 tests가 구현되어 있어야 한다):

```json
{
  "id": "database-roundtrip",
  "name": "대표 입력의 DB 저장 후 조회 값 일치",
  "category": "integration",
  "required": true,
  "oracle": "독립적으로 정한 fixture의 필드·개수와 실제 저장·조회 결과를 비교한다.",
  "command": ["{python}", "-m", "unittest", "tests.test_database_roundtrip"],
  "timeout": 30
}
```

검증마다 `runs/verification/<고유ID>/`에 report.json, report.md, 설정 snapshot, 검사별 로그·metadata를 보존한다. JSON은 실행 당시 Git commit·dirty 상태와 요구사항 연결을 포함한다. 종료 코드: 통과 0, 필수 검사 실패·blocked 1, 설정 오류 2, 중단 130. optional 실패도 보고서에 나타나지만 전체 통과를 막지는 않는다. 구조 검사는 파일 존재·종류만 확인하며 의존성이나 기능은 tests로 검사한다.

GitHub Actions는 push·PR 시 Python 3.10/3.12에서 같은 파이프라인을 실행하고 보고서·로그를 14일간 artifact로 보존한다. 실제 프로젝트에서는 workflow도 해당 프로젝트의 검증 설정을 실행하도록 연결한다.

**테스트 통과는 선언한 조건의 근거이며 AI 코드의 무결함 보장이 아니다.** 사람이 요구사항·예상값·tests를 검토하고, 실제 전체 흐름·실패 복구·경계를 확인해야 한다. mock만 통과한 검사를 실제 외부 연동으로 표현하지 않는다. 프로덕션 DB나 실제 사용자 데이터에 파괴적인 테스트를 실행하지 않는다. 검증 설정은 명령을 실행하므로 읽고 신뢰할 수 있는 설정만 사용한다.

## 실험 실행 도구

```bash
python scripts/run_experiment.py --name baseline --timeout 30 --seed 42 -- python examples/demo.py --mode success
```

매 실행의 명령·cwd·seed·코드 버전·시간·종료·stdout/stderr를 별도 runs/ 폴더에 보존한다. 성공 0, 자식 실패 1, 실행 오류 2, 시간 초과 124, 중단 130을 반환하며 실제 자식 종료 코드는 metadata에 남긴다. --seed는 HARNESS_SEED로 전달하므로 학습 코드에서 random/NumPy/PyTorch seed를 적용해야 한다. POSIX는 일반적인 프로세스 그룹, Windows는 직접 자식을 종료하며 별도로 이탈한 프로세스는 보장하지 않는다.

실행 명령·로그는 원문 저장되므로 비밀을 넣거나 출력하지 않는다. 이 도구는 sandbox나 개인정보 제거기가 아니다. metadata의 commit만으로 dirty 변경을 복원할 수 없으므로 해당 코드도 블록 커밋으로 보존한다. 기본적으로 로그·데이터·가중치는 Git 제외이며 중요한 결과와 재현 조건은 문서에 기록한다.

## Git와 인계

승인 계획 → 블록별 코드·tests·결과표·결정·현재 요약을 의미 있는 로컬 커밋으로 남긴다. 필요한 경로만 stage하고 기존 사용자 변경은 섞지 않는다. 실행 코드 버전과 결과 기록 커밋을 구분한다. push는 별도 요청 때만 한다. PLAN/HANDOFF에 이력을 쌓지 않고 Git과 상세 파일을 참조한다.

## 기존 폴더에서 사용

빈 현재 폴더에는 다음처럼 받을 수 있다.

```bash
git clone https://github.com/YiwonYu/ai-kit.git .
```

파일이 있는 과제 폴더에서는 하위에 clone하고 Codex에 `ai-kit/AGENTS.md`와 `ai-kit/.agents/skills/solve/SKILL.md`를 읽으라고 명시해도 된다. 이 경우 하위 Skill이 자동 발견된다고 가정하지 않는다. 실행·양식 경로는 키트 위치를 기준으로 해석하고, 결과·계획·Git 기록은 실제 문제 프로젝트에서 관리한다. 기존 AGENTS.md나 .agents 설정을 덮어쓰지 않는다. 시험의 자료 반입·AI 허용 규칙이 우선이다.
