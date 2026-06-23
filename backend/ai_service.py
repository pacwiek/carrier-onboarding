from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
from io import BytesIO

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_documents(folder: str):

    folder = Path(folder)

    if not folder.exists():
        return f"Folder nie istnieje: {folder}"

    pdf_files = [
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".pdf"
    ]

    if not pdf_files:
        return "Nie znaleziono dokumentów PDF."

    print(f"Znaleziono {len(pdf_files)} plików PDF.")

    content = []

    for pdf in pdf_files:

        print(f"Wysyłam: {pdf.name}")

        try:

            with open(pdf, "rb") as f:
                data = f.read()

            stream = BytesIO(data)

            # OpenAI rozpoznaje rozszerzenie po nazwie
            stream.name = pdf.stem + ".pdf"

            uploaded = client.files.create(
                file=stream,
                purpose="user_data"
            )

            print(f"OK -> {uploaded.id}")

            content.append(
                {
                    "type": "input_file",
                    "file_id": uploaded.id
                }
            )

        except Exception as error:

            print(f"Błąd podczas wysyłania {pdf.name}")

            print(error)

    if not content:
        return "Nie udało się wysłać żadnego dokumentu."

    content.append(
        {
            "type": "input_text",
            "text": """
Jesteś doświadczonym audytorem przewoźników drogowych.

Przeanalizuj wszystkie załączone dokumenty i przygotuj zwięzły raport.

Raport nie może przekroczyć 150 słów.

Skup się wyłącznie na informacjach istotnych dla podjęcia decyzji o współpracy.


## 🔍 WERYFIKACJA DOKUMENTÓW

W punktach oceń:

• czy dokumenty są spójne,
• czy dane we wszystkich dokumentach są zgodne,
• czy występują oznaki edycji graficznej, manipulacji lub podrobienia,
• jeżeli nie można tego jednoznacznie ocenić, napisz:
  "Nie stwierdzono oczywistych oznak ingerencji na podstawie dostarczonych dokumentów."

## 👥 ZARZĄD / WŁAŚCICIELE

Podaj w punktach:

• właścicieli lub wspólników,
• członków zarządu,
• sposób reprezentacji spółki.

## 📄 KLUCZOWE INFORMACJE

W punktach podaj wyłącznie:

• ważność licencji transportowej (jeżeli dostępna),
• najważniejsze informacje z polisy OCP (ubezpieczyciel, okres obowiązywania, suma gwarancyjna),
• ważność OCP,
• ewentualne ograniczenia odpowiedzialności.

## 🚩 CZERWONE FLAGI

Wypisz maksymalnie 5 najważniejszych czerwonych flag.

Nie opisuj szczegółowo dokumentów. Nie powtarzaj informacji. Odpowiadaj wyłącznie w punktach.

Jeżeli któregoś dokumentu brakuje (np. licencji transportowej), wskaż to jako czerwoną flagę.

Nie zakładaj istnienia dokumentów, których nie otrzymałeś.
"""
        }
    )

    print("Rozpoczynam analizę AI...")

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    print("Analiza zakończona.")

    return response.output_text