#!/usr/bin/env python3
"""
생성된 SEO 페이지 결과를 Google Sheets에 업데이트
SEO_PAGE_GENERATOR_ARCHITECTURE.md 구조에 따라:
- Sheet2: 한국어 초안 탭
- Sheet5: 분석 탭
"""

import os
import json
import google.auth
from googleapiclient.discovery import build
from datetime import datetime

# Application Default Credentials 사용
credentials, project = google.auth.default(
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Google Sheets API 초기화
sheets_service = build('sheets', 'v4', credentials=credentials)

# Sheet ID
SPREADSHEET_ID = '1SypcyOc9kSwTNp8AiHQg6kIStQELXuJpbax8-QOcLD4'

print("=" * 100)
print("📊 SEO 페이지 결과를 Google Sheets에 업데이트")
print("=" * 100 + "\n")

try:
    # 1. 리서치 데이터 읽기
    with open('/Users/kyungmin/Documents/seo-automation/research/요약-슬라이드.json', 'r', encoding='utf-8') as f:
        research_data = json.load(f)

    # 2. 한국어 초안 탭(Sheet2) 데이터 준비
    korean_draft_data = [
        [
            "대표 키워드",
            "요약 슬라이드"
        ],
        [
            "제목",
            "요약 슬라이드 만드는 법: 발표 핵심을 1장에 담는 3단계 공식 (2026)"
        ],
        [
            "메타 설명",
            "요약 슬라이드 구성이 어려우신가요? 선별-구조화-시각화 3단계 공식으로 발표 핵심을 1장에 담는 법을 알려드립니다. 업무 보고·투자 피칭·학교 발표 상황별 실전 예시, 흔한 실수 5가지와 Before/After 개선 사례, AI 자동 생성 팁까지 총정리했습니다. 지금 바로 확인하세요!"
        ],
        [
            "URL 슬러그",
            "/blog/요약-슬라이드-만드는-법"
        ],
        [
            "단어 수",
            "2480"
        ],
        [
            "읽기 시간",
            "12분"
        ],
        [
            "관련 키워드",
            "프레젠테이션 요약 슬라이드, PPT 요약 페이지, 발표 마무리 슬라이드, PPT 결론 슬라이드, executive summary 슬라이드, 발표 정리 슬라이드, 요약 슬라이드 템플릿"
        ],
        [
            "검수 상태",
            "✅ APPROVED"
        ],
        [
            "발행 상태",
            "✅ 발행 준비 완료"
        ],
        [
            "발행 날짜",
            datetime.now().strftime("%Y-%m-%d")
        ]
    ]

    # 3. 분석 탭(Sheet5) 데이터 준비
    kw_analysis = research_data['keyword_analysis']
    comp_analysis = research_data['competitive_analysis']

    analysis_data = [
        [
            "분석 항목",
            "값"
        ],
        [
            "키워드",
            research_data['keyword']
        ],
        [
            "분석 날짜",
            research_data['analyzed_date']
        ],
        [
            "",
            ""
        ],
        [
            "=== 키워드 분석 ===",
            ""
        ],
        [
            "주요 키워드",
            kw_analysis['primary_keyword']
        ],
        [
            "월간 검색량",
            str(kw_analysis['estimated_search_volume'])
        ],
        [
            "검색 난이도",
            kw_analysis['search_difficulty']
        ],
        [
            "사용자 의도",
            kw_analysis['user_intent']
        ],
        [
            "키워드 타입",
            kw_analysis['keyword_type']
        ],
        [
            "관련 키워드 수",
            str(len(kw_analysis['related_keywords']))
        ],
    ]

    # 관련 키워드 추가
    analysis_data.append(["", ""])
    analysis_data.append(["=== 관련 키워드 (Top 10) ===", ""])
    for kw in kw_analysis['related_keywords']:
        analysis_data.append([
            kw['keyword'],
            f"검색량: {kw['search_volume']}, 의도: {kw['intent']}"
        ])

    # 경쟁사 분석 추가
    analysis_data.append(["", ""])
    analysis_data.append(["=== 경쟁사 분석 ===", ""])
    analysis_data.append(["분석 항목", "값"])
    analysis_data.append(["평균 H2 수", str(comp_analysis['common_structure']['average_h2_count'])])
    analysis_data.append(["일반적 단어 수", str(comp_analysis['common_structure']['typical_word_count'])])
    analysis_data.append(["분석 대상 페이지 수", "10개"])

    # 주요 섹션 추가
    analysis_data.append(["", ""])
    analysis_data.append(["=== 일반적 콘텐츠 구조 ===", ""])
    for section in comp_analysis['common_structure']['common_sections']:
        analysis_data.append([section, ""])

    # 콘텐츠 갭 추가
    analysis_data.append(["", ""])
    analysis_data.append(["=== 콘텐츠 갭 (기회) ===", ""])
    for i, gap in enumerate(comp_analysis['content_gaps'], 1):
        analysis_data.append([f"{i}. {gap}", ""])

    # 4. Google Sheets 업데이트
    print("📝 한국어 초안 시트 업데이트 중...")

    request = sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='한국어 초안!A1',
        valueInputOption='RAW',
        body={'values': korean_draft_data}
    )
    response = request.execute()
    print(f"✅ 한국어 초안 시트 업데이트 완료: {response['updatedRows']}행")

    print("\n📊 분석 결과 시트 업데이트 중...")

    request = sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='분석 결과!A1',
        valueInputOption='RAW',
        body={'values': analysis_data}
    )
    response = request.execute()
    print(f"✅ 분석 결과 시트 업데이트 완료: {response['updatedRows']}행")

    print("\n" + "=" * 100)
    print("✅ Google Sheets 업데이트 완료!")
    print("=" * 100)
    print(f"\n📊 업데이트된 데이터:")
    print(f"  - Sheet2 (한국어 초안): {len(korean_draft_data)}행")
    print(f"  - Sheet5 (분석 탭): {len(analysis_data)}행")
    print(f"\n🔗 Google Sheets: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    exit(1)
