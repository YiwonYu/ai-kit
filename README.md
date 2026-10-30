# AI Kit

AI 연구·알고리즘·개발 과제를 위한 최소 작업 키트. Python 3.10 이상.

## 빠른 시작

```bash
git clone https://github.com/YiwonYu/ai-kit.git
cd ai-kit
python -m unittest discover -s tests -v
codex
```

```text
$solve
원문: [여기에 입력]
전체 시간: [분], 실행 환경: [CPU/GPU/메모리]
허용 도구와 제출 조건: [안내문]
원문을 읽고 PLAN.md를 채운 뒤 baseline부터 실행해라.
```

AGENTS.md는 이 프로젝트의 공통 지침이다. Skill은 `.agents/skills/solve/SKILL.md`에 있으며 `/skills`에서 확인할 수 있다. 실제 실행·수정은 사용자의 요청으로 시작한다. 자동 타이머·예약·백그라운드 에이전트는 없다.

## 별도 ai-kit 폴더 없이 받기

현재 디렉터리가 비어 있을 때 다음 명령을 사용한다. 숨김 파일도 없어야 하며 Git 저장소가 초기화되어 있어도 사용할 수 없다.

```bash
git clone https://github.com/YiwonYu/ai-kit.git .
codex
```

현재 폴더에 파일이 있으면 이 명령은 실패한다. 기존 파일을 삭제하지 말고 별도 위치에 clone한 뒤 필요한 파일만 병합한다. 기존 AGENTS.md와 .agents 설정을 덮어쓰지 않는다.

## 기존 과제 저장소에서 사용

기존 과제 저장소는 별도로 유지한다. 이 키트를 참고 자료로 지정하고 Codex에 필요한 지침·스크립트만 적용하도록 요청한다. 기존 AGENTS.md, 실행 코드, Git 이력을 덮어쓰지 않는다. 공개 저장소는 GitHub 인증 없이 clone할 수 있다. 시험 환경의 네트워크와 반입 규정을 먼저 확인한다.

## 실험 실행

저장소 루트에서 실행한다. `--` 뒤는 shell 문자열이 아니라 명령 인자이다. 종료 코드: 성공 0, 자식 실패 1, 실행 실패 2, 시간 초과 124, 중단 130. 실제 자식 종료 코드는 metadata.json에 보존한다.

```bash
python scripts/run_experiment.py --name baseline --timeout 30 --seed 42 -- python examples/demo.py --mode success
python scripts/run_experiment.py --name fail --timeout 30 -- python examples/demo.py --mode fail
python scripts/run_experiment.py --name timeout --timeout 0.2 -- python examples/demo.py --mode wait
```

매 실행은 `runs/고유ID/`를 만들고 `metadata.json`, `stdout.log`, `stderr.log`를 보존한다. 실패·시간 초과도 다른 실행 결과를 덮어쓰지 않는다. 실행 전 command, cwd, UTC 시작 시간, Git commit·dirty 여부를 기록한다. 끝나면 종료 상태·시간·실제 return code를 기록한다. Git 변경 내용 자체는 보존하지 않으므로 재현하려면 코드도 별도로 commit해야 한다.

`--seed`는 메타데이터와 `HARNESS_SEED` 환경 변수에 전달된다. 학습 코드에서 random/NumPy/PyTorch seed를 직접 설정해야 한다. 외부 API의 결정성은 보장하지 않는다. 예제는 Python random에 이를 적용한다. timeout은 실행 명령 단위 제한이며 전체 시험 시간은 직접 관리해야 한다. POSIX에서는 일반적인 자식 프로세스 그룹도 종료하지만 별도 세션으로 이탈한 프로세스까지 보장하지 않는다. Windows에서는 직접 자식만 종료한다.

명령 인자·stdout·stderr는 그대로 저장된다. 비밀은 명령 인자로 넘기거나 출력하지 않는다. 이 도구는 sandbox, 보안 검사기, 정답 평가기 또는 민감정보 제거기가 아니다.

## 파일 구성과 작업 순서

- AGENTS.md: 공통 규칙
- .agents/skills/solve/SKILL.md: 문제 풀이 절차
- templates/: PLAN, EXPERIMENTS, HANDOFF, SUBMISSION 빈 양식
- scripts/run_experiment.py: 실행·로그·시간 제한
- examples/demo.py: 정상·실패·시간 초과 예제
- tests/: 실행 도구의 회귀 검사

문제 확인 → PLAN 작성 → baseline → 실제 평가 → 가설별 개선 → 전체 흐름 확인 → HANDOFF·제출 점검 순서로 진행한다. 양식은 루트의 같은 이름 파일로 복사해 채우되 templates 원본은 유지한다.

## 문제 유형별로 현장에서 추가할 검사

| 유형 | 확인할 항목 |
|---|---|
| 모델 학습 | 고정 학습 조건, 데이터 누수, 파라미터 수, 실제 추론 metric |
| 규칙 복원 | 알려진 합성 규칙 복원, 별도 검증 시퀀스, 출력 길이 |
| 수치 예측 | 시계열 분할, baseline 비교, 합계 등 명세상 불변조건 |
| 영상 에이전트 | 숫자 순 파일 매핑, 선택지 유효성, 처리 시간, 재시도·결과 보존 |

문제에 따라 metric과 제약을 결정한다. 미리 특정 모델·학습률·선택지 수를 강제하지 않는다. 손풀이 또는 AI 금지 시험에서는 이 키트를 사용하지 않는다.
