import asyncio
import traceback

from company_classifier import classify

from ceidg_service import (
    download_ceidg_pdf
)

from ceidg_sc_service import (
    download_ceidg_sc_pdfs
)

from krs_pdf_service import (
    download_krs_pdf
)

from regon_pdf_service import (
    download_regon_pdf
)

from vies_runner import (
    download_vies_pdf
)


async def get_company_pdf(
    country: str,
    tax_id: str
):

    try:

        classification = await classify(
            country,
            tax_id
        )

    except Exception:

        traceback.print_exc()

        return {
            "entity_type": "UNKNOWN",
            "pdf_path": None
        }


    entity_type = classification[
        "entity_type"
    ]

    company_name = classification.get(
        "company_name"
    )

    print("ENTITY:", entity_type)
    print("NAME:", company_name)

    #
    # JDG
    #

    if entity_type == "JDG":

        pdf_path = await asyncio.to_thread(
            download_ceidg_pdf,
            tax_id,
            company_name
        )

        regon_pdf_path = None

        try:

            regon_pdf_path = await asyncio.to_thread(
                download_regon_pdf,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        vies_pdf_path = None

        try:

            vies_pdf_path = await asyncio.to_thread(
                download_vies_pdf,
                country,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        return {
            "entity_type": entity_type,
            "pdf_path": pdf_path,
            "regon_pdf_path": regon_pdf_path,
            "vies_pdf_path": vies_pdf_path
        }

    #
    # SPÓŁKA CYWILNA
    #

    if entity_type == "SC":

        pdf_files = await asyncio.to_thread(
            download_ceidg_sc_pdfs,
            tax_id,
            company_name
        )

        regon_pdf_path = None

        try:

            regon_pdf_path = await asyncio.to_thread(
                download_regon_pdf,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        vies_pdf_path = None

        try:

            vies_pdf_path = await asyncio.to_thread(
                download_vies_pdf,
                country,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        return {
            "entity_type": entity_type,
            "pdf_path": pdf_files[0]
            if pdf_files else None,
            "pdf_files": pdf_files,
            "regon_pdf_path": regon_pdf_path,
            "vies_pdf_path": vies_pdf_path
        }

    #
    # KRS
    #

    if entity_type in [
        "SP_ZOO",
        "SP_K",
        "SP_J",
        "SA",
        "LEGAL_ENTITY",
        "FUNDACJA",
        "STOWARZYSZENIE"
    ]:

        pdf_path = await asyncio.to_thread(
            download_krs_pdf,
            tax_id,
            company_name
        )

        regon_pdf_path = None

        try:

            regon_pdf_path = await asyncio.to_thread(
                download_regon_pdf,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        vies_pdf_path = None

        try:

            vies_pdf_path = await asyncio.to_thread(
                download_vies_pdf,
                country,
                tax_id,
                company_name
            )

        except Exception:

            traceback.print_exc()

        return {
            "entity_type": entity_type,
            "pdf_path": pdf_path,
            "regon_pdf_path": regon_pdf_path,
            "vies_pdf_path": vies_pdf_path
        }

    return {
        "entity_type": entity_type,
        "pdf_path": None
    }