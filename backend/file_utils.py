from pathlib import Path
import re


def safe_name(name: str):

    return re.sub(
        r'[<>:"/\\|?*]',
        "_",
        name
    )


def get_company_folder(
    nip: str,
    company_name: str
):

    downloads_dir = (
        Path.home()
        / "Downloads"
        / "Przewoznicy"
    )

    folder_name = (
        f"{nip}_{safe_name(company_name)}"
    )

    company_dir = (
        downloads_dir
        / folder_name
    )

    company_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return company_dir