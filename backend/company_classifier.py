from regon_service import get_company_data


async def classify(
    country: str,
    tax_id: str
):

    country = country.strip().upper()
    tax_id = tax_id.strip()

    result = {
        "country": country,
        "tax_id": tax_id,
        "source": None,
        "entity_type": None
    }

    if country != "PL":

        result["source"] = "NOT_SUPPORTED"
        result["entity_type"] = "UNKNOWN"

        return result

    company_data = await get_company_data(
        tax_id
    )

    legal_form = company_data["legal_form"]

    forma_prawna = (
        company_data.get("forma_prawna") or ""
    ).upper()

    print("FORMA PRAWNA:", forma_prawna)

    if legal_form == "F":

        result["source"] = "CEIDG"

        if "CYWILN" in forma_prawna:

            result["entity_type"] = "SC"

        else:

            result["entity_type"] = "JDG"

    elif legal_form == "P":

        result["source"] = "KRS"

        if "OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ" in forma_prawna:

            result["entity_type"] = "SP_ZOO"

        elif "CYWILN" in forma_prawna:

            result["source"] = "CEIDG"
            result["entity_type"] = "SC"

        elif "KOMANDYTOW" in forma_prawna:

            result["entity_type"] = "SP_K"

        elif "JAWN" in forma_prawna:

            result["entity_type"] = "SP_J"

        elif "AKCYJN" in forma_prawna:

            result["entity_type"] = "SA"

        elif "FUNDACJ" in forma_prawna:

            result["entity_type"] = "FUNDACJA"

        elif "STOWARZYSZEN" in forma_prawna:

            result["entity_type"] = "STOWARZYSZENIE"

        else:

            result["entity_type"] = "LEGAL_ENTITY"

    else:

        result["source"] = "UNKNOWN"
        result["entity_type"] = "UNKNOWN"

    result["company_name"] = company_data["company_name"]
    result["regon"] = company_data["regon"]
    result["forma_prawna"] = company_data["forma_prawna"]

    return result