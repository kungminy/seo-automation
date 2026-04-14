# SEO 자동 생성 시스템 구현 가이드

## 📋 전체 요약

Claude Code의 **팀 에이전트 기능**을 활용하여 미리캔버스의 SEO 블로그 콘텐츠를 자동 생성하는 시스템입니다.

**핵심:**
- 🔍 **Researcher**: 키워드 & 경쟁사 분석
- ✍️ **Writer**: SEO 최적화 기사 작성  
- ⚙️ **Optimizer**: 메타데이터 & 스키마 최적화
- ✅ **Reviewer**: 최종 품질 검증

---

## 🚀 빠른 시작 (5분)

### 1단계: 환경 설정

```bash
# Claude Code CLI 확인 (2.1.32+ 필요)
claude --version

# 환경변수 활성화
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.zshrc
source ~/.zshrc
```

### 2단계: 프로젝트 파일 확인

```
seo-automation/
├── .claude/
│   ├── CLAUDE.md ✓
│   └── agents/
│       ├── seo-researcher.md ✓
│       ├── seo-writer.md ✓
│       ├── seo-optimizer.md ✓
│       └── seo-reviewer.md ✓
├── IMPROVED_AGENT_ARCHITECTURE.md
├── ARCHITECTURE_COMPARISON.md
├── /content/ (생성될 폴더)
├── /research/ (생성될 폴더)
└── IMPLEMENTATION_GUIDE.md (이 파일)
```

### 3단계: Claude Code에서 팀 생성

```text
/agent team create seo-generator
```

또는 자연어로:

```text
Create an agent team to automate weekly SEO content generation with these roles:

1. Researcher Teammate - Find keywords, analyze competitors, identify trends
2. Writer Teammate - Write SEO-optimized articles
3. Optimizer Teammate - Add metadata, schema, structure optimization
4. Reviewer Teammate - Final quality assurance

All teammates should use Opus model for quality.
Start with test run on these 2 keywords:
1. "프레젠테이션 구성"
2. "파워포인트 슬라이드 만드는 법"
```

### 4단계: 테스트 실행

```text
Generate SEO content for the "프레젠테이션 구성" keyword this week.

Step 1: Researcher, analyze the keyword
Step 2: Writer, create article based on research
Step 3: Optimizer, add metadata and schema
Step 4: Reviewer, final quality check

Progress report after each step.
```

### 5단계: 결과 확인

생성된 파일들:
- `/research/presentation-structure.json` - 리서치 결과
- `/content/drafts/presentation-structure.md` - 초안
- `/content/optimized/presentation-structure.md` - 최적화 버전

---

## 📊 아키텍처 선택 이유

### 초안 vs 개선안 비교

| 항목 | 초안 | 개선안 ✅ |
|------|------|---------|
| **실행 방식** | 순차 | 병렬 |
| **속도** | 느림 (3시간) | 빠름 (25분) |
| **확장성** | 제한적 | 무제한 |
| **복잡도** | 높음 | 낮음 |
| **모니터링** | 불가 | 실시간 |

**8배 빠른 성능** 및 **무제한 확장성**으로 팀 에이전트 선택!

---

## 🔄 워크플로우 상세 설명

### 한 번의 실행 흐름

```
┌─ Team Lead (Main Session)
│  └─ Google Sheets에서 키워드 읽기
│
├─ Researcher (병렬 실행)
│  └─ 키워드 분석 → /research/{keyword}.json
│     └─ Message Lead: "Research done"
│
├─ Writer (리서치 완료 후)
│  └─ 기사 작성 → /content/drafts/{keyword}.md
│     └─ Message Lead: "Draft ready"
│
├─ Optimizer (초안 완료 후)
│  └─ 메타데이터 최적화 → /content/optimized/{keyword}.md
│     └─ Message Lead: "Optimization done"
│
├─ Reviewer (최적화 완료 후)
│  └─ 최종 검수 → APPROVED ✓
│     └─ Message Lead: "Review complete"
│
└─ Team Lead
   └─ Google Sheets에 결과 저장
      └─ GitHub PR 생성
```

**소요 시간:** ~25분/3개 키워드 (병렬화)

---

## 📋 각 팀원의 역할

### 1️⃣ Researcher Teammate

**입력:**
```json
{
  "keyword": "프레젠테이션 구성",
  "target_audience": "초보자, 직장인",
  "deadline": "1시간"
}
```

**출력:**
```json
{
  "keyword": "프레젠테이션 구성",
  "search_volume": "4400/month",
  "difficulty": "High",
  "user_intent": "Informational",
  "pain_points": ["구성이 막힘", "표현력 부족"],
  "top_competitors": [...],
  "content_recommendations": {...}
}
```

**메시지:**
```
"Research complete for keyword '프레젠테이션 구성'.
Search Volume: 4400/month
Difficulty: High
Research file: /research/presentation-structure.json
Ready for writer to begin."
```

---

### 2️⃣ Writer Teammate

**입력:**
```
Write article using research from: /research/presentation-structure.json

Requirements:
- 2,000+ words
- PREP framework (Conclusion → Reason → Example → Conclusion)
- 4-6 H2 sections
- 3-5 internal links
- MiriCanvas AI integration where relevant
- Target audience: Beginners
```

**출력:**
```markdown
# 프레젠테이션 구성의 기본과 요령! 초보자를 위한 총정리

## Table of Contents
1. 좋은 프레젠테이션이란?
2. 기본 구성: 서론·본론·결론
3. 상황별 프레임워크: PREP·SDS·DESC
...

[2,000+ words article]
```

**메시지:**
```
"Article draft complete for keyword '프레젠테이션 구성'.
- Word Count: 2,340 words
- Internal Links: 4
- Structure: 5 H2 sections, 12 H3 subsections

Draft saved to: /content/drafts/presentation-structure.md
Ready for optimizer."
```

---

### 3️⃣ Optimizer Teammate

**입력:**
```
Optimize article: /content/drafts/presentation-structure.md

Tasks:
- Title: 50-60 chars with primary keyword
- Meta description: 155-160 chars with CTA
- Heading hierarchy verification
- Schema markup (BlogPosting + FAQ)
- Internal link validation
- Image alt text
```

**출력:**
```markdown
---
title: "프레젠테이션 구성의 기본과 요령! 초보자를 위한 총정리"
description: "좋은 프레젠테이션 구성법을 배우세요. PREP법부터..."
slug: "/blog/presentation-structure-guide"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  ...schema markup...
}
</script>

[Optimized article content]
```

**메시지:**
```
"SEO optimization complete for keyword '프레젠테이션 구성'.
- Title: Optimized (58 chars)
- Meta: Optimized with CTA
- Schema: BlogPosting + FAQPage added
- Internal Links: 4 verified
- Readability: Flesch-Kincaid 65

Optimized article: /content/optimized/presentation-structure.md
Ready for review."
```

---

### 4️⃣ Reviewer Teammate

**입력:**
```
Final quality review for: /content/optimized/presentation-structure.md

Checklist:
- Grammar and spelling ✓
- Factual accuracy ✓
- Audience fit ✓
- Brand consistency ✓
- Technical compliance ✓

Decision: APPROVED / NEEDS REVISION / REJECTED
```

**출력:**
```
Status: APPROVED ✓

Strengths:
- Clear structure and flow
- Accurate information with proper citations
- Target audience (beginners) well served
- Proper SEO optimization
- Strong CTA to MiriCanvas AI

Minor notes:
- Consider adding one more example in Section 2
- (Optional improvement, not required)

This article is publication-ready!
```

**메시지:**
```
"Quality review complete for keyword '프레젠테이션 구성'.

Status: APPROVED ✓

Scores:
- Grammar: 5/5
- Accuracy: 5/5
- Audience Fit: 5/5
- Brand Consistency: 5/5
- Technical: 5/5

Ready for publication!"
```

---

## 🛠️ 실제 사용 시나리오

### 시나리오 1: 단일 키워드 처리

```text
User: "Generate content for '파워포인트 디자인 법칙'"

Team Lead: 
1. Create task for Researcher
2. Assign keyword with context

Researcher: (5분)
└─ Research complete

Writer: (10분)
└─ Article drafted

Optimizer: (5분)
└─ Metadata added

Reviewer: (3분)
└─ Approved

Total: 23분
```

### 시나리오 2: 배치 처리 (3개 키워드)

```text
User: "Generate this week's content: 프레젠테이션, 파워포인트, 슬라이드"

Team Lead:
└─ Create 3 research tasks

[병렬 실행]
Researcher ┬─ KW1 Research (5분)
          ├─ KW2 Research (5분)
          └─ KW3 Research (5분)

Writer ┬─ KW1 Draft (10분)
       ├─ KW2 Draft (10분)
       └─ KW3 Draft (10분)

Optimizer ┬─ KW1 Optimize (5분)
         ├─ KW2 Optimize (5분)
         └─ KW3 Optimize (5분)

Reviewer ┬─ KW1 Review (3분)
        ├─ KW2 Review (3분)
        └─ KW3 Review (3분)

Total: 23분 (대비 순차 69분 → 3배 빠름!)
```

### 시나리오 3: 주간 자동화 (스케줄)

```bash
# 매주 월요일 9시 자동 실행
/schedule

Prompt: "Generate this week's SEO content (3 articles)"
Cron: 0 9 * * 1 (매주 월요일 9시)
Network: Internet enabled
MCP: Google Sheets, GitHub
```

---

## 📝 Google Sheets 연동

### 입력 시트 (Sheet1) 구조

```
| 행 | A: 키워드 | B: 관련키워드 | C: 대상 상황 | D: 고민 | E: 검색자심리 | F: JTBD | G: USP | H: 상태 |
|----|----------|-------------|----------|--------|------------|--------|--------|---------|
| 1  | 헤더      | 헤더        | 헤더     | 헤더  | 헤더       | 헤더   | 헤더   | 헤더    |
| 2  | 프레젠테이션 구성 | ... | ... | ... | ... | ... | ... | 진행 중 |
| 3  | 파워포인트 슬라이드 | ... | ... | ... | ... | ... | ... | 대기 중 |
| 4  | ... | ... | ... | ... | ... | ... | ... | ... |
```

### 출력 시트 (Sheet2-5) 구조

**Sheet2: 한국어 초안**
```
| A: 키워드 | B: 제목 | C: 메타설명 | D: 링크 | E: 상태 | F: 생성날짜 |
|---------|--------|----------|-------|--------|---------|
| 프레젠테이션 구성 | ... | ... | /content/optimized/... | 완료 | 2026-04-13 |
```

**Sheet3: 영어 버전**
```
| A: Keyword | B: Title | C: Meta Desc | D: Link | E: Status |
(향후 번역 팀원 추가 시)
```

**Sheet4: 일본어 버전**
```
| A: キーワード | B: タイトル | C: メタ説明 | D: リンク | E: 状態 |
(향후 번역 팀원 추가 시)
```

**Sheet5: 분석 결과**
```
| A: 키워드 | B: 검색량 | C: 난이도 | D: 경쟁사1 | E: 경쟁사2 | F: 마진분석 |
|---------|---------|---------|---------|---------|----------|
| 프레젠테이션 구성 | 4400 | High | Epson | Globis | ... |
```

---

## ⚠️ 문제 해결

### 문제 1: 팀원이 응답하지 않음

```
1. Shift+Down으로 해당 팀원 세션 확인
2. 팀원에게 직접 메시지:
   "What are you working on? Do you need more information?"
3. 팀원이 여전히 안 움직이면 작업 재할당
```

### 문제 2: 품질 저하

```
원인 분석:
- 프롬프트가 불명확한가? → 더 구체적으로 작성
- 팀원이 부족한가? → Opus로 업그레이드
- 가이드 문서가 부족한가? → 참고 자료 제공

조치:
1. 해당 팀원에게 개선 요청
2. 필요시 다시 실행
```

### 문제 3: Google Sheets 연동 실패

```
확인:
- Google Sheets API 인증? `gcloud auth application-default login`
- Sheet ID 올바른가? (URL에서 확인)
- 팀 리더 권한 있나?

조치:
- API 재인증
- Sheet ID 다시 확인
- 권한 재설정
```

---

## 📈 성능 최적화 팁

### 1. 모델 선택

```
Researcher → Opus (복잡한 분석)
Writer → Opus (고품질 콘텐츠)
Optimizer → Sonnet (간단한 수정, 비용 절감)
Reviewer → Sonnet (체크리스트 검증, 빠름)

월간 토큰 추정:
- 4주 × 3기사/주 × 90K tokens = 1.08M tokens
- Opus 대비 30% 비용 절감 가능
```

### 2. 배치 크기 최적화

```
권장: 3-5개 키워드 동시 처리
최대: 10개 (그 이상은 조율 복잡도 ↑)

예시:
- 소규모: 주 2-3개 기사
- 중규모: 주 3-5개 기사 ← 권장
- 대규모: 주 5-10개 기사
```

### 3. 캐싱 활용

```
같은 주제의 기사 작성 시:
1. Researcher 출력 재사용 가능
2. Writer가 관련 기사들 참고 가능
3. Optimizer 템플릿 재사용

→ 전체 시간 20% 단축 가능
```

---

## 🎯 성공 지표

### Week 1: 기초 확립
- [ ] 팀 에이전트 생성 및 실행 가능
- [ ] 1개 키워드 전체 파이프라인 완료
- [ ] 각 팀원 역할 명확화
- [ ] 출력 파일 구조 검증

### Week 2-4: 프로세스 최적화
- [ ] 주 3개 기사 안정적 생성
- [ ] 각 팀원 성능 피드백 반영
- [ ] Google Sheets 연동 자동화
- [ ] 클라우드 스케줄 설정

### Month 2: 확장 및 고도화
- [ ] 주 5-10개 기사로 확대
- [ ] 다국어 팀원 추가 (영어, 일본어)
- [ ] 트렌드 분석 심화
- [ ] GitHub 자동 PR 생성

### Month 3+: 완전 자동화
- [ ] 클라우드 스케줄로 주간 자동 실행
- [ ] 인간 개입 최소화 (검수만)
- [ ] SEO 성과 추적 시스템 구축
- [ ] 다양한 콘텐츠 유형 자동화

---

## 📚 참고 자료

### 공식 문서
- [Claude Code 팀 에이전트](https://code.claude.com/docs/en/agent-teams)
- [서브에이전트](https://code.claude.com/docs/en/sub-agents)
- [클라우드 스케줄](https://code.claude.com/docs/en/web-scheduled-tasks)

### 프로젝트 파일
- `IMPROVED_AGENT_ARCHITECTURE.md` - 전체 아키텍처
- `ARCHITECTURE_COMPARISON.md` - 초안 vs 개선안 비교
- `.claude/CLAUDE.md` - 프로젝트 설정
- `.claude/agents/*.md` - 각 팀원 정의

---

## ✅ 체크리스트

### 초기 설정
- [ ] Claude Code CLI v2.1.32+ 설치
- [ ] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수 활성화
- [ ] 프로젝트 폴더 구조 생성
- [ ] `.claude/` 디렉토리의 모든 파일 준비
- [ ] Google Sheets API 인증
- [ ] GitHub 토큰 설정

### 첫 실행
- [ ] 팀 생성 명령어 실행
- [ ] 1개 키워드로 테스트
- [ ] 각 팀원의 출력 검증
- [ ] 최종 결과물 품질 확인

### 자동화
- [ ] Google Sheets 입출력 연동
- [ ] 클라우드 스케줄 설정 (`/schedule`)
- [ ] 주간 자동 실행 테스트
- [ ] 에러 처리 프로세스 정의

### 운영
- [ ] 주간 진행 상황 모니터링
- [ ] 팀원 성능 피드백
- [ ] 프롬프트 지속적 개선
- [ ] 콘텐츠 품질 추적

---

## 🚀 다음 단계

1. **이번 주**: 팀 에이전트 생성 + 테스트 실행 (1개 키워드)
2. **다음 주**: 배치 처리 (3개 키워드) + 최적화
3. **3주차**: 클라우드 스케줄 설정 + 자동화
4. **4주차**: 성과 분석 + 다국어 확장 계획

---

**마지막 업데이트**: 2026-04-13  
**상태**: 🟢 실행 준비 완료  
**다음 단계**: 팀 에이전트 생성
