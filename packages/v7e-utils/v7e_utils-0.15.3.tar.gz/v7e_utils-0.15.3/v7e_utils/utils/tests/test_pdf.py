from django.test import TestCase
from ..pdf import Job, PfdParameters


class UtilsPdfTestCase(TestCase):
    def test_job_pdf_ftp(self):
        parameters = PfdParameters(
            ftp_output_path="/home/system/docker/nextcloud/data/istmocenter/files/Reports/PDFs/contrato",
            report_unit_uri="/PDFs/contrato_definido/contrato_definido",
            output_file_name="test_estifito",
            parameters={
                "OwnerName": "ISTMO CENTER POP! SOCIEDAD ANONIMA",
                "OwnerIdentification": "1-14710-009",
                "LegalRepresentativeIdentification": "1-14710-009",
                "EmployeePosition": "San Jose, Goicoechea, Calle Blancos",
                "LegalRepresentativeLocation": "Cartago dentro",
                "TimesMarried": "1",
                "OwnerLocation": "San José, San Pedro, Montes de Oca",
                "EmployeeLocation": "Formalizador Temporal",
                "BusinessUnitLocation": "an José, San Pedro, Montes de oca Mall, quinto piso del Office Mall",
                "SalarySpell": "docientos mil",
                "BeginEmployment": "26 de diciembre",
                "LegalRepresentativeName": "Jorge Ugarte Garro",
                "EndEmployment": "1 de enero del 2023",
                "EmployeeSalary": "330 299",
                "EmployeeIdentification": "113540596",
                "EmployeeName": "David Gerardo Vargas Esquivel",
                "Journey": "Diurno"
            }
        )
        job = Job(config_parameters=parameters)
        response = job.generate_pdf_ftp_now()
        self.assertIn(response.status_code, [200])
