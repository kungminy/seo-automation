# 미리캔버스 SEO 페이지 자동 생성 시스템

## 프로젝트 개요

Claude Code 팀 에이전트를 활용한 SEO 콘텐츠 자동 생성 시스템입니다.

**구성:**
- Team Lead: Google Sheets 관리 및 팀원 조율
- Researcher Teammate: 키워드 리서치 및 경쟁사 분석
- Writer Teammate: SEO 최적화 기사 작성
- Optimizer Teammate: 메타데이터 및 구조 최적화
- Reviewer Teammate: 최종 품질 검수

---

## 팀 에이전트 활성화

### 1. 환경 변수 설정

```bash
# ~/.zshrc 또는 ~/.bash_profile에 추가
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 2. Claude Code CLI 버전 확인

```bash
claude --version
# 2.1.32 이상 필요
```

---

## 팀 생성 명령어

```
Create an agent team to automate weekly SEO content generation:

1. **Researcher Teammate** - Find keywords, analyze competitors, identify trends
   - Model: Opus
   - Tools: Read, Glob, Grep, WebSearch
   - Role: Keyword research and competitive analysis

2. **Writer Teammate** - Write SEO-optimized articles based on research
   - Model: Opus
   - Tools: Read, Write, Edit
   - Role: Content creation with PREP/SDS/DESC structure

3. **Optimizer Teammate** - Optimize metadata, structure, and links
   - Model: Opus
   - Tools: Read, Edit
   - Role: Technical SEO and schema markup

4. **Reviewer Teammate** - Final quality assurance before publication
   - Model: Opus
   - Tools: Read
   - Role: Grammar, logic, and brand consistency check

Start with test run on 1-2 keywords to validate the workflow.
```

---

## 작업 흐름

### 단일 키워드 파이프라인

```
1. Team Lead 읽기: Google Sheet에서 키워드 정보 추출
2. Researcher 할당: "키워드 '{keyword}' 리서치 완료"
3. Writer 할당: "리서치 결과 바탕으로 기사 작성"
4. Optimizer 할당: "메타데이터 및 스키마 최적화"
5. Reviewer 할당: "최종 검수 및 승인"
6. Team Lead 저장: Google Sheet 결과 탭에 저장
7. GitHub: 승인된 기사를 PR로 생성
```

### 키워드 배치 실행

```
3개 키워드 동시 처리:
  ├─ Research KW1, KW2, KW3 (병렬, ~5분)
  ├─ Write KW1, KW2, KW3 (병렬, ~10분)
  ├─ Optimize KW1, KW2, KW3 (병렬, ~5분)
  ├─ Review KW1, KW2, KW3 (병렬, ~3분)
  └─ Save all results (~2분)

총 시간: ~25분 (순차 대비 8배 빠름)
```

---

## Google Sheets 연동

### 입력 시트 (Sheet1)

```
| A: 대표 키워드 | B: 관련 키워드 | C: 대표 상황 | D: 주요 고민 | E: 검색자 심리 | F: JTBD | G: 제품 USP |
|-------------|-------------|----------|---------|-----------|--------|---------|
| 프레젠테이션 구성 | 프레젠 자료 구성, 파워포 구성... | ... | ... | ... | ... | ... |
```

### 출력 탭

- **Sheet2: 한국어 초안** - 리뷰 완료된 기사
- **Sheet3: 영어 버전** - 번역 및 로컬라이제이션
- **Sheet4: 일본어 버전** - 번역 및 로컬라이제이션
- **Sheet5: 분석 결과** - 경쟁사 분석, 트렌드 데이터

---

## 팀원 커뮤니케이션

### Team Lead → Researcher

```
"Research keyword: '{keyword}'

Target information:
- Search volume
- User intent
- Related long-tail keywords
- Top 10 competitor pages
- Content structure patterns
- Regional trends (Korea, US, Japan)

Output format: JSON at /research/{keyword}.json"
```

### Researcher → Team Lead (완료 메시지)

```
"Research complete for '{keyword}'.
- Search volume: 4,400/month
- Difficulty: High
- User intent: Informational
- Output: /research/{keyword}.json"
```

### Team Lead → Writer

```
"Write article based on research: /research/{keyword}.json

Requirements:
- Title: 50-60 chars, keyword in first 5 words
- Meta description: 155-160 chars with CTA
- Article: 2,000-2,500 words
- Structure: Intro → H2 sections (4-6) → H3 subsections → Conclusion
- Framework: PREP law (Conclusion → Reason → Example → Conclusion)
- Internal links: 3-5 relevant links
- Target audience: Beginners in the topic

Output: /content/drafts/{keyword}.md"
```

---

## 팀 모니터링

### 실시간 진행상황 확인 (인프로세스)

```
Claude Code에서:
- Shift+Down: 다음 팀원으로 전환
- Shift+Up: 이전 팀원으로 전환
- 각 팀원의 대화 히스토리 실시간 확인
```

### 팀 상태 쿼리

```
"What's the current status of the team?
- Which tasks are pending?
- Who's working on what?
- Are there any blockers?
- Show me the progress on {keyword}"
```

### 팀원 지시 (커스텀 명령)

```
"Message the writer: 'Expand the conclusion section with more actionable tips'"
"Tell the optimizer: 'Double-check the schema markup for BlogPosting'"
"Ask the reviewer: 'Check if the tone matches the brand guidelines'"
```

---

## 클라우드 스케줄 설정

### 매주 자동 실행 (권장)

```bash
/schedule
```

**설정:**
- Cron: `0 9 * * 1` (매주 월요일 9시)
- Network: Internet access enabled
- MCP: Google Sheets API, GitHub
- Environment: 
  - GOOGLE_SHEETS_ID=your-sheet-id
  - GITHUB_TOKEN=your-token

**Prompt:**
```
Generate SEO content for top 3 keywords this week.
Process:
1. Read keyword list from Google Sheet
2. Create research tasks for researcher team member
3. Monitor team progress
4. Save results when all articles approved
5. Create GitHub PR with new content
```

---

## 에러 처리

### 팀원이 막혔을 때

```
Team Lead: "What's blocking you, {teammate}?
Can I help with:
- More specific instructions?
- Additional context?
- Different approach?"
```

### 작업 재할당

```
"Reassign {task} from {current_teammate} to {new_teammate}
Provide context from previous attempt"
```

### 부분 재실행

```
"Only {new_teammate}, reprocess article: /content/drafts/{keyword}.md
Keep existing metadata, improve {specific_aspect}"
```

---

## 성능 최적화

### 모델 선택

- **Opus (권장)**: 최고 품질, 복잡한 분석 필요 시
- **Sonnet**: 비용 50% 절감, 품질 유지 (최적화 역할에 좋음)

```
Create team with Opus for researcher and writer,
Sonnet for optimizer (fast) and reviewer (straightforward task)
```

### 배치 크기

- **최적**: 3-5개 키워드 동시 처리
- **최대**: 10개 (더 이상은 조율 복잡도 ↑)

---

## 다국어 확장 (향후)

### 현재: 한국어만

```
Research → Write → Optimize → Review → Save
```

### 향후: 다국어 추가

```
한국어 (완료)
  ├─ Translator-EN Teammate
  │  └─ Researcher-EN → Writer-EN → Optimizer-EN → Reviewer-EN
  │
  └─ Translator-JA Teammate
     └─ Researcher-JA → Writer-JA → Optimizer-JA → Reviewer-JA
```

---

## 보안 및 권한

### Google Sheets API

```bash
# 인증 설정
gcloud auth application-default login
# 또는
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### GitHub 토큰

```bash
# .env 파일
GITHUB_TOKEN=ghp_...
```

### 팀 멤버 권한

- Team Lead: 모든 권한
- Teammates: 읽기/쓰기 제한 (필요한 디렉토리만)

---

## 문제 해결

### 팀이 응답하지 않음

```
1. 각 팀원 세션 상태 확인 (Shift+Down)
2. 명시적으로 작업 재할당
3. 더 구체적인 프롬프트 제공
```

### Google Sheets 연동 실패

```
1. API 인증 확인
2. Sheet ID 올바른지 확인
3. Team Lead 권한 확인
```

### 품질 저하

```
1. 팀원 모델을 Opus로 업그레이드
2. 더 상세한 프롬프트 제공
3. 참고 자료(가이드 문서) 제공
```

---

## 주요 파일 구조

```
.claude/
├── CLAUDE.md (이 파일)
├── agents/
│   ├── seo-researcher.md
│   ├── seo-writer.md
│   ├── seo-optimizer.md
│   └── seo-reviewer.md
├── loop.md (선택사항: /loop 커스텀)
└── settings.json (선택사항: 고급 설정)

/content/
├── drafts/
│   ├── {keyword}.md
│   └── ...
└── published/
    ├── {keyword}.md
    └── ...

/research/
├── {keyword}.json
└── ...
```

---

## 성공 체크리스트

- [ ] Claude Code CLI v2.1.32+ 설치
- [ ] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수 활성화
- [ ] `.claude/agents/` 디렉토리의 4개 팀원 파일 생성
- [ ] Google Sheets API 인증 설정
- [ ] GitHub 토큰 설정
- [ ] 테스트 키워드 1개로 전체 파이프라인 실행
- [ ] 각 팀원의 출력 검증
- [ ] 클라우드 스케줄 설정
- [ ] 첫 주간 자동 실행 모니터링
- [ ] 팀원 성능 피드백 반영

---

## 참고 자료

- [Claude Code 팀 에이전트](https://code.claude.com/docs/en/agent-teams)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [GitHub API](https://docs.github.com/en/rest)

---

## 연락처 및 지원

이 프로젝트에 대한 질문이나 문제가 있으면:
1. `.claude/CLAUDE.md` 최신 버전 확인
2. 각 팀원 에이전트 정의 확인
3. Team Lead 로그 검토
4. Claude Code 공식 문서 참고

---

**마지막 업데이트:** 2026-04-13
**버전:** 1.0 (팀 에이전트 최초 구현)
