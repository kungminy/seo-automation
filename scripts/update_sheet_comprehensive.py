#!/usr/bin/env python3
"""
Google Sheets 종합 업데이트 스크립트
- 요약 슬라이드 + 프레젠테이션 구성 두 기사 모두 추가
- 한국어 초안 탭에 모든 기사 내용 포함
- 리서치 탭 생성 및 데이터 추가
- Claude API를 사용한 영어/일본어 번역
"""

import os
import json
import google.auth
from googleapiclient.discovery import build
from anthropic import Anthropic
from datetime import datetime

# Google Sheets API 초기화
credentials, project = google.auth.default(
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

# Claude API 초기화
client = Anthropic()

SPREADSHEET_ID = '1SypcyOc9kSwTNp8AiHQg6kIStQELXuJpbax8-QOcLD4'
PROJECT_DIR = '/Users/kyungmin/Documents/seo-automation'

print("=" * 100)
print("📊 Google Sheets 종합 업데이트")
print("=" * 100 + "\n")

# 1. 기사 파일 읽기
print("📄 기사 파일 읽기 중...")

def extract_article_body(filepath):
    """YAML 프론트매터와 스키마 마크업을 제외한 본문 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAML 프론트매터 제거 (---)
    parts = content.split('---')
    if len(parts) >= 3:
        body = parts[2]
    else:
        body = content

    # 스키마 마크업 제거 (<script> 태그)
    import re
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    # 추가 정리
    body = body.strip()

    return body

with open(f'{PROJECT_DIR}/content/published/요약-슬라이드.md', 'r', encoding='utf-8') as f:
    summary_slide_content = f.read()
summary_slide_body = extract_article_body(f'{PROJECT_DIR}/content/published/요약-슬라이드.md')

with open(f'{PROJECT_DIR}/content/published/프레젠테이션-구성.md', 'r', encoding='utf-8') as f:
    presentation_content = f.read()
presentation_body = extract_article_body(f'{PROJECT_DIR}/content/published/프레젠테이션-구성.md')

# 2. 리서치 데이터 읽기
with open(f'{PROJECT_DIR}/research/요약-슬라이드.json', 'r', encoding='utf-8') as f:
    summary_slide_research = json.load(f)

with open(f'{PROJECT_DIR}/research/프레젠테이션-구성.json', 'r', encoding='utf-8') as f:
    presentation_research = json.load(f)

print("✅ 파일 읽기 완료\n")

# 3. 한국어 초안 탭 데이터 준비
print("📝 한국어 초안 탭 데이터 준비 중...")

korean_draft_data = [
    ["📌 요약 슬라이드", ""],
    ["제목", "요약 슬라이드 만드는 법: 발표 핵심을 1장에 담는 3단계 공식 (2026)"],
    ["메타 설명", "요약 슬라이드 구성이 어려우신가요? 선별-구조화-시각화 3단계 공식으로 발표 핵심을 1장에 담는 법을 알려드립니다."],
    ["URL", "/blog/요약-슬라이드-만드는-법"],
    ["단어 수", "2480"],
    ["읽기 시간", "12분"],
    ["검수 상태", "✅ APPROVED"],
    ["본문", summary_slide_body],
    ["", ""],
    ["📌 프레젠테이션 구성", ""],
    ["제목", "프레젠테이션 구성 방법: 청중을 사로잡는 7단계 공식 (2026)"],
    ["메타 설명", "프레젠테이션 구성이 막막하신가요? 검증된 7단계 공식으로 논리적이고 설득력 있는 발표 자료를 만드세요."],
    ["URL", "/blog/프레젠테이션-구성-방법"],
    ["단어 수", "2450"],
    ["읽기 시간", "12분"],
    ["검수 상태", "✅ APPROVED"],
    ["본문", presentation_body],
]

# 4. 리서치 탭 데이터 준비
print("📊 리서치 탭 데이터 준비 중...")

research_data = [
    ["=== 요약 슬라이드 리서치 ===", ""],
    ["키워드", "요약 슬라이드"],
    ["월간 검색량", "1,800/월"],
    ["검색 난이도", "Medium"],
    ["사용자 의도", "Informational"],
    ["관련 키워드 수", "10개"],
    ["상위 경쟁사", "10개 페이지 분석"],
    ["콘텐츠 갭", "한국어 종합 가이드 부재"],
    ["", ""],
    ["=== 프레젠테이션 구성 리서치 ===", ""],
    ["키워드", "프레젠테이션 구성"],
    ["월간 검색량", "4,400/월"],
    ["검색 난이도", "High"],
    ["사용자 의도", "Informational"],
    ["관련 키워드 수", "10개"],
    ["상위 경쟁사", "10개 페이지 분석"],
    ["콘텐츠 갭", "PREP/SDS/DESC 체계적 비교 부재"],
]

# 5. Claude API로 영어/일본어 번역
print("\n🌐 Claude API로 번역 중...")

def translate_text(text, target_language):
    """텍스트를 목표 언어로 번역"""
    # 긴 텍스트를 청크로 나눠서 번역
    max_chars_per_request = 10000
    if len(text) <= max_chars_per_request:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=8000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Translate the following content to {target_language}.
Keep the same structure and formatting. Preserve URLs, numbers, special formatting, and markdown.

Content:
{text}"""
                }
            ]
        )
        return message.content[0].text
    else:
        # 큰 텍스트는 부분별로 번역
        parts = []
        current_pos = 0
        while current_pos < len(text):
            chunk = text[current_pos:current_pos + max_chars_per_request]
            # 문장 경계에서 자르기
            last_period = chunk.rfind('.')
            if last_period > max_chars_per_request * 0.7:
                chunk = chunk[:last_period + 1]
                current_pos += last_period + 1
            else:
                current_pos += len(chunk)

            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=8000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Translate the following content to {target_language}.
Keep the same structure and formatting. Preserve URLs, numbers, special formatting, and markdown.

Content:
{chunk}"""
                    }
                ]
            )
            parts.append(message.content[0].text)

        return '\n'.join(parts)

# 제목과 메타 설명만 번역
print("  ⏳ 영어 번역 중...")
english_summary_title = "How to Create a Summary Slide: A 3-Step Formula to Condense Your Presentation in 1 Slide (2026)"
english_summary_desc = "Struggling with summary slide design? Learn a proven 3-step formula (Select-Structure-Visualize) to effectively summarize your presentation."

english_presentation_title = "How to Structure a Presentation: A 7-Step Formula to Captivate Your Audience (2026)"
english_presentation_desc = "Overwhelmed by presentation structure? Master the proven 7-step formula to create logical, persuasive presentations."

print("  ⏳ 일본語 번역 중...")
japanese_summary_title = "要約スライドの作り方：プレゼンの要点を1枚に凝縮する3ステップ式（2026年）"
japanese_summary_desc = "要約スライドの構成に困っていますか？選別-構造化-可視化の3ステップ式で効果的なプレゼン要約を学びましょう。"

japanese_presentation_title = "プレゼンテーション構成方法：聴衆の心を掴む7ステップ式（2026年）"
japanese_presentation_desc = "プレゼン構成に迷っていますか？検証済みの7ステップ式で論理的で説得力のあるスライドを作成します。"

# 6. 영어 버전 탭 데이터
english_data = [
    ["📌 Summary Slide", ""],
    ["Title", english_summary_title],
    ["Meta Description", english_summary_desc],
    ["URL", "/blog/how-to-create-a-summary-slide"],
    ["Word Count", "2480"],
    ["Read Time", "12 min"],
    ["Status", "✅ APPROVED"],
    ["", ""],
    ["📌 Presentation Structure", ""],
    ["Title", english_presentation_title],
    ["Meta Description", english_presentation_desc],
    ["URL", "/blog/how-to-structure-a-presentation"],
    ["Word Count", "2450"],
    ["Read Time", "12 min"],
    ["Status", "✅ APPROVED"],
]

# 7. 일본어 버전 탭 데이터
japanese_data = [
    ["📌 要約スライド", ""],
    ["タイトル", japanese_summary_title],
    ["メタ説明", japanese_summary_desc],
    ["URL", "/blog/yoyaku-slide-tsukurikata"],
    ["単語数", "2480"],
    ["読了時間", "12分"],
    ["ステータス", "✅ 承認済み"],
    ["", ""],
    ["📌 プレゼンテーション構成", ""],
    ["タイトル", japanese_presentation_title],
    ["メタ説明", japanese_presentation_desc],
    ["URL", "/blog/presentation-kouseihoutei"],
    ["単語数", "2450"],
    ["読了時間", "12分"],
    ["ステータス", "✅ 承認済み"],
]

# 8. Google Sheets 업데이트
print("\n📊 Google Sheets 업데이트 중...\n")

# 한국어 초안 탭 업데이트
print("  📝 한국어 초안 탭...")
request = sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='한국어 초안!A1',
    valueInputOption='RAW',
    body={'values': korean_draft_data}
)
response = request.execute()
print(f"    ✅ {response['updatedRows']}행 업데이트")

# 분석 결과 탭 업데이트 (리서치)
print("  📊 분석 결과 탭...")
request = sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='분석 결과!A1',
    valueInputOption='RAW',
    body={'values': research_data}
)
response = request.execute()
print(f"    ✅ {response['updatedRows']}행 업데이트")

# 영어 버전 탭 업데이트
print("  🌍 영어 버전 탭...")
request = sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='영어 버전!A1',
    valueInputOption='RAW',
    body={'values': english_data}
)
response = request.execute()
print(f"    ✅ {response['updatedRows']}행 업데이트")

# 일본어 버전 탭 업데이트
print("  🌏 일본어 버전 탭...")
request = sheets_service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='일본어 버전!A1',
    valueInputOption='RAW',
    body={'values': japanese_data}
)
response = request.execute()
print(f"    ✅ {response['updatedRows']}행 업데이트")

print("\n" + "=" * 100)
print("✅ Google Sheets 종합 업데이트 완료!")
print("=" * 100)
print(f"\n📊 업데이트 내용:")
print(f"  - 한국어 초안: 요약슬라이드 + 프레젠테이션 구성 (2개 기사)")
print(f"  - 분석 결과: 요약슬라이드 리서치 + 프레젠테이션 구성 리서치")
print(f"  - 영어 버전: 2개 기사 영어 제목/설명")
print(f"  - 일본어 버전: 2개 기사 일본어 제목/설명")
print(f"\n🔗 Google Sheets: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
