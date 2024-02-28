package bceao.application.bean.business.report.sfm;

import java.util.HashMap;
import java.util.Map;

//import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import bceao.application.edition.ConstanteStatut;
import bceao.commun.service.impl.provider.GenericProvider;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.data.JRBeanCollectionDataSource;

@Component("sfmProvider")
public class SfmProvider extends GenericProvider<BasicFields, SfmRequestParameters> {

    private static Logger logger = Logger.getLogger(SfmProvider.class);

    @Autowired
    private SfmHelper sfmHelpers;

    @Override
    public Class<SfmRequestParameters> getParamBeanClass() {
        return SfmRequestParameters.class;
    }

    @Override
    public void reportDataProducer(SfmRequestParameters requestParameters) {
        try {

            /* main report */       
            Map<String, Object> templateParameters = new HashMap<>(); // parameter to be passed to the main report template            
            // todo: add static paremeters to the report. for example: templateParameters.put("report_title","Sample reports");
            
            List<BasicFields> templateFieldsList = sfmHelper.getBasicFields(); // todo: takes value of list to display in the tables body and must match the fields of the template.

            /* subreports processing */
            String JASPERSUBREPORTPATHS = Constantes.EDITION_MAQUETTE_PATH; // path to the subreport templates
            
JasperReport sfmTableOnePartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_one_part_two.jrxml"); // specify the subreport template
List <BasicFields> sfmTableOnePartTwoFieldsList = sfmHelper.getBasicFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableOnePartTwoSubreport", sfmTableOnePartTwoSubreport); 
templateParameters.put("sfmTableOnePartTwoDataSource", new JRBeanCollectionDataSource(sfmTableOnePartTwoFieldsList)); 



JasperReport sfmTableTwoPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_two_part_one.jrxml"); // specify the subreport template
List <BasicFields> sfmTableTwoPartOneFieldsList = sfmHelper.getBasicFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableTwoPartOneSubreport", sfmTableTwoPartOneSubreport); 
templateParameters.put("sfmTableTwoPartOneDataSource", new JRBeanCollectionDataSource(sfmTableTwoPartOneFieldsList)); 



JasperReport sfmTableThreePartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_three_part_one.jrxml"); // specify the subreport template
List <BasicFields> sfmTableThreePartOneFieldsList = sfmHelper.getBasicFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableThreePartOneSubreport", sfmTableThreePartOneSubreport); 
templateParameters.put("sfmTableThreePartOneDataSource", new JRBeanCollectionDataSource(sfmTableThreePartOneFieldsList)); 



JasperReport sfmTableFourPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_four_part_one.jrxml"); // specify the subreport template
List <AdvancedFields> sfmTableFourPartOneFieldsList = sfmHelper.getAdvancedFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableFourPartOneSubreport", sfmTableFourPartOneSubreport); 
templateParameters.put("sfmTableFourPartOneDataSource", new JRBeanCollectionDataSource(sfmTableFourPartOneFieldsList)); 



JasperReport sfmTableFivePartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_five_part_one.jrxml"); // specify the subreport template
List <AdvancedFields> sfmTableFivePartOneFieldsList = sfmHelper.getAdvancedFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableFivePartOneSubreport", sfmTableFivePartOneSubreport); 
templateParameters.put("sfmTableFivePartOneDataSource", new JRBeanCollectionDataSource(sfmTableFivePartOneFieldsList)); 



JasperReport sfmTableFivePartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_five_part_two.jrxml"); // specify the subreport template
List <AdvancedFields> sfmTableFivePartTwoFieldsList = sfmHelper.getAdvancedFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableFivePartTwoSubreport", sfmTableFivePartTwoSubreport); 
templateParameters.put("sfmTableFivePartTwoDataSource", new JRBeanCollectionDataSource(sfmTableFivePartTwoFieldsList)); 



JasperReport sfmTableSixPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_six_part_one.jrxml"); // specify the subreport template
List <AdvancedFields> sfmTableSixPartOneFieldsList = sfmHelper.getAdvancedFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableSixPartOneSubreport", sfmTableSixPartOneSubreport); 
templateParameters.put("sfmTableSixPartOneDataSource", new JRBeanCollectionDataSource(sfmTableSixPartOneFieldsList)); 



JasperReport sfmTableSixPartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_six_part_two.jrxml"); // specify the subreport template
List <AdvancedFields> sfmTableSixPartTwoFieldsList = sfmHelper.getAdvancedFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableSixPartTwoSubreport", sfmTableSixPartTwoSubreport); 
templateParameters.put("sfmTableSixPartTwoDataSource", new JRBeanCollectionDataSource(sfmTableSixPartTwoFieldsList)); 



JasperReport sfmTableSevenPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "sfm_table_seven_part_one.jrxml"); // specify the subreport template
List <BasicFields> sfmTableSevenPartOneFieldsList = sfmHelper.getBasicFields(); // todo: update parameter signature. list of fields to be passed to the subreport template
templateParameters.put("sfmTableSevenPartOneSubreport", sfmTableSevenPartOneSubreport); 
templateParameters.put("sfmTableSevenPartOneDataSource", new JRBeanCollectionDataSource(sfmTableSevenPartOneFieldsList)); 




            /* feed request paramaters and fields to the main template */
            setDs(templateFieldsList);
            setReportParams(templateParameters);

        } catch (Exception e) {
            logger.error("Erreur dans le provider : " + e);
        }
    }

}

