from zeep import Client
import xml.etree.ElementTree as ET

WSDL_URL = (
    "https://wyszukiwarkaregon.stat.gov.pl/"
    "wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl"
)

API_KEY = "d940cd8e003c462cadda"


async def get_company_data(nip: str):

    client = Client(WSDL_URL)

    print(client.service)

    sid = client.service.Zaloguj(
        API_KEY
    )

    print("SID:", sid)

    client.transport.session.headers.update({
        "sid": sid
    })

    result = client.service.DaneSzukaj({
        "Nip": nip
    })

    print("RESULT:")
    print(result)

    if not result:

        return {
            "company_name": None,
            "regon": None,
            "legal_form": None,
            "silos_id": None,
            "forma_prawna": None
        }

    root = ET.fromstring(result)

    dane = root.find("dane")

    if dane is None:

        return {
            "company_name": None,
            "regon": None,
            "legal_form": None,
            "silos_id": None,
            "forma_prawna": None
        }

    nazwa = dane.findtext("Nazwa")
    regon = dane.findtext("Regon")
    typ = dane.findtext("Typ")
    silos_id = dane.findtext("SilosID")

    forma_prawna = None

    try:

        if typ == "P":

            full_report = (
                client.service
                .DanePobierzPelnyRaport(
                    regon,
                    "DaneRaportPrawnaPubl"
                )
            )

            full_root = ET.fromstring(
                full_report
            )

            full_dane = full_root.find(
                "dane"
            )

            if full_dane is not None:

                forma_prawna = (
                    full_dane.findtext(
                        "praw_nazwaSzczegolnejFormyPrawnej"
                    )
                )

                print(
                    "FORMA PRAWNA:",
                    forma_prawna
                )

    except Exception as e:

        print(
            "BLAD FULL REPORT:",
            str(e)
        )

    print("SILOS:", silos_id)
    print("NAZWA:", nazwa)
    print("REGON:", regon)
    print("TYP:", typ)

    return {
        "company_name": nazwa,
        "regon": regon,
        "legal_form": typ,
        "silos_id": silos_id,
        "forma_prawna": forma_prawna
    }