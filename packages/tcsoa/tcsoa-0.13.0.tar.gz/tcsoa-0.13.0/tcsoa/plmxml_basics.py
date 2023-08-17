import os
from typing import List, Optional

from tcsoa.basics import TcSoaBasics
from tcsoa.fcc.file_management_utility import FileManagementUtility
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2007_01.FileManagement import TransientFileInfo
from tcsoa.gen.Core.services import FileManagementService
from tcsoa.gen.GlobalMultiSite._2007_06.ImportExport import GetPLMXMLRuleInputData
from tcsoa.gen.GlobalMultiSite._2007_12.ImportExport import NamesAndValues
from tcsoa.gen.GlobalMultiSite._2010_04.ImportExport import ImportObjectsFromPLMXMLResponse
from tcsoa.gen.GlobalMultiSite.services import ImportExportService


class TcPlmxmlBasics:
    @classmethod
    def plmxml_export(cls, xml_path: str, obj: BusinessObject, rev_rule: BusinessObject = None, transfer_mode: BusinessObject = None, options: List[NamesAndValues] = ()):
        response = ImportExportService.exportObjectsToPLMXML(
            exportObjects=[obj],
            transfermode=transfer_mode,
            revRule=rev_rule,
            languages=[],
            xmlFileName='',
            sessionOptions=options,
        )
        FileManagementUtility.get_file_by_ticket(response.xmlFileTicket.ticket, xml_path)

    @classmethod
    def plmxml_import(cls, xml_path: str, transfer_mode, options: List[NamesAndValues] = ()) -> ImportObjectsFromPLMXMLResponse:
        transient_response = FileManagementService.getTransientFileTicketsForUpload([
            TransientFileInfo(
                fileName=os.path.basename(xml_path)
            )
        ])
        ticket_info = transient_response.transientFileTicketInfos[0]
        FileManagementUtility.ensure_init()
        FileManagementUtility.fcc.upload_files_to_plm([ticket_info.ticket], [xml_path])
        return ImportExportService.importObjectsFromPLMXML(
            xmlFileTicket=ticket_info.ticket,
            namedRefFileTickets=[],
            transfermode=transfer_mode,
            icRev=None,
            sessionOptions=options,
        )

    @classmethod
    def get_transfer_mode(cls, name: str) -> Optional[BusinessObject]:
        _transfer_mode_cache = getattr(cls, '_transfer_mode_cache', None)
        if _transfer_mode_cache is None:
            TcSoaBasics.set_object_load_policy('TransferMode', ['object_name'])
            get_transfermodes_response = ImportExportService.getTransferModes(
                inputs=GetPLMXMLRuleInputData(
                    scope='EXPORT',
                    schemaFormat='PLMXML'
                )
            )
            transfermodes = list(get_transfermodes_response.serviceData.modelObjects.values())
            _transfer_mode_cache = {t.prop_str('object_name'): t for t in transfermodes}
            setattr(cls, '_transfer_mode_cache', _transfer_mode_cache)
        return _transfer_mode_cache.get(name, None)

    @classmethod
    def get_workflow_template(cls, name: str):
        _workflow_template_cache = getattr(cls, '_workflow_template_cache', None)
        if _workflow_template_cache is None:
            from tcsoa.gen.Workflow.services import WorkflowService
            from tcsoa.gen.Workflow._2013_05.Workflow import GetWorkflowTemplatesInputInfo

            TcSoaBasics.set_object_load_policy('EPMTaskTemplate', ['template_name'])
            get_templates_response = WorkflowService.getWorkflowTemplates2([
                GetWorkflowTemplatesInputInfo(
                    clientId='abc',
                    includeUnderConstruction=True,
                )
            ])
            wfl_templates = get_templates_response.templatesOutput[0].workflowTemplates
            _workflow_template_cache = {i.prop_str('template_name'): i for i in wfl_templates}
            setattr(cls, '_workflow_template_cache', _workflow_template_cache)
        return _workflow_template_cache.get(name, None)