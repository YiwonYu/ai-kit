# AI Kit

Codex CLI용 계획 승인·실험 비교·블록별 구현·자동 검증 키트이다. Python 3.10 이상과 표준 라이브러리만 사용한다.

## 시작

```bash
git clone https://github.com/YiwonYu/ai-kit.git
cd ai-kit
codex
```

```text
$solve
문제: [원문]
시간·환경·제출 조건: [내용]
문제를 설명하고 단계별 접근·구조·실험·하네스·검증 계획을 작성해라.
아직 구현·실행하지 말고 계획 검토를 기다려라.
```

검토 후 “방법 탐색 계획을 승인한다. baseline 구현·평가 블록만 진행해라”처럼 실행 범위를 지정한다. 각 블록 결과를 확인하고 다음 허락을 준다. 여러 블록을 승인하면 해당 범위까지 진행한다. 공통 지침은 AGENTS.md, Skill은 `.agents/skills/solve/SKILL.md`에 있다. 승인 흐름은 지침이며 실행 스크립트의 권한 잠금은 아니다.

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
