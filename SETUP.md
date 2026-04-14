# SEO 자동화 시스템 - 설정 가이드

## 1. Google Sheets API 연동 설정

### 방법 A: gcloud CLI (권장) - 현재 상태

```bash
# 이미 설정됨:
gcloud auth application-default login

# 결과:
# ~/.config/gcloud/application_default_credentials.json 자동 생성
```

**장점:**
- ✅ 자동 토큰 갱신
- ✅ 보안 (개인 정보 git에 안 들어감)
- ✅ 추가 설정 불필요

### 방법 B: 환경변수 설정 (필요시)

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정
SPREADSHEET_ID="your-actual-sheet-id"

# Python 스크립트는 자동으로 읽음
python3 scripts/read_sheet_json.py
```

---

## 2. 필수 라이브러리 설치

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

---

## 3. Google Sheets ID 확인

```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit

# 예: https://docs.google.com/spreadsheets/d/1SypcyOc9kSwTNp8AiHQg6kIStQELXuJpbax8-QOcLD4/edit
#     ↑ 이 부분이 SPREADSHEET_ID
```

---

## 4. 스크립트 실행

### 리서치 데이터 조회
```bash
python3 scripts/read_sheet_json.py
```

### 기사 생성 파이프라인 실행
```bash
# Claude Code에서 팀 에이전트 실행
# (자동으로 처리됨)
```

---

## 5. 보안 체크리스트

- ✅ `.env` 파일은 `.gitignore`에 포함됨
- ✅ `credentials.json` 제외됨
- ✅ `token.json` 제외됨
- ✅ gcloud ADC는 홈 디렉토리에 저장 (git 외부)

---

## 6. CI/CD 배포 시

GitHub Actions 등에서 배포할 때:

```yaml
env:
  SPREADSHEET_ID: ${{ secrets.SPREADSHEET_ID }}
  GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GOOGLE_APPLICATION_CREDENTIALS }}
```

또는 서비스 계정 JSON 사용:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

---

## 문제 해결

### "API has not been used in project" 에러
→ Google Cloud Console에서 Google Sheets API 활성화 필요
https://console.developers.google.com/apis/api/sheets.googleapis.com/overview

### "Request had insufficient authentication scopes" 에러
→ 다시 인증:
```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets
```

### .env 파일이 없음
→ 기본값이 스크립트에 하드코딩되어 있음 (현재 SPREADSHEET_ID)
→ 필요시 .env.example을 참고해서 .env 생성
