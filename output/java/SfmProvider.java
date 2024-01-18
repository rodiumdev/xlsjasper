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
public class SfmProvider extends GenericProvider<SfmSimpleFields, SfmRequestParameters> {

    private static Logger logger = Logger.getLogger(SfmProvider.class);

    @Override
    public Class<SfmRequestParameters> getParamBeanClass() {
        return SfmRequestParameters.class;
    }

    @Override
    public void reportDataProducer(SfmRequestParameters requestParameters) {
        try {
            
            Map<String, Object> templateParameters = new HashMap<>(); // parameter to be passed to the main report template            
            String JASPERSUBREPORTPATHS = Constantes.EDITION_MAQUETTE_PATH; // path to the subreport templates

            /* you can add static paremeters of the report here an example is given below */             
            templateParameters.put("report_title","Sample reports");
            
            List<SfmSimpleFields> templateFieldsList = new ArrayList<>(); // [todo] takes value of list to displayed in the tables body and must match the fields of the template.

            /* case for subreports */
            
JasperReport sfmTableOnePartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableOnePartTwo.jrxml"); // specify the subreport template
List <SfmSimpleFields> sfmTableOnePartTwoFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableOnePartTwoSubreport", sfmTableOnePartTwoSubreport); 
templateParameters.put("sfmTableOnePartTwoSubreportSource", new JRBeanCollectionDataSource(sfmTableOnePartTwoFieldsList)); 



JasperReport sfmTableTwoPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableTwoPartOne.jrxml"); // specify the subreport template
List <SfmSimpleFields> sfmTableTwoPartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableTwoPartOneSubreport", sfmTableTwoPartOneSubreport); 
templateParameters.put("sfmTableTwoPartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableTwoPartOneFieldsList)); 



JasperReport sfmTableThreePartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableThreePartOne.jrxml"); // specify the subreport template
List <SfmSimpleFields> sfmTableThreePartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableThreePartOneSubreport", sfmTableThreePartOneSubreport); 
templateParameters.put("sfmTableThreePartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableThreePartOneFieldsList)); 



JasperReport sfmTableFourPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableFourPartOne.jrxml"); // specify the subreport template
List <SfmComplexFields> sfmTableFourPartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableFourPartOneSubreport", sfmTableFourPartOneSubreport); 
templateParameters.put("sfmTableFourPartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableFourPartOneFieldsList)); 



JasperReport sfmTableFivePartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableFivePartOne.jrxml"); // specify the subreport template
List <SfmComplexFields> sfmTableFivePartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableFivePartOneSubreport", sfmTableFivePartOneSubreport); 
templateParameters.put("sfmTableFivePartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableFivePartOneFieldsList)); 



JasperReport sfmTableFivePartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableFivePartTwo.jrxml"); // specify the subreport template
List <SfmComplexFields> sfmTableFivePartTwoFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableFivePartTwoSubreport", sfmTableFivePartTwoSubreport); 
templateParameters.put("sfmTableFivePartTwoSubreportSource", new JRBeanCollectionDataSource(sfmTableFivePartTwoFieldsList)); 



JasperReport sfmTableSixPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableSixPartOne.jrxml"); // specify the subreport template
List <SfmComplexFields> sfmTableSixPartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableSixPartOneSubreport", sfmTableSixPartOneSubreport); 
templateParameters.put("sfmTableSixPartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableSixPartOneFieldsList)); 



JasperReport sfmTableSixPartTwoSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableSixPartTwo.jrxml"); // specify the subreport template
List <SfmComplexFields> sfmTableSixPartTwoFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableSixPartTwoSubreport", sfmTableSixPartTwoSubreport); 
templateParameters.put("sfmTableSixPartTwoSubreportSource", new JRBeanCollectionDataSource(sfmTableSixPartTwoFieldsList)); 



JasperReport sfmTableSevenPartOneSubreport = GenerateurJasperReport.getPdfJasperReport(JASPERSUBREPORTPATHS, "SfmTableSevenPartOne.jrxml"); // specify the subreport template
List <SfmSimpleFields> sfmTableSevenPartOneFieldsList = new ArrayList<>(); // [todo] list of fields to be passed to the subreport one template can be from a service
templateParameters.put("sfmTableSevenPartOneSubreport", sfmTableSevenPartOneSubreport); 
templateParameters.put("sfmTableSevenPartOneSubreportSource", new JRBeanCollectionDataSource(sfmTableSevenPartOneFieldsList)); 




            /* feed fields and paramaters to the main template */
            setDs(templateFieldsList);
            setReportParams(templateParameters);

        } catch (Exception e) {
            logger.error("Erreur dans le provider : " + e);
        }
    }

}

