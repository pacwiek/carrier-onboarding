from company_classifier import classify


async def get_company_data(
    country: str,
    tax_id: str
):

    classification = await classify(
        country,
        tax_id
    )

    return classification