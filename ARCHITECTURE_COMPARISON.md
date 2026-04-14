# 아키텍처 비교: 초안 vs 개선안

## 핵심 차이점

### 1. 실행 모델

#### ❌ 초안 (일반적 에이전트 개념)
```
부모 세션 (메인 컨텍스트)
  ├─ Stage 1: Data Collector
  ├─ Stage 2: Content Generator  
  ├─ Stage 3: QA/Edit
  ├─ Stage 4: Translation
  └─ Stage 5: Analysis
```
- **문제점:**
  - 모든 작업이 한 세션에서 순차 실행
  - 부모의 대화 히스토리 계속 증가 (토큰 낭비)
  - 병렬화 불가능
  - 컨텍스트 오염 (각 작업이 이전 결과 "본다")

#### ✅ 개선안 (Claude Code 팀 에이전트)
```
Team Lead Session (Google Sheets 관리)
  │
  ├─ Researcher Teammate (독립 컨텍스트)
  ├─ Writer Teammate (독립 컨텍스트)
  ├─ Optimizer Teammate (독립 컨텍스트)
  └─ Reviewer Teammate (독립 컨텍스트)
```
- **장점:**
  - 각 팀원이 독립적 컨텍스트 (깔끔함)
  - 4개 작업 완전 병렬화 가능
  - 팀원 간 메시징으로 필요한 정보만 전달
  - 전문화된 도구 set으로 효율성 ↑

---

### 2. 컨텍스트 관리

| 항목 | 초안 | 개선안 |
|------|------|--------|
| **부모 컨텍스트** | 모든 작업 결과 누적 | Google Sheets 관리만 |
| **각 작업 컨텍스트** | 공유 (이전 결과 포함) | 완전 격리 |
| **토큰 효율성** | 낮음 (누적 증가) | 높음 (각 팀원 독립) |
| **디버깅** | 한 곳에서만 가능 | 각 팀원 세션 확인 |
| **재실행** | 모든 것 재실행 | 한 팀원만 재실행 |

---

### 3. 데이터 흐름

#### ❌ 초안
```
Google Sheets
  ↓
[JSON 생성]
  ↓
Data Collector (Stage 1)
  → Content Generator (Stage 2)
    → QA Agent (Stage 3)
      → Translation (Stage 4)
        → Analysis (Stage 5)
  ↓
Google Sheets [결과]
```

**문제:**
- 한 단계에서 실패하면 이후 모든 단계 영향
- 각 Stage가 이전 결과를 "알고" 있음
- 병렬화 불가능

#### ✅ 개선안
```
Google Sheets [입력]
  ↓
Team Lead
  ├─→ Researcher (병렬 실행)
  │    └─ research_brief.json
  │
  ├─→ Writer (리서치 완료 후)
  │    └─ draft_article.md
  │
  ├─→ Optimizer (초안 완료 후)
  │    └─ optimized_article.md
  │
  └─→ Reviewer (최적화 완료 후)
       └─ approval ✓ / revision
  ↓
Google Sheets [결과]
```

**장점:**
- 명확한 의존성 (sequential gates)
- 실패 격리 (한 팀원만 재작업)
- 필요한 정보만 다음 단계로 전달
- 기다리는 팀원이 다른 작업 수행 가능

---

### 4. 통신 방식

#### ❌ 초안: 단방향
```
부모 → 자식에게 프롬프트 전달
  ↓
자식이 결과 반환
  ↓
부모가 다음 단계로 전달
```

#### ✅ 개선안: 쌍방향 + 협업
```
Team Lead → Researcher: "Find keywords for {topic}"
Researcher → Team Lead: "Research done, results at /research/{keyword}.json"
Team Lead → Writer: "Write article based on /research/{keyword}.json"
Writer → Team Lead: "Article ready at /content/drafts/{keyword}.md"
Team Lead → Optimizer: "Optimize /content/drafts/{keyword}.md"
...
```

---

### 5. 성능 비교

#### 예시: 3개 키워드, 각 단계 시간

**초안 (순차 실행)**
```
Research KW1 (5분)
  → Write KW1 (10분)
    → Optimize KW1 (5분)
      → Review KW1 (3분)
        → Research KW2 (5분)
          → Write KW2 (10분)
            → ...

총 소요 시간: ~3시간 (KW1, 2, 3 순차)
```

**개선안 (병렬 + 순차 게이트)**
```
Research KW1, 2, 3 (5분) ← 동시 실행
  ↓ (모두 완료 후)
Write KW1, 2, 3 (10분) ← 동시 실행
  ↓
Optimize KW1, 2, 3 (5분) ← 동시 실행
  ↓
Review KW1, 2, 3 (3분) ← 동시 실행

총 소요 시간: ~23분 (병렬화 덕분)
```

**⏱️ 성능 향상: 8배 빠름!** (8.8x speedup)

---

### 6. 확장성

| 항목 | 초안 | 개선안 |
|------|------|--------|
| **10개 키워드** | ~10시간 | ~25분 |
| **50개 키워드** | ~50시간 | ~25분 |
| **추가 팀원 (번역, 다국어)** | 더 느려짐 | 확장 가능 |
| **품질 개선 (재검수)** | 전체 재실행 | 해당 팀원만 재실행 |

---

### 7. 사용자 경험

#### ❌ 초안
```
사용자: "세 개 키워드로 콘텐츠 생성해줘"
  ↓
Claude: "모든 단계 자동 실행 중... (기다리는 중)"
  ↓
90분 후: 결과 완료
```

#### ✅ 개선안
```
사용자: "세 개 키워드로 콘텐츠 생성해줘"
  ↓
Claude: "팀을 생성했습니다. 팀원들이 병렬로 작업 중입니다."
사용자: "Shift+Down"으로 각 팀원의 진행 상황 실시간 확인
  ↓
23분 후: 결과 완료
```

**추가 혜택:**
- 각 팀원의 진행상황 실시간 확인
- 막힌 팀원에게 즉시 지시 가능
- 팀원 간 협업 감시 가능

---

### 8. 복잡도 관리

#### ❌ 초안: 높은 복잡도
- 한 세션에서 모든 로직 관리
- 상태 추적 복잡함
- 에러 처리 어려움

#### ✅ 개선안: 낮은 복잡도
- 각 팀원이 자신의 역할만 수행
- 명확한 입출력
- 에러 격리 (한 팀원 실패 = 그 팀원만 수정)

---

## 선택 가이드

### 초안을 사용하는 경우:
- ✅ 간단한 작업 (1-2단계)
- ✅ 빠른 프로토타입 (개념 검증)
- ✅ 낮은 복잡도
- ❌ 미리캔버스 SEO 자동화에는 부적합

### 개선안(팀 에이전트)을 사용하는 경우:
- ✅ 복잡한 협업 워크플로우
- ✅ 병렬 작업이 필요한 경우
- ✅ 각 단계별 전문화 필요
- ✅ **미리캔버스 SEO 자동화에 최적** ⭐

---

## 기술 구현 비교

### 초안: 일반 에이전트 호출
```python
# Python 코드 예시
agent_result = Agent(
    subagent_type="general-purpose",
    prompt="Generate content for {keyword}"
)
# 모든 로직이 한 프롬프트에 들어감
```

### 개선안: Claude Code 팀 에이전트
```python
# Claude Code 명령어
/agent team create seo-generator
# 팀 리더 세션에서 관리

# 각 팀원 정의
.claude/agents/seo-researcher.md
.claude/agents/seo-writer.md
.claude/agents/seo-optimizer.md
.claude/agents/seo-reviewer.md

# 팀 실행 (자동 스케줄)
/schedule
# 매주 월요일 9시 자동 실행
```

---

## 마이그레이션 경로

### Phase 1: 프로토타입 (초안 + 수동)
```
사용자 → 구글 시트 수동 입력
      ↓
   Claude API 호출 (수동)
      ↓
   결과 수동 저장
```

### Phase 2: 부분 자동화 (초안 기반)
```
구글 시트 → Python 스크립트 → Claude API → 구글 시트
(자동이지만 순차, 느림)
```

### Phase 3: 완전 자동화 (팀 에이전트 + 스케줄)
```
클라우드 스케줄 (자동 실행)
  ↓
팀 에이전트 (병렬 실행)
  ↓
구글 시트 + GitHub (자동 저장)
```

---

## 결론

| 기준 | 초안 | 개선안 |
|------|------|--------|
| **실행 속도** | 느림 (순차) | 빠름 (병렬) |
| **코드 복잡도** | 높음 | 낮음 |
| **유지보수성** | 어려움 | 쉬움 |
| **확장성** | 제한적 | 무제한 |
| **실시간 모니터링** | 불가 | 가능 |
| **에러 복구** | 전체 재실행 | 부분 재실행 |
| **Claude Code 활용도** | 낮음 | 높음 |
| **비용 효율성** | 낮음 | 높음 |
| **다국어 확장** | 어려움 | 쉬움 |

**🎯 미리캔버스 SEO 자동화 프로젝트는 개선안(팀 에이전트)으로 구현하는 것이 최적입니다.**

---

## 다음 단계

1. **환경 설정** - `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 활성화
2. **Agent 정의 파일 작성** - `.claude/agents/` 디렉토리에 각 팀원 정의
3. **Team Lead 프롬프트 작성** - Google Sheets 통합 로직
4. **클라우드 스케줄 설정** - 매주 자동 실행
5. **테스트 실행** - 1개 키워드로 전체 파이프라인 검증
6. **피드백 반영** - 각 팀원 성능 최적화
7. **확장** - 다국어/추가 분석 팀원 추가
