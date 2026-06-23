from bir_client import BirClient
import xml.etree.ElementTree as ET


def xml_to_dict(xml_string: str):

    root = ET.fromstring(xml_string)

    dane = root.find("dane")

    if dane is None:
        return None

    result = {}

    for child in dane:
        result[child.tag] = child.text

    return result


async def get_company_data(nip: str):

    # Nowy klient dla każdego zapytania
    client = BirClient()

    client.login()

    try:

        result_xml = client.search_by_nip(nip)

        if not result_xml:

            return {
                "company_name": None,
                "regon": None,
                "legal_form": None,
                "silos_id": None,
                "forma_prawna": None
            }

        company = xml_to_dict(result_xml)

        if company is None:

            return {
                "company_name": None,
                "regon": None,
                "legal_form": None,
                "silos_id": None,
                "forma_prawna": None
            }

        regon = company.get("Regon")
        typ = company.get("Typ")
        silos = company.get("SilosID")
        nazwa = company.get("Nazwa")

        forma_prawna = None

        try:

            if typ == "P":

                report_xml = client.get_report(
                    regon,
                    "BIR11OsPrawna"
                )

                report = xml_to_dict(report_xml)

                if report:

                    forma_prawna = report.get(
                        "praw_szczegolnaFormaPrawna_Nazwa"
                    )

            elif typ == "F":

                report_xml = client.get_report(
                    regon,
                    "BIR11OsFizycznaDaneOgolne"
                )

                report = xml_to_dict(report_xml)

                if report:

                    forma_prawna = report.get(
                        "fiz_formaPrawna"
                    )

        except Exception as e:

            print("BŁĄD RAPORTU:", e)

        return {
            "company_name": nazwa,
            "regon": regon,
            "legal_form": typ,
            "silos_id": silos,
            "forma_prawna": forma_prawna
        }

    finally:

        try:
            client.logout()
        except Exception:
            pass