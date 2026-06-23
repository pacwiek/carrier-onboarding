import asyncio

from file_utils import (
    get_company_folder,
    safe_name
)

from vies_service import ViesService


def download_vies_pdf(
    country: str,
    vat_number: str,
    company_name: str
):

    print("VIES START")

    company_dir = get_company_folder(
        vat_number,
        company_name
    )

    pdf_path = (
        company_dir
        / f"{safe_name(company_name)}_VIES.pdf"
    )

    print("VIES PATH:", pdf_path)

    service = ViesService()

    asyncio.run(
        service.download_vies_pdf(
            country,
            vat_number,
            str(pdf_path)
        )
    )

    print("VIES END")

    return str(pdf_path)