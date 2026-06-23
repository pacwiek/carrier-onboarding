import requests


def get_krs_company_data(krs):

    url = (
        f"https://api-krs.ms.gov.pl/api/krs/"
        f"OdpisAktualny/{krs}"
        f"?rejestr=P&format=json"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return {
            "error": "KRS API ERROR",
            "status_code": response.status_code
        }

    data = response.json()

    podmiot = (
        data["odpis"]
        ["dane"]
        ["dzial1"]
        ["danePodmiotu"]
    )

    identyfikatory = podmiot.get(
        "identyfikatory",
        {}
    )

    return {
        "krs": data["odpis"]["naglowekA"]["numerKRS"],
        "nip": identyfikatory.get("nip"),
        "regon": identyfikatory.get("regon"),
        "company_name": podmiot.get("nazwa"),
        "legal_form": podmiot.get("formaPrawna")
    }

def get_company_by_nip(nip):

    return {
        "message": "not implemented yet",
        "nip": nip
    }