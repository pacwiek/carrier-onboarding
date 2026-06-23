from zeep import Client

WSDL_URL = (
    "https://wyszukiwarkaregon.stat.gov.pl/"
    "wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl"
)

API_KEY = "d940cd8e003c462cadda"


class BirClient:

    def __init__(self):
        self.client = Client(WSDL_URL)
        self.sid = None

    def login(self):

        self.sid = self.client.service.Zaloguj(API_KEY)

        self.client.transport.session.headers.update({
            "sid": self.sid
        })

        return self.sid

    def logout(self):

        if self.sid:

            try:
                self.client.service.Wyloguj(
                    self.sid
                )
            except:
                pass

    def search_by_nip(self, nip):

        return self.client.service.DaneSzukajPodmioty(
            {
                "Nip": nip
            }
        )

    def search_by_regon(self, regon):

        return self.client.service.DaneSzukajPodmioty(
            {
                "Regon": regon
            }
        )

    def search_by_krs(self, krs):

        return self.client.service.DaneSzukajPodmioty(
            {
                "Krs": krs
            }
        )

    def get_report(
        self,
        regon,
        report_name
    ):

        return self.client.service.DanePobierzPelnyRaport(
            regon,
            report_name
        )

    def get_value(
        self,
        name
    ):

        return self.client.service.GetValue(
            name
        )