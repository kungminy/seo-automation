#!/usr/bin/env python3
"""
Google Sheets Sheet1 데이터 읽기
"""

import os
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
print("📊 구글 시트 Sheet1 데이터 읽기")
print("=" * 100)
print(f"📋 Sheet ID: {SPREADSHEET_ID}\n")

try:
    # 먼저 스프레드시트 메타데이터 가져오기 (시트 이름 확인)
    spreadsheet = sheets_service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID
    ).execute()

    sheets = spreadsheet.get('sheets', [])
    sheet_names = [sheet['properties']['title'] for sheet in sheets]

    print(f"📄 사용 가능한 시트: {sheet_names}\n")

    # 첫 번째 시트의 이름 사용
    first_sheet_name = sheet_names[0] if sheet_names else 'Sheet1'

    # 데이터 읽기
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{first_sheet_name}'
    ).execute()

    values = result.get('values', [])

    if not values:
        print("❌ 데이터가 없습니다.")
    else:
        # 헤더 출력
        headers = values[0]
        print("📌 헤더 (컬럼):")
        for i, header in enumerate(headers, 1):
            print(f"  {i}. {header}")

        print("\n" + "-" * 100)
        print("📝 데이터 행:\n")

        # 데이터 행 출력
        for row_num, row in enumerate(values[1:], 1):
            # 빈 행 스킵
            if not row or all(cell.strip() == '' for cell in row if isinstance(cell, str)):
                continue

            print(f"🔹 행 {row_num}:")
            for col_idx, header in enumerate(headers):
                cell_value = row[col_idx] if col_idx < len(row) else ''
                if cell_value.strip():
                    print(f"   {header}: {cell_value}")
            print()

        print("=" * 100)
        print(f"✅ 총 {len(values) - 1}개 데이터 행 읽음")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    exit(1)
