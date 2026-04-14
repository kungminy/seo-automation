# 미리캔버스 SEO 페이지 자동 생성 시스템
## 에이전트 구조도 및 워크플로우

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SEO PAGE AUTO GENERATOR SYSTEM                         │
│                      (Google Sheets 기반 자동화)                          │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │  Master Executor │
                              │   (Orchestrator) │
                              └────────┬─────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
    ┌────────────┐             ┌──────────────┐            ┌─────────────┐
    │   Stage 1  │             │   Stage 2    │            │   Stage 3   │
    │   Data     │             │   Content    │            │   QA/Edit   │
    │ Collector  │             │  Generator   │            │             │
    └──────┬─────┘             └──────┬───────┘            └──────┬──────┘
           │                          │                           │
           │ [Google Sheets]          │ [Claude API]              │
           │                          │                           │
    ┌──────────────────────┐  ┌──────────────────────┐   ┌────────────────┐
    │ Input Data Schema:   │  │ Generation Features: │   │ Review Checklist│
    │ • 대표 키워드        │  │ • H1, Title,        │   │ • 문법 검수    │
    │ • 관련 키워드        │  │   Description       │   │ • 로직 일관성  │
    │ • 대표 상황(CEP)     │  │ • H2/H3 구조        │   │ • SEO 최적화   │
    │ • 주요 고민/질문     │  │ • 목차 자동 생성    │   │ • 한국어 다듬기│
    │ • 검색자 심리        │  │ • PREP/SDS/DESC     │   │ • 이미지 지시  │
    │ • JTBD               │  │   프레임워크 적용   │   │ • 링크 검증    │
    │ • 제품 USP           │  │ • 메인 CTA 생성     │   └────────────────┘
    │ • 경쟁사 분석 자료   │  │ • 내부 링크 제안    │
    └──────────────────────┘  └──────────────────────┘
        │ Output: Validated      │ Output: Initial Draft
        │ Input JSON             │

        ┌───────────────────────────────────────────────────────────────┐
        │                                                               │
        ▼                                                               ▼
    ┌────────────┐                                              ┌──────────────┐
    │   Stage 4  │                                              │    Stage 5   │
    │Translation │◄────────────────────────────────────────────┤Translation & │
    │  & Localize│                                              │   Analysis   │
    └──────┬─────┘                                              └──────┬───────┘
           │                                                           │
           ├─────────────────┬──────────────────┬────────────────────┤
           │                 │                  │                    │
           ▼                 ▼                  ▼                    ▼
    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌─────────────┐
    │  English   │    │  Japanese  │    │   Trend    │    │ Competitor  │
    │Translation │    │Translation │    │  Analysis  │    │  Analysis   │
    │            │    │            │    │            │    │             │
    │ • Translator│   │ • Translator│   │ • KW Search│    │ • SERP Top  │
    │   Agent    │    │   Agent    │    │   Volume   │    │   10 Pages  │
    │ • Tone     │    │ • Tone     │    │ • Regional │    │ • Title/Desc│
    │   Adapt    │    │   Adapt    │    │   Trends   │    │   Patterns  │
    │ • Grammar  │    │ • Grammar  │    │ • Traffic  │    │ • Keywords  │
    │   Check    │    │   Check    │    │   Season   │    │   Used      │
    └────┬───────┘    └────┬───────┘    └────┬───────┘    └──────┬──────┘
         │                 │                 │                   │
         └─────────────────┴─────────────────┴───────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │  Content Finalization    │
                    │  & Output Generation     │
                    │                          │
                    │ • Final Review           │
                    │ • Google Sheets Updated  │
                    │ • Multi-language Drafts  │
                    │ • Ready for Publication  │
                    └──────────────────────────┘
```

---

## 각 에이전트 상세 설명

### 1️⃣ **Data Collector Agent** (Stage 1)
**목적**: 구글 시트에서 SEO 입력 정보 수집

**입력 데이터**:
```
대표 키워드 (대표) | 관련 키워드 | 대표 상황(CEP) | 주요 고민&질문 | 검색자 심리 | JTBD | 제품 USP
프레젠테이션 구성 | 프레젠 자료 | 파워포 구성    | [여러 관련 키워드들...] | 초보자가 겪는 실패 | 실용적 가이드 | AI 기능 체험
```

**처리 로직**:
- Google Sheets API로 입력 데이터 읽기
- 데이터 유효성 검증
- JSON 형식으로 정규화
- 다음 단계로 전달

**출력**: 구조화된 JSON 데이터

---

### 2️⃣ **Content Generator Agent** (Stage 2)
**목적**: Claude AI를 사용하여 SEO 최적화 초안 생성

**프롬프트 템플릿**:
```
당신은 미리캔버스 SEO 블로그 콘텐츠 전문가입니다.

[입력 데이터]
- 대표 키워드: {keyword}
- 관련 키워드: {related_keywords}
- 타겟 상황: {situation}
- 검색자 심리: {psychology}
- 제품 USP: {usp}

[생성 요구사항]
1. SEO 최적화 제목 (Title, 60자 이내)
2. 메타 설명 (Description, 160자 이내)
3. H1 - H3 구조화된 목차
4. 각 섹션별 본문 (500-800자)
5. PREP/SDS/DESC 프레임워크 적용
6. 메인 CTA (Call-to-Action)
7. 내부 링크 제안 (3-5개)

[참고 가이드 문서]
- PREP법: 결론 → 이유 → 사례 → 결론
- SDS법: 요약 → 상세 → 정리
- DESC법: 묘사 → 의견 → 제안 → 결과

[출력 형식]
JSON 형식으로 다음 구조로 반환:
{
  "title": "...",
  "description": "...",
  "h1": "...",
  "content_outline": {
    "h2_1": {
      "heading": "...",
      "h3_items": ["...", "..."],
      "body": "..."
    }
  },
  "cta": "...",
  "internal_links": ["...", "..."]
}
```

**생성 결과**:
- SEO 최적화된 제목 및 설명
- 논리적 흐름의 목차 구조
- 각 섹션별 상세 본문
- CTA 문구
- 내부 링크 제안

---

### 3️⃣ **QA/Edit Agent** (Stage 3)
**목적**: 한국어 초안 검수 및 개선

**검수 항목**:
- ✅ 문법 및 맞춤법
- ✅ 논리적 일관성 (PREP/SDS/DESC 구조 확인)
- ✅ SEO 최적화 (키워드 배치, 자연스러움)
- ✅ 타겟층과 톤&매너 일치
- ✅ 길이 적절성 (너무 길거나 짧지 않은지)
- ✅ 이미지/시각 요소 지시사항 추가
- ✅ 링크 유효성

**출력**: 검수된 한국어 초안 (Reviewed Korean Draft)

---

### 4️⃣ **Translation Agents** (Stage 4a, 4b)

#### **4a. English Translation Agent**
**처리**:
- 한국어 → 영어 번역
- 영미 비즈니스 톤 적용
- SEO 키워드 영어화
- 미국/영국 표현 표준화

#### **4b. Japanese Translation Agent**
**처리**:
- 한국어 → 일본어 번역
- 일본 비즈니스 매너(敬語) 적용
- 일본 검색 트렌드 반영
- 히라가나/가타카나 표기 확인

---

### 5️⃣ **Analysis Agents** (Stage 5a, 5b)

#### **5a. Trend Analysis Agent**
**분석 항목**:
- 🔍 각 언어권 검색 트렌드
- 📊 키워드 검색량 및 트렌드
- 📈 계절성 및 주기성
- 🎯 지역별 관심도
- 💡 관련 검색어 (People Also Ask)

#### **5b. Competitor Analysis Agent**
**분석 항목**:
- 🏆 상위 노출 페이지 10개 분석
- 📝 제목/설명 패턴
- 📌 주요 키워드 사용량
- 🎨 콘텐츠 구조 및 길이
- 🔗 백링크 전략
- 💬 사용자 Q&A 분석

---

## 워크플로우 실행 방식

### **옵션 1: Google Sheets 기반 자동화** (추천)

```
구글 시트 [입력]
    ↓
[Google Sheets API]
    ↓
[Stage 1: Data Collector]
    ↓
[Stage 2: Content Generator] → Claude API
    ↓
[Stage 3: QA/Edit Agent]
    ↓
[Stage 4: Translation Agents]
    ↓
[Stage 5: Analysis Agents]
    ↓
구글 시트 [출력 탭: 초안]
구글 시트 [출력 탭: 영어]
구글 시트 [출력 탭: 일본어]
구글 시트 [출력 탭: 분석]
```

**구글 시트 구조**:
- **입력 탭**: 원본 정보 입력
- **한국어 초안 탭**: Stage 3 결과
- **영어 버전 탭**: Stage 4a 결과 + 5a 분석
- **일본어 버전 탭**: Stage 4b 결과 + 5b 분석
- **분석 탭**: Trend & Competitor Analysis

---

### **옵션 2: 터미널 기반 CLI 자동화**

```bash
# 실행 명령어
python seo_generator.py \
  --sheet-id "YOUR_GOOGLE_SHEET_ID" \
  --input-range "Sheet1!A1:H10" \
  --output-range "Sheet2!A1" \
  --languages "ko,en,ja" \
  --include-analysis true
```

**결과**:
- `output_ko.json` - 한국어 초안
- `output_en.json` - 영어 버전
- `output_ja.json` - 일본어 버전
- `analysis.json` - 트렌드/경쟁사 분석

---

## 기술 스택

| 역할 | 도구/기술 |
|------|---------|
| 데이터 수집 | Google Sheets API, gspread |
| AI 생성 | Claude API (claude-opus-4-6) |
| 번역 | Claude API (다국어 프롬프트) 또는 Google Translate API |
| 데이터 처리 | Python, Pandas |
| 자동화 | Google Apps Script 또는 Python Scheduler |
| 저장소 | Google Sheets, JSON files |

---

## 실행 순서

1. **준비 단계**
   - Google Sheets 템플릿 생성
   - Google API 인증 설정
   - Claude API 키 설정

2. **Stage 1-3 (한국어)**
   - 구글 시트에 입력 데이터 작성
   - Data Collector 실행
   - Content Generator 실행 (Claude API)
   - QA Agent 검수

3. **Stage 4-5 (다국어 + 분석)**
   - Translation Agents 실행
   - Analysis Agents 실행

4. **최종 리뷰**
   - 구글 시트의 모든 탭 검토
   - 필요시 수정 후 재생성

---

## 다음 단계

1. **Google Sheets 템플릿 설계** - 입력/출력 탭 구조
2. **Claude API 프롬프트 최적화** - 각 Stage별 상세 프롬프트
3. **Python 자동화 스크립트 작성** - Google Sheets ↔ Claude API 연동
4. **테스트 및 반복 개선** - 생성된 콘텐츠 품질 검증

