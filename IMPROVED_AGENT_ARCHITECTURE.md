# 미리캔버스 SEO 페이지 자동 생성 시스템 (개선 ver.)
## Claude Code 팀 에이전트 기반 아키텍처

> ✅ Claude Code 공식 팀 에이전트 기능 기반  
> ✅ 독립적 컨텍스트를 가진 병렬 작업  
> ✅ 공유 작업 목록으로 자동 조율  
> ✅ 클라우드 스케줄 기반 주기적 실행

---

## 시스템 아키텍처

```
┌────────────────────────────────────────────────────────────────────┐
│               SEO PAGE AUTO GENERATOR (Cloud Scheduled)              │
│                  Weekly Execution (매주 월요일 9시)                  │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │    Team Lead (Main Session)│
        │  - Google Sheets API 관리   │
        │  - 팀원 조율 & 모니터링      │
        │  - 최종 결과 저장           │
        └─────────┬──────────────────┘
                  │
        ┌─────────┴──────────┬──────────────┬──────────────┐
        │                    │              │              │
        ▼                    ▼              ▼              ▼
    ┌─────────┐        ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Researcher│       │  Writer  │   │Optimizer │   │ Reviewer │
    │Teammate  │       │ Teammate │   │ Teammate │   │ Teammate │
    │(독립     │       │(독립     │   │(독립     │   │(독립     │
    │컨텍스트) │       │컨텍스트) │   │컨텍스트) │   │컨텍스트) │
    └─────────┘       └──────────┘   └──────────┘   └──────────┘
        │                    │              │              │
        │                    │              │              │
    Keyword & Info  →  Draft Article  →  SEO Tags  →  Final Check
    Competitor        with Structure      & Links         & Approval
    Analysis
```

---

## 팀 에이전트 vs 초안 아키텍처의 주요 차이

| 항목 | 초안 (서브에이전트) | 개선안 (팀 에이전트) |
|------|------------------|-------------------|
| **각 Stage별 구조** | 부모 컨텍스트 내 순차 실행 | 독립적 팀원이 병렬 실행 |
| **컨텍스트** | 공유 (부모 대화 보임) | 완전히 격리됨 |
| **통신 방식** | 부모 → 자식 (단방향) | 팀원 간 직접 메시징 |
| **작업 관리** | 부모가 모두 관리 | 공유 작업 목록 (자동 조율) |
| **병렬성** | 제한적 | 완전 병렬 |
| **디버깅** | 부모 대화에서만 가능 | 각 팀원의 독립 세션 확인 |
| **적합한 프로젝트** | 단순, 빠른 작업 | 복잡, 협업 필요 |

**✅ 팀 에이전트 선택 이유:**
- SEO 콘텐츠는 다양한 작업이 병렬로 진행 가능 (분석, 작성, 검증)
- 각 팀원이 독립적으로 집중하면 품질 ↑
- 장시간 실행되므로 세션 유지 불필요 (클라우드 스케줄)
- 팀원 간 협업으로 자동 조율 효율성 높음

---

## 상세 아키텍처

### 1️⃣ **Team Lead (Main Session)**

**책임:**
- Google Sheets API로 입력 데이터 읽기
- 팀원 작업 할당
- 팀원 간 메시지 중계
- 최종 결과 Google Sheets에 저장
- GitHub PR 생성

**사용 도구:**
- `Read` - Sheets 데이터 읽기
- `Write` - Sheets 결과 저장
- `Bash` - Git/API 명령

**구성 파일:** `.claude/team-lead.md`

```markdown
# Team Lead - SEO Content Generator Leader
---
role: team_lead
model: opus
---

You are the team leader for SEO content generation. Your responsibilities:

1. **Morning Routine:**
   - Read keyword list from Google Sheet (Sheet1 range A2:B20)
   - Create a task list with 3-5 keywords to process this week
   - Assign tasks to team members

2. **Coordination:**
   - Monitor team's progress on task list
   - Route researcher output to writer
   - Route draft articles to optimizer
   - Route optimized content to reviewer

3. **Quality Gates:**
   - Ensure all articles pass reviewer approval
   - Check for consistency across versions
   - Verify link structure and metadata

4. **Output Management:**
   - Save approved articles to /content/articles/
   - Update Google Sheet with results
   - Create git branch and PR for review

5. **Problem Solving:**
   - If teammate is stuck, investigate and provide guidance
   - Escalate blockers to human review if needed
```

---

### 2️⃣ **Researcher Teammate**

**책임:**
- 키워드 연구 및 검색량 분석
- 경쟁사 분석 (상위 10개 페이지)
- 지역별 트렌드 분석
- 관련 검색어 수집
- 리서치 브리프 작성

**독립적 컨텍스트 활용:**
- 웹 검색, Grep, Glob 등에만 집중
- 부모의 대화 히스토리 없음 → 효율적
- 한 번에 리서치 완료 후 리더에게 보고

**구성 파일:** `.claude/agents/seo-researcher.md`

```markdown
# SEO Researcher Agent
---
subagent_type: seo-researcher
description: Research keywords, competitors, and trends for SEO content
tools:
  - Read
  - Glob
  - Grep
  - WebSearch
---

You are an expert SEO researcher. When assigned a keyword:

## Research Deliverables

### 1. Keyword Analysis
- Monthly search volume (estimate based on competitive difficulty)
- Search intent (informational, transactional, navigational)
- Related long-tail keywords (5-10 variations)
- Keyword clusters by user intent

### 2. Competitor Analysis
- Top 10 SERP pages for main keyword
- Title tags and meta descriptions
- Content length and structure
- Internal linking patterns
- Common keywords across top results

### 3. Market Trends
- Regional search trends (Korea, US, Japan)
- Seasonal patterns
- Trending topics in the category
- User pain points and questions

### 4. Research Brief
Output JSON format:
```json
{
  "keyword": "프레젠테이션 구성",
  "search_volume": 4400,
  "difficulty": "High",
  "user_intent": "Informational",
  "target_audience": "초보자, 직장인",
  "pain_points": ["구성이 막힘", "표현력 부족"],
  "related_keywords": [
    "프레젠 자료 구성",
    "파워포 슬라이드 구성"
  ],
  "top_competitors": [
    {
      "url": "...",
      "title": "...",
      "description": "..."
    }
  ],
  "content_outline": [
    "기본 개념",
    "PREP/SDS/DESC 프레임워크",
    "실제 예시"
  ]
}
```

## 메시지 포맷
작업 완료 후 팀 리더에게 보고:
"Research complete for keyword '{keyword}'. Research brief saved to /research/{keyword}.json"
```

---

### 3️⃣ **Writer Teammate**

**책임:**
- Researcher의 분석 자료 받기
- SEO 최적화된 제목 및 설명 작성
- 2,000+ 단어의 상세 기사 작성
- 논리적 흐름 구조화 (서론-본론-결론)
- 내부 링크 제안

**독립적 컨텍스트 활용:**
- 리서치 브리프를 입력으로 받음
- 집중해서 초안 작성
- 자신의 세션에서만 작업 → 방해 없음

**구성 파일:** `.claude/agents/seo-writer.md`

```markdown
# SEO Content Writer Agent
---
subagent_type: seo-writer
description: Write SEO-optimized articles based on research
tools:
  - Read
  - Write
  - Edit
---

You are an expert SEO content writer. When given a research brief:

## Writing Standards

### 1. Title & Meta
- **Title Tag**: 50-60 chars, primary keyword first
- **Meta Description**: 155-160 chars, includes CTA
- **URL Slug**: lowercase, hyphens, keyword-rich

### 2. Article Structure
- **H1**: Single, keyword-rich title
- **Intro**: Hook + value proposition (150-200 chars)
- **H2 Sections**: 4-6 main topics
  - **H3 Subsections**: 2-3 depth levels
- **Conclusion**: Summary + CTA
- **Internal Links**: 3-5 relevant links

### 3. Content Quality
- Target audience first
- Use "you" and conversational tone
- Break long paragraphs (max 3-4 sentences)
- Include examples and case studies
- 1 slide/visual per 300-400 words

### 4. SEO Optimization
- Primary keyword in H1, first 100 words, conclusion
- Related keywords naturally throughout
- External expert sources cited
- Link anchor text descriptive
- Lists and tables for scannable content

## Deliverables
```
/content/drafts/{keyword}.md

# Title (optimized for SEO)
Meta: description here

## Table of Contents
## Section 1
### Subsection 1.1
...
## Section N
...
## Conclusion

Internal Links:
- [Link text](url) - reason for link
```

## 메시지 포맷
"Draft article for '{keyword}' complete. File: /content/drafts/{keyword}.md"
```

---

### 4️⃣ **Optimizer Teammate**

**책임:**
- Writer의 초안 받기
- 메타 데이터 최적화 (제목, 설명)
- 구조화된 데이터 추가 (Schema.org JSON-LD)
- 이미지 alt 텍스트 작성
- 내부 링크 검증 및 개선

**독립적 컨텍스트 활용:**
- 초안 파일만 읽으면 됨
- 기술적 최적화에 집중
- 빠른 처리 (10-15분)

**구성 파일:** `.claude/agents/seo-optimizer.md`

```markdown
# SEO Optimizer Agent
---
subagent_type: seo-optimizer
description: Optimize article metadata, structure, and links
tools:
  - Read
  - Edit
---

You are an SEO technical expert. When optimizing an article:

## Optimization Checklist

### 1. Title & Description
- [ ] Title: 50-60 chars, primary keyword
- [ ] Description: 155-160 chars, includes benefit + CTA
- [ ] No duplicate titles in site
- [ ] No special characters breaking display

### 2. URL Optimization
- [ ] Slug: lowercase, hyphens, 3-5 words
- [ ] Keyword in URL path
- [ ] No numbers or dates (evergreen content)

### 3. Heading Structure
- [ ] Only 1 H1 on page
- [ ] H2 follows H1 (no H3 before H2)
- [ ] Headings include variations of target keywords
- [ ] Logical hierarchy maintained

### 4. Schema Markup
Add JSON-LD for:
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "...",
  "description": "...",
  "datePublished": "2026-04-13",
  "dateModified": "2026-04-13",
  "author": {
    "@type": "Organization",
    "name": "MiriCanvas"
  },
  "mainEntity": {
    "@type": "FAQPage",
    "mainEntity": [...]
  }
}
```

### 5. Image Optimization
- [ ] All images have descriptive alt text
- [ ] Alt text includes keyword when natural
- [ ] Image titles match alt text
- [ ] Compressed for web performance

### 6. Internal Links
- [ ] 3-5 internal links minimum
- [ ] Anchor text is descriptive (not "click here")
- [ ] Links point to relevant pages
- [ ] No broken links

### 7. Performance Checks
- [ ] No keyword stuffing (keyword density < 2%)
- [ ] Readability score high (Flesch 60+)
- [ ] Scannable format (short paragraphs, lists)

## 메시지 포맷
"Optimization complete for '{keyword}'. Metadata and schema added."
```

---

### 5️⃣ **Reviewer Teammate**

**책임:**
- Optimizer의 최종 버전 검수
- 문법 및 맞춤법 확인
- 논리적 일관성 검증
- 브랜드 톤&매너 확인
- 최종 승인 또는 피드백

**독립적 컨텍스트 활용:**
- 최종 확인만 담당
- Yes/No 결정 역할
- 빠른 반응 (5-10분)

**구성 파일:** `.claude/agents/seo-reviewer.md`

```markdown
# Quality Reviewer Agent
---
subagent_type: seo-reviewer
description: Review and approve final content before publication
tools:
  - Read
---

You are the final quality gate. When reviewing an article:

## Final Review Checklist

### 1. Grammar & Style
- [ ] No spelling errors
- [ ] Consistent verb tense (present tense)
- [ ] Proper punctuation
- [ ] No jargon without explanation

### 2. Factual Accuracy
- [ ] Statistics and data are cited
- [ ] Claims are substantiated
- [ ] Expert quotes are accurate
- [ ] No outdated information

### 3. Audience Fit
- [ ] Language matches target audience
- [ ] Solves the user's problem
- [ ] Actionable takeaways included
- [ ] CTA is clear and compelling

### 4. Brand Consistency
- [ ] Tone matches MiriCanvas brand
- [ ] Product benefits clearly stated
- [ ] No competitor favoritism
- [ ] Consistent terminology

### 5. Structure & Flow
- [ ] Logical progression (beginning → middle → end)
- [ ] Transitions between sections smooth
- [ ] Conclusion ties back to intro
- [ ] No tangential sections

### 6. Technical Compliance
- [ ] No broken links
- [ ] Proper heading hierarchy
- [ ] Metadata complete
- [ ] Images properly formatted

## 승인 기준
"APPROVED" 또는 "NEEDS REVISION: [specific feedback]"

## 메시지 포맷
"Review complete for '{keyword}'. Status: APPROVED ✓"
또는
"Review complete for '{keyword}'. Revision needed: [feedback]"
```

---

## 팀 구성 및 실행

### Team Creation Prompt

```
Create an agent team to automate weekly SEO content generation with these roles:

1. **Researcher Teammate** - Research keywords, analyze competitors, identify trends
2. **Writer Teammate** - Write engaging, SEO-optimized articles
3. **Optimizer Teammate** - Add metadata, schema, optimize structure
4. **Reviewer Teammate** - Final quality assurance and approval

Team Configuration:
- Model: Claude Opus for quality
- Execution: Parallel with sequential gates
- Communication: Shared task list
- Output: Google Sheets integration via Team Lead
```

### 팀 작업 흐름

```
Team Lead (Main Session)
│
├─ Task: "Research: 프레젠테이션 구성"
│  └─ Assign to Researcher
│     └─ Output: research_brief.json
│        └─ Message Lead: "Research done"
│           └─ Lead assigns to Writer
│
├─ Task: "Write: 프레젠테이션 구성"
│  └─ Assign to Writer
│     └─ Output: draft_article.md
│        └─ Message Lead: "Draft ready"
│           └─ Lead assigns to Optimizer
│
├─ Task: "Optimize: 프레젠테이션 구성"
│  └─ Assign to Optimizer
│     └─ Output: optimized_article.md
│        └─ Message Lead: "Optimization done"
│           └─ Lead assigns to Reviewer
│
├─ Task: "Review: 프레젠테이션 구성"
│  └─ Assign to Reviewer
│     └─ APPROVED or NEEDS REVISION
│        └─ Message Lead: "Review complete"
│           └─ Lead saves to Sheets & creates PR
```

---

## 스케줄링 전략

### 클라우드 스케줄 설정

```bash
# 매주 월요일 오전 9시 자동 실행
/schedule
# Prompt: "Generate SEO content for top 3 keywords this week"
# Cron: 0 9 * * 1  (매주 월요일 9시)
# Network: Internet access enabled
# MCP: Google Sheets, GitHub
```

### 대안: /loop 실시간 모니터링 (Team Lead 세션)

```bash
# 팀 진행 상황 매 30분마다 확인
/loop 30m Check the SEO team's article generation progress and report

# 또는 커스텀 loop.md
# .claude/loop.md
Coordinate the SEO content team:
1. Check task list for pending work
2. Report stuck teammates
3. Monitor quality of completed work
4. If all articles approved, create PR
```

---

## 데이터 흐름 다이어그램

```
┌──────────────────────────────────────────────────────────────┐
│                    GOOGLE SHEETS (입력)                        │
│  Column A: Keyword | B: CEP | C: Pain Point | D: USP | ...   │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │    Team Lead (Main Session)   │
        │  1. Read Google Sheet         │
        │  2. Create task list          │
        │  3. Assign to teammates       │
        │  4. Monitor & coordinate      │
        │  5. Save results to Sheets    │
        └──────────────┬────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
    ┌─────────┐  ┌────────┐  ┌──────────┐  ┌────────┐
    │Researcher│  │ Writer │  │Optimizer │  │Reviewer│
    └────┬────┘  └───┬────┘  └────┬─────┘  └───┬────┘
         │           │            │            │
         │           │            │            │
    research      draft       optimized    approved
    _brief.json   _article    _article    _article.md
         │           │            │            │
         └───────────┴────────────┴────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │  GOOGLE SHEETS (출력 탭들)    │
        │  - 한국어 초안               │
        │  - 영어 버전 (번역 추가)     │
        │  - 일본어 버전 (번역 추가)   │
        │  - 메타데이터               │
        │  - 경쟁사 분석               │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │      GITHUB (최종)            │
        │  1. Create branch            │
        │  2. Push articles            │
        │  3. Create PR for review     │
        └──────────────────────────────┘
```

---

## 팀 에이전트 제어 명령어

### 팀 생성 및 시작

```text
Create an agent team for weekly SEO content generation:
- Research Teammate: Find keywords, analyze competitors
- Writer Teammate: Write SEO-optimized articles
- Optimizer Teammate: Add metadata and structure
- Reviewer Teammate: Final quality check

Start with these 3 keywords:
1. 프레젠테이션 구성
2. 프레젠 슬라이드 만드는 법
3. 파워포인트 레이아웃 디자인
```

### 팀 진행 상황 확인

```text
What are the current tasks and who's working on what?
Show me the progress on article generation.
```

### 팀원과 직접 소통

```text
Message the researcher: "Include search volume data in your analysis"
Tell the writer: "Expand the conclusion section with more actionable tips"
Ask the optimizer: "Double-check the schema markup for correctness"
```

### 팀 최적화 및 정리

```text
Show me which tasks are blocked
Help the optimizer with technical SEO optimization
Clean up the team when all articles are published
Create a final summary of completed work
```

---

## 다국어 확장 (향후)

### 현재 워크플로우: 한국어

```
Research (한국어)
  ↓
Write (한국어)
  ↓
Optimize (한국어)
  ↓
Review (한국어)
  ↓
저장 (Google Sheets)
```

### 향후 다국어 확장: 영어 + 일본어

```
Team Lead (한국어 완료)
  ├─ Message Translator Teammate (KO→EN)
  │  └─ Translate + Localize
  │     └─ Researcher-EN finds English keywords
  │        └─ Writer-EN adapts for English audience
  │           └─ Optimizer-EN applies English SEO
  │              └─ Reviewer-EN checks quality
  │
  └─ Message Translator Teammate (KO→JA)
     └─ Translate + Localize (일본어 경어 등)
        └─ (동일 프로세스)
```

---

## 비용 및 성능 추정

### 클라우드 스케줄 실행 비용

| 항목 | 소비 |
|------|------|
| **Team Lead** | 1 Opus 세션 |
| **Researcher** | 1 Opus 세션 |
| **Writer** | 1 Opus 세션 |
| **Optimizer** | 1 Opus 세션 |
| **Reviewer** | 1 Opus 세션 |
| **총 토큰** | ~80K-100K tokens (5개 기사 기준) |
| **월간 실행** | 4회 × ~90K tokens = 360K tokens |

**💡 최적화 팁:**
- 각 팀원이 독립 컨텍스트 → 불필요한 토큰 낭비 최소화
- 병렬 실행 → 실행 시간 단축
- Sonnet으로 다운그레이드 시 가능 (비용 50% 절감, 품질 유지)

### 예상 실행 시간

| 단계 | 시간 | 병렬화 |
|------|------|-------|
| Research (1개 키워드) | 5분 | 3개 동시 |
| Write (1개 기사) | 10분 | 3개 동시 |
| Optimize | 5분 | 3개 동시 |
| Review | 3분 | 3개 동시 |
| **순차 총 시간** | ~23분 | - |
| **병렬 총 시간** | ~23분 | ✅ (동시 진행) |

---

## 구현 체크리스트

- [ ] Google Sheets API 인증 설정
- [ ] `.claude/team-lead.md` 작성
- [ ] `.claude/agents/seo-researcher.md` 작성
- [ ] `.claude/agents/seo-writer.md` 작성
- [ ] `.claude/agents/seo-optimizer.md` 작성
- [ ] `.claude/agents/seo-reviewer.md` 작성
- [ ] 클라우드 스케줄 설정 (`/schedule`)
- [ ] 테스트 실행 (1개 키워드 기준)
- [ ] Google Sheets 템플릿 최종화
- [ ] 팀 에이전트 초대 및 권한 설정
- [ ] 첫 실행 모니터링

---

## 참고

**Claude Code 공식 문서:**
- 팀 에이전트: https://code.claude.com/docs/en/agent-teams
- 서브에이전트: https://code.claude.com/docs/en/sub-agents
- 클라우드 스케줄: https://code.claude.com/docs/en/web-scheduled-tasks
- Agent SDK: https://github.com/anthropics/anthropic-sdk-python

**필수 요구사항:**
- Claude Code CLI v2.1.32+
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수
