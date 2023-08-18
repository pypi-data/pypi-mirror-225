from google.oauth2 import service_account

CREDENTIALS_FILE = 'Repos/stg_development/sown-ml-2023/wheel_development/srq_score_wheel/app_io/sown-translate-prod.json'

GOOGLE_TRANSLATE_API_CREDENTIALS = service_account \
                                   .Credentials \
                                   .from_service_account_file(CREDENTIALS_FILE)       