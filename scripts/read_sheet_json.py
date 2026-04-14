#!/usr/bin/env python3
"""
Google Sheets 데이터를 JSON으로 출력
"""

import os
import json
import google.auth
from googleapiclient.discovery import build
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Application Default Credentials 사용
credentials, project = google.auth.default(
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

# Google Sheets API 초기화
sheets_service = build('sheets', 'v4', credentials=credentials)

# .env에서 SPREADSHEET_ID 읽기
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1SypcyOc9kSwTNp8AiHQg6kIStQELXuJpbax8-QOcLD4')

print("=" * 100)
print("📊 구글 시트 모든 데이터 (JSON 형식)")
print("=" * 100 + "\n")

try:
    # 먼저 스프레드시트 메타데이터 가져오기
    spreadsheet = sheets_service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID
    ).execute()

    sheets = spreadsheet.get('sheets', [])

    for sheet in sheets:
        sheet_title = sheet['properties']['title']
        print(f"📋 시트: {sheet_title}")
        print("-" * 100)

        # 데이터 읽기
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_title
        ).execute()

        values = result.get('values', [])

        if not values:
            print("(데이터 없음)\n")
            continue

        # 헤더와 데이터를 딕셔너리 리스트로 변환
        headers = values[0]
        data_list = []

        for row in values[1:]:
            # 빈 행 스킵
            if not row or all(cell.strip() == '' for cell in row if isinstance(cell, str)):
                continue

            row_dict = {}
            for col_idx, header in enumerate(headers):
                cell_value = row[col_idx] if col_idx < len(row) else ''
                row_dict[header] = cell_value

            data_list.append(row_dict)

        # JSON으로 출력 (들여쓰기 포함)
        print(json.dumps(data_list, ensure_ascii=False, indent=2))
        print("\n" + "=" * 100 + "\n")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    exit(1)
