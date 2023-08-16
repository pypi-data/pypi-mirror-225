
from IPython.core.magic import register_cell_magic
from IPython.display import HTML
import re
from saspy.SASLogLexer import SASLogStyle, SASLogLexer
from saspy.sasbase import SASsession
from pygments.formatters import HtmlFormatter
from pygments import highlight
import warnings

def SASMagic(sas, sys='viya') :
    warnings.filterwarnings('ignore',module='saspy')
    
    if sys == 'viya' :
        sas.submit("""
        proc template;
          define style Styles.Hangul;
          parent = Styles.HTMLBlue;
          style graphfonts from graphfonts /
                'NodeDetailFont' = ("Noto Sans KR",7pt)
                'NodeInputLabelFont' = ("Noto Sans KR",9pt)
                'NodeLabelFont' = ("Noto Sans KR",9pt)
                'NodeTitleFont' = ("Noto Sans KR",9pt)
                'GraphDataFont' = ("Noto Sans KR",7pt)
                'GraphUnicodeFont' = ("Noto Sans KR",9pt)
                'GraphValueFont' = ("Noto Sans KR",9pt)
                'GraphLabel2Font' = ("Noto Sans KR",10pt)
                'GraphLabelFont' = ("Noto Sans KR",10pt)
                'GraphFootnoteFont' = ("Noto Sans KR",10pt)
                'GraphTitleFont' = ("Noto Sans KR",11pt,bold)
                'GraphTitle1Font' = ("Noto Sans KR",14pt,bold)
                'GraphAnnoFont' = ("Noto Sans KR",10pt);         
          end;
        run;
        """)
        sas.HTML_Style = "Hangul"
        sas.submit("""
        filename storage FILESRVC folderpath='/Public/'; 
        %include storage(sas7bdat, KOSIS_MACRO_V3_5, ecos, enara, localfinance, POSTDATA, ECOS3D); 
        %LET MARKER=MARKERS MARKERATTRS=(SYMBOL=CIRCLEFILLED SIZE=11); 
        %LET DATALABEL=DATALABEL DATALABELATTRS=(SIZE=11); 
        %LET printit=%str(proc print data=raw(obs=3);run;); 
        %LET xaxis=xaxis type=discrete valueattrs=(size=10.5) labelattrs=(size=10.5) display=(nolabel); 
        %LET yaxis=yaxis grid valueattrs=(size=10.5) labelattrs=(size=10.5) labelpos=top;         
        cas casauto; 
        caslib _all_ assign; 
        options dlcreatedir; 
        options casdatalimit=all;
        caslib c datasource=(srctype="path") path="/home/&sysuserid/casuser" sessref=casauto;
        LIBNAME ASOS './public/';
        ods graphics/imagemap;
        """)
        print("알림 : KOSIS_MACRO_V3_5, ECOS, ECOS3, ENARA, POSTDATA, MODIFY_DATA, LOCALFINANCE, SAS7BDAT 매크로를 로드하였습니다.")
        print("알림 : 매크로 변수 MARKER, DATALABEL, PRINTIT, XAXIS, YAXIS를 로드하였습니다.")
        print("알림 : 모든 CAS 라이브러리를 로드하였습니다. ODS GRAPHICS IMAGEMAP 옵션을 로드하였습니다.")
        print("알림 : Jupyter Notebook Cell Magic %%SASK를 로드하였습니다.")
        
        
    if sys == 'oda' :
        sas.submit("""
        proc template;
          define style Styles.Hangul;
          parent = Styles.HTMLBlue;
          style graphfonts from graphfonts /
                'NodeDetailFont' = ("Gulim",7pt)
                'NodeInputLabelFont' = ("Gulim",9pt)
                'NodeLabelFont' = ("Gulim",9pt)
                'NodeTitleFont' = ("Gulim",9pt)
                'GraphDataFont' = ("Gulim",7pt)
                'GraphUnicodeFont' = ("Gulim",9pt)
                'GraphValueFont' = ("Gulim",9pt)
                'GraphLabel2Font' = ("Gulim",10pt)
                'GraphLabelFont' = ("Gulim",10pt)
                'GraphFootnoteFont' = ("Gulim",10pt)
                'GraphTitleFont' = ("Gulim",11pt,bold)
                'GraphTitle1Font' = ("Gulim",14pt,bold)
                'GraphAnnoFont' = ("Gulim",10pt);         
          end;
        run;
        """)
        sas.HTML_Style = "Hangul"
        sas.submit("""
        options validvarname=any;
        
        %let temp=%sysfunc(getoption(work));
        filename kosis "&temp/MACROS.sas";
        proc http url="https://www.googleapis.com/drive/v3/files/15L96rVErDU10g9o-U-8LnLo9XtvZjWmz?alt=media&key=AIzaSyBfJIzuu9x7AZjgtr0UhbrxNTz0vqbYWv0" method='GET' out=kosis;
        run;
        %include "&temp/MACROS.sas";
        %symdel temp;
                       
        %LET MARKER=MARKERS MARKERATTRS=(SYMBOL=CIRCLEFILLED SIZE=11); 
        %LET DATALABEL=DATALABEL DATALABELATTRS=(SIZE=11); 
        %LET printit=%str(proc print data=raw(obs=3);run;); 
        %LET xaxis=xaxis type=discrete valueattrs=(size=10.5) labelattrs=(size=10.5) display=(nolabel); 
        %LET yaxis=yaxis grid valueattrs=(size=10.5) labelattrs=(size=10.5) labelpos=top;
        ods graphics/imagemap;
        """)
        print("알림 : KOSIS_MACRO_V3_5, ECOS, ECOS3, ENARA, POSTDATA, MODIFY_DATA, LOCALFINANCE, SAS7BDAT 매크로를 로드하였습니다.")
        print("알림 : 매크로 변수 MARKER, DATALABEL, PRINTIT, XAXIS, YAXIS를 로드하였습니다.")
        print("알림 : ODS GRAPHICS IMAGEMAP 옵션을 로드하였습니다.")
        print("알림 : Jupyter Notebook Cell Magic %%SASK를 로드하였습니다.")        
            
    def _which_display(sas, log, output):
      lst_len = 30762
      lines = re.split(r'[\n]\s*', log)
      i = 0
      elog = []
      for line in lines:
          i += 1
          e = []
          if line[sas.logoffset:].startswith('ERROR'):
              e = lines[(max(i - 15, 0)):(min(i + 16, len(lines)))]
          elog = elog + e
      if len(elog) == 0 and len(output) > lst_len:   # no error and LST output
          return HTML(output)
      elif len(elog) == 0 and len(output) <= lst_len:   # no error and no LST
          color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
          return HTML(color_log)
      elif len(elog) > 0 and len(output) <= lst_len:   # error and no LST
          color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
          return HTML(color_log)
      else:   # errors and LST
          color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
          return HTML(color_log + output)

    @register_cell_magic
    def SASK(line, cell):
        sas.submit("proc optsave out=__jupyterSASKernel__; run;")
        if len(line) > 0 :
            res = sas.submit("ods layout gridded columns=" + str(line) + " advance=table;" + cell + "ods layout end;")
        else :
            res = sas.submit(cell)        
        dis = _which_display(sas, res['LOG'], res['LST'])
        sas.submit("proc optload data=__jupyterSASKernel__; run;")
        return dis

    warnings.filterwarnings('default')