#!/usr/bin/env python3
"""
Google Sheets API OAuth 2.0 인증 스크립트
처음 실행 시 브라우저에서 인증이 필요합니다.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# 현재 스크립트 디렉토리
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'token.json')

def authenticate():
    """
    Google Sheets API 인증
    처음 실행 시 브라우저를 열어 인증 요청
    이후 token.json이 자동으로 갱신됨
    """
    creds = None

    # token.json이 이미 존재하면 로드
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 토큰이 없거나 만료됨
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 새로운 인증 흐름 시작
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        # 토큰 저장
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"\n✅ 인증 완료! 토큰이 저장되었습니다: {TOKEN_FILE}")
    else:
        print(f"✅ 기존 토큰을 사용합니다: {TOKEN_FILE}")

    return creds

if __name__ == '__main__':
    try:
        creds = authenticate()
        print("\n✅ Google Sheets API 인증 성공!")
        print(f"클라이언트 ID: {creds.client_id}")
        print(f"스코프: {creds.scopes}")
    except Exception as e:
        print(f"\n❌ 인증 실패: {e}")
        exit(1)
