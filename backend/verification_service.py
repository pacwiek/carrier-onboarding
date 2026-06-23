from pathlib import Path
import shutil
import extract_msg
import os
import zipfile

from PIL import Image


def save_uploaded_files(files, folder: str):

    target = Path(folder)

    target.mkdir(parents=True, exist_ok=True)

    saved = []

    for file in files:

        destination = target / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved.append(file.filename)

    return saved

from pathlib import Path
from PIL import Image


def convert_images_to_pdf(folder: str):

    folder = Path(folder)

    for extension in ("*.jpg", "*.jpeg", "*.png"):

        for image_path in folder.glob(extension):

            pdf_path = image_path.with_suffix(".pdf")

            # Jeżeli PDF już istnieje, usuwamy obraz i przechodzimy dalej
            if pdf_path.exists():

                image_path.unlink()

                continue

            try:

                image = Image.open(image_path)

                if image.mode != "RGB":
                    image = image.convert("RGB")

                image.save(pdf_path, "PDF")

                image.close()

                if pdf_path.exists():

                    image_path.unlink()

                    print(f"Przekonwertowano: {image_path.name} -> {pdf_path.name}")

            except Exception as error:

                print(f"Błąd konwersji {image_path.name}: {error}")

def extract_msg_attachments(folder: str):

    folder = Path(folder)

    for msg_path in folder.glob("*.msg"):

        print(f"MSG: {msg_path}")

        try:

            msg = extract_msg.Message(str(msg_path))

            print(f"Liczba załączników: {len(msg.attachments)}")

            for attachment in msg.attachments:

                filename = attachment.getFilename()

                print("ZAŁĄCZNIK:", filename)

                if not filename:
                    continue

                # Pomijamy obrazki ze stopki Outlook
                if filename.lower().startswith("image"):
                    continue

                attachment.save(customPath=str(folder))

                saved_file = folder / filename

                # Usuwamy małe obrazki (logo, stopki Outlook)
                if (
                    saved_file.exists()
                    and saved_file.suffix.lower() in (".png", ".jpg", ".jpeg")
                    and saved_file.stat().st_size < 20480
                ):
                    print("Usuwam mały obrazek:", filename)
                    saved_file.unlink()

            msg.close()

        except Exception as error:

            print(error)

def collect_msg_attachments(folder: str):

    folder = Path(folder)

    allowed_extensions = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".zip",
        ".msg"
    }

    for item in folder.iterdir():

        if not item.is_dir():
            continue

        for root, _, files in os.walk(item):

            for file in files:

                source = Path(root) / file

                if source.suffix.lower() not in allowed_extensions:
                    continue

                destination = folder / source.name

                if destination.exists():
                    continue

                shutil.move(str(source), str(destination))

        shutil.rmtree(item, ignore_errors=True)

def extract_zip_files(folder: str):

    folder = Path(folder)

    for zip_path in folder.glob("*.zip"):

        print(f"ZIP: {zip_path.name}")

        try:

            with zipfile.ZipFile(zip_path, "r") as zip_ref:

                zip_ref.extractall(folder)

            print("Rozpakowano:", zip_path.name)

            # Usuwamy ZIP po poprawnym rozpakowaniu
            zip_path.unlink()

        except Exception as error:

            print(error)

def flatten_zip_folders(folder: str):

    folder = Path(folder)

    for item in folder.iterdir():

        if not item.is_dir():
            continue

        # Przenosimy wszystkie pliki z podfolderów
        for file in item.rglob("*"):

            if not file.is_file():
                continue

            destination = folder / file.name

            if destination.exists():
                continue

            shutil.move(str(file), str(destination))

        # Usuwamy pusty folder
        shutil.rmtree(item, ignore_errors=True)

def normalize_file_extensions(folder: str):

    folder = Path(folder)

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix != file.suffix.lower():

            new_name = file.stem + file.suffix.lower()
            new_path = file.with_name(new_name)

            print(f"Zmieniono: {file.name} -> {new_path.name}")

            file.rename(new_path)

def cleanup_folder(folder: str):

    folder = Path(folder)

    normalize_file_extensions(folder)

    # Usuwamy puste katalogi
    for item in folder.rglob("*"):

        if item.is_dir():

            try:
                item.rmdir()
            except OSError:
                pass

    # Usuwamy wszystkie wiadomości MSG
    for msg in folder.glob("*.msg"):

        try:
            msg.unlink()
            print("Usunięto:", msg.name)
        except Exception as error:
            print(error)