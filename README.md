# SWIFT ValidateAI Enterprise

Flask tabanli SWIFT mesaj dogrulama API'si. Uygulama lokal gelistirmede Azure zorunlu olmadan calisir; Azure Blob Storage bilgisi saglandiginda dogrulama kayitlarini tarih bazli klasorlerle saklar.

## Ozellikler

- JSON API ile SWIFT mesaj dogrulama
- Zorunlu alan, tutar, para birimi ve BIC format kontrolleri
- Opsiyonel `X-API-Key` veya `Authorization: Bearer ...` korumasi
- Azure Blob Storage'a opsiyonel, gecikmeli baglanti
- Azure Key Vault'tan secret okuma destegi
- Basit web arayuzu
- Pytest testleri

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Uygulama varsayilan olarak `http://localhost:5000` adresinde calisir.

## Ortam Degiskenleri

- `API_KEY`: Ayarlanirsa `/validate` endpoint'i API key ister.
- `AZURE_STORAGE_CONNECTION_STRING`: Blob Storage baglanti string'i.
- `AZURE_STORAGE_CONTAINER`: Blob container adi. Varsayilan: `messages`.
- `KEY_VAULT_URL`: Key Vault URL'si.
- `AZURE_STORAGE_CONNECTION_SECRET_NAME`: Key Vault icindeki storage secret adi. Varsayilan: `AZURE_STORAGE_CONNECTION_STRING`.
- `REQUIRE_STORAGE`: `true` ise storage yazimi basarisiz oldugunda API hata dondurur.

## API

### `GET /health`

Saglik kontrolu.

### `POST /validate`

Ornek istek:

```json
{
  "TransactionReference": "TRX-2026-0001",
  "Amount": "1250.50",
  "Currency": "USD",
  "SenderBIC": "DEUTDEFF",
  "ReceiverBIC": "NWBKGB2L"
}
```

Basarili dogrulama `200`, gecersiz mesaj `422`, hatali JSON `400/415` dondurur.

## Test

```bash
pytest
```
