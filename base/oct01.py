import os
import logging
from osgeo import ogr

from Common.helper import get_fields
from Common.ErrorHandler import baseException

# global
EMPTY = ['', ' ', None]

def patchOct01(layer: ogr.Layer):
  '''Applies Oct 01 patch if required'''
  try:
    patch = ['0928', '0929', '0930', '1001', '1002', '1003', '1004']
    fn = layer.GetName()
    date = fn.split('_')[2]

    # check date
    if date[4:] not in patch:
      return
 
    ldefn = layer.GetLayerDefn()
    fields = get_fields(ldefn)

  # loop through layer
    logging.info('running oct01 patch')
    layer.ResetReading()
    for ft in layer:
      if ft.GetField('POLY_TYPE') == 'I':
        # get egg fields
        CT1 = ft.GetField('E_CT')
        CA1 = ft.GetField('E_CA')
        CB1 = ft.GetField('E_CB')
        CC1 = ft.GetField('E_CC')
        CD1 = ft.GetField('E_CD')

        CT1 = '0' if CT1 in EMPTY else CT1
        CA1 = CT1 if CA1 in EMPTY else CA1
        CA1 = '9.7' if CA1 == '9+' else CA1
        CB1 = '0' if CB1 in EMPTY else CB1
        CC1 = '0' if CC1 in EMPTY else CC1
        CD1 = '0' if CD1 in EMPTY else CD1

        SA1 = ft.GetField('SA')
        SB1 = ft.GetField('SB')
        SC1 = ft.GetField('SC')
        CN1 = ft.GetField('CN')
        SigCD = ft.GetField('CD')
        
        FA1 = ft.GetField('FA')
        FB1 = ft.GetField('FB')
        FC1 = ft.GetField('FC')

        CT_tot = float(ft.GetField('N_CT'))

        # e.1) Find the total concentration of any FYI (add all the FYI partial CTs)              
        # Note: Extremely rare to find thin or medium FYI at this time of year (end of melt season) but tracking just in case
        
        concFYI = 0
        concFYI_trace = 0

        concFYI_thk = 0
        concFYI_m = 0
        concFYI_tn = 0
        concFYI_thk_trace = 0
        concFYI_m_trace = 0
        concFYI_tn_trace = 0

        floeFYI = '-9'
        floeFYI_thk = '-9'
        floeFYI_m = '-9'
        floeFYI_tn = '-9'

        # find total concentration of any FYI present
        if SA1 in ['86', '87', '91', '93']:
          concFYI = concFYI + int(round(float(CA1))) 
        if SB1 in ['86', '87', '91', '93']:
          concFYI = concFYI + int(CB1)
        if SC1 in ['86', '87', '91', '93']:
          concFYI = concFYI + int(CC1)

        if CD1 in ['86', '87', '91', '93']:
          if (CT1 == '9+'):
            concCD1 = 10 - (int(round(float(CA1)))+int(CB1)+int(CC1))
          else:
            concCD1 = int(CT1) - (int(round(float(CA1)))+int(CB1)+int(CC1))
          concFYI = concFYI + concCD1
        if CN1 in ['86', '87', '91', '93']:
          concFYI_trace = concFYI_trace + 0.3  #trace is 0.3, open water is 0.2, bergy water is 0.3

        # find total concentration and floe size of any thick FYI present 
        if (SA1 == '93'):
          concFYI_thk = concFYI_thk + int(round(float(CA1)))  
          floeFYI_thk = FA1
        if (SB1 == '93'):
          concFYI_thk = concFYI_thk + int(CB1)
          floeFYI_thk = FB1
        if (SC1 == '93'):
          concFYI_thk = concFYI_thk + int(CC1)
          floeFYI_thk = FC1
        if (CD1 == '93'):
          if (CT1 == '9+'):
            concCD1_thk = 10 - (int(round(float(CA1)))+int(CB1)+int(CC1))
          else:
            concCD1_thk = int(CT1) - (int(round(float(CA1)))+int(CB1)+int(CC1))
          concFYI_thk = concFYI_thk + concCD1_thk
        if (CN1 == '93'):
          concFYI_thk_trace = concFYI_thk_trace + 0.3

        # find total concentration and floe size of any medium FYI present 
        if (SA1 == '91'):
          concFYI_m = concFYI_m + int(round(float(CA1)))  
          floeFYI_m = FA1
        if (SB1 == '91'):
          concFYI_m = concFYI_m + int(CB1)
          floeFYI_m = FB1
        if (SC1 == '91'):
          concFYI_m = concFYI_m + int(CC1)
          floeFYI_m = FC1
        if (CD1 == '91'):
          if (CT1 == '9+'):
            concCD1_m = 10 - (int(round(float(CA1)))+int(CB1)+int(CC1))
          else:
            concCD1_m = int(CT1) - (int(round(float(CA1)))+int(CB1)+int(CC1))
          concFYI_m = concFYI_m + concCD1_m
        if (CN1 == '91'):
          concFYI_m_trace = concFYI_m_trace + 0.3

        # find total concentration and floe size of any thin FYI present (should be 0 at this time of year - end of the melt season)
        if (SA1 == '87'):
          concFYI_tn = concFYI_tn + int(round(float(CA1)))  
          floeFYI_tn = FA1
        if (SB1 == '87'):
          concFYI_tn = concFYI_tn + int(CB1)
          floeFYI_tn = FB1
        if (SC1 == '87'):
          concFYI_tn = concFYI_tn + int(CC1)
          floeFYI_tn = FA1
        if (CD1 == '87'):
          if (CT1 == '9+'):
            concCD1_tn = 10 - (int(round(float(CA1)))+int(CB1)+int(CC1))
          else:
            concCD1_tn = int(CT1) - (int(round(float(CA1)))+int(CB1)+int(CC1))
          concFYI_tn = concFYI_tn + concCD1_tn
        if (CN1 == '87'):
          concFYI_tn_trace = concFYI_tn_trace + 0.3

        # find the predominant floe size for all types of FYI combined
        if (floeFYI_thk == '08') or (floeFYI_m == '08') or (floeFYI_tn == '08'):    
          # Now do this fast ice floe size check at the end (lower down) when setting up the new egg, as FYI might not end up being in right-most column ... 
          # ... if a D column got shifted up to column C ... then that new C column should get floe size 8 if the polygon has fast ice
          # floeFYI = '08'                                                         
          pass
        else:
          if (concFYI_tn > concFYI_m):
            floeFYI = floeFYI_tn if (concFYI_tn > concFYI_thk) else floeFYI_thk
          else:
            floeFYI = floeFYI_m if (concFYI_m > concFYI_thk) else floeFYI_thk             
    
        # e.2) Calculate the concentration of existing OI (should all be 95/7. ice in September ... should not be any 96/8. or 97/9. present in charts originating from before Oct01, but include these as a check)
        concSYI = 0
        concSYI_trace = 0
        concMYI = 0
        concMYI_trace = 0
        concOI = 0
        concOI_trace = 0

        floeSYI = '-9'
        floeMYI = '-9'
        floeOI = '-9'

        # find total concentration and floe size of any OI already present (Note: for raw chart dates before Oct 01, there should only be 95/7. present)
        # dont need to worry about D column for old ice ... should never be old ice in this column
        if (SA1 == '95'): # or (SA1 == '96') or (SA1 == '97'):
          concOI = concOI + int(round(float(CA1)))  
        if (SB1 == '95'): # or (SB1 == '96') or (SB1 == '97'):
          concOI = concOI + int(CB1)   
        if (SC1 == '95'): # or (SC1 == '96') or (SC1 == '97'):
          concOI = concOI + int(CC1)
        if (CN1 == '95'): # or (CN1 == '96') or (CN1 == '97'):
          concOI_trace = concOI_trace + 0.3

        # find floe size for 95/7. ice
        if (SA1 == '95'):
          floeOI = FA1
        if (SB1 == '95'):
          floeOI = FB1
        if (SC1 == '95'):
          floeOI = FC1

        # find total concentration and floe size of any SYI already present (**should be 0** for charts with original dates before Oct01)
        if (SA1 == '96'):
          concSYI = concSYI + int(round(float(CA1)))  
          floeSYI = FA1
        if (SB1 == '96'):
          concSYI = concSYI + int(CB1)
          floeSYI = FB1
        if (SC1 == '96'):
          concSYI = concSYI + int(CC1)
          floeSYI = FC1
        if (CN1 == '96'):
          concSYI_trace = concSYI_trace + 0.3 # this should be 0

        # find total concentration and floe size of any MYI already present (**should be 0** for charts with original dates before Oct01)
        if (SA1 == '97'):
          concMYI = concMYI + int(round(float(CA1)))  
          floeMYI = FA1
        if (SB1 == '97'):
          concMYI = concMYI + int(CB1)
          floeMYI = FB1
        if (SC1 == '97'):
          concMYI = concMYI + int(CC1)
          floeMYI = FC1
        if (CN1 == '97'):
          concMYI_trace = concMYI_trace + 0.3 # this should be 0

        # f) If FYI exists, convert it to MYI; if OI exists, convert it to MYI
        if (CT_tot > 0.3) and ((concFYI > 0) or (concFYI_trace > 0) or (concOI > 0) or (concOI_trace > 0)):  
          # don't need to do rows with just young/new ice or open water (OW) or bergy water (BW)  
          # count_total = count_total + 1

          concSYI_new = 0
          concMYI_new = 0
          concOI_new = 0
          concFYI_new = 0
          
          # g) convert FYI to SYI ... compute new SYI concentrations
          # convert pre-existing OI to MYI ... compute new MYI concentrations
          # compute new total OI concentration = SYI + MYI

          concSYI_new = concSYI + concFYI         # FYI added to (becomes) SYI (ice type 96/8.) 
          concMYI_new = concMYI + concOI          # OI added to (becomes) MYI (ice type 97/9.)
          concOI_new = concSYI_new + concMYI_new  # equivalent to 'concOI_new = concOI + concFYI'    #ice type 95/7. (= 96/8. + 97/9.)

          concFYI_new = 0                         # All FYI concentrations are now 0 (they have all been converted to SYI)
          
          # if total new concentration of SYI / MYI / OI == 0 but traces of FYI / pre-existing OI exist ...
          if (concSYI_new == 0) and (concFYI_trace != 0):
            concSYI_new = concSYI_new + concFYI_trace
          if (concMYI_new == 0) and (concOI_trace != 0):
            concMYI_new = concMYI_new + concOI_trace
          if (concOI_new == 0) and (concOI_trace != 0):
            concOI_new = concOI_new + concOI_trace

          # if total new concentration == 10 but previous total concentration was numeric 9.7 / egg 9+ / sigrid 91 
          # ... then the max total conc = 9.7/9+/91 (can't be 10 as this would indicate fast ice)
          if (concSYI_new == 10) and (CT_tot < 10):
            concSYI_new = 9.7
          if (concMYI_new == 10) and (CT_tot < 10):
            concMYI_new = 9.7
          if (concOI_new == 10) and (CT_tot < 10):
            concOI_new = 9.7
        
          # h) Update the Numeric fields in the dbf file (attribute table) for the new ice types and concentrations
          # Numeric fields are done first because they are easiest ('N_CT','N_COI','N_CMY','N_CSY','N_CFY','N_CFY_TK','N_CFY_M','N_CFY_TN','N_CYI','N_CGW','N_CG','N_CN','N_CB')

          # value for N_CT (row[30]) will stay the same
          # values for N_CYI, N_CGW, N_CG, N_CN, N_CB (row[38] row[39] row[40] row[41] row[42]) will stay the same
          
          # set N_CSY field to concSYI_new, N_CMY field to concMYI_new, N_COI to concOI_new 
          concSYI_newf = float(concSYI_new)
          concMYI_newf = float(concMYI_new)
          concOI_newf = float(concOI_new)
          concFYI_newf = float(concFYI_new)
          ft.SetField('N_COI', str(concOI_newf)) # ... any previous trace amount of OI in this field is subsumed into the new concentration if concentration is > 0
          ft.SetField('N_CMY', str(concMYI_newf)) # ... keep previous trace amounts in this field if new OI total conc is > 0.3?? Or set it to blank in such a case??
          ft.SetField('N_CSY', str(concSYI_newf))
          
          # set N_CFY field to 0.0 (N_CFY_TK, N_CFY_M, N_CFY_TN are set to blanks)
          ft.SetField('N_CFY', '0.0')
          ft.SetField('N_CFY_TK', ' ')
          ft.SetField('N_CFY_M', ' ')
          ft.SetField('N_CFY_TN', ' ')
          
          # i) Before updating the Sigrid and Egg fields in the dbf file (attribute table) for the new ice types / concentrations / floe sizes, need to ...
          # ... first define a new egg based on the new values [there should no longer be any FYI anywhere (should only have MYI,SYI,GW,G,N and bergs)]

          # Note: If there was only thick FYI present originally, then updating the polygon's fields is straightforward, as no Egg column shifts are required. 
          #       **However, if there was more than one category of FYI present, then we need to create a whole new egg as the original egg's columns will shift ...
          #       ... when the separate FYI columns are collapsed into a single SYI column. We then have to update all the attribute table fields according to the new egg column structure.
          #       Steve's original script had a method of doing this that was simpler and worked but which forgot to check for berg concentrations in Egg column A (although he did consider bergs in the Numeric columns).
          #       This script uses a longer but technically more complete method of defining the new egg columns.

          # CA,SA,FA ... bergs or 1st thickest/oldest ice type 
          # CB,SB,FB ... 2nd thickest/oldest ice type
          # CB,SB,FB ... 3rd thickest/oldest ice type

          # i.1) determine the partial concentrations for the different ice types in the new 'egg'
          COI = concOI_newf
          CMY = concMYI_newf
          CSY = concSYI_newf
          CFY = concFYI_newf #This will be 0 now
          CYI = float(ft.GetField('N_CYI'))
          if (ft.GetField('N_CGW') in EMPTY):
            CGW = 0.0
          else:
            CGW = float(ft.GetField('N_CGW'))
          if (ft.GetField('N_CG') in EMPTY):
            CG = 0.0
          else:
            CG = float(ft.GetField('N_CG'))
          if (ft.GetField('N_CN') in EMPTY):
            CN = 0.0
          else:
            CN = float(ft.GetField('N_CN'))
            
          if (ft.GetField('N_CB') in EMPTY):    
            CBerg = 0.0
          else:
            CBerg = float(ft.GetField('N_CB'))

          # i.2) determine the floe sizes for the different ice types in the new 'egg' (Sigrid and Egg code) 
          floeSYI_new = floeFYI
          floeMYI_new = floeOI
          FMY = floeMYI_new
          FSY = floeSYI_new
          if (FMY == '03'):
            EFMY = '3'
          elif (FMY == '04'):
            EFMY = '4'
          elif (FMY == '05'):
            EFMY = '5'
          elif (FMY == '06'):
            EFMY = '6'
          elif (FMY == '07'):
            EFMY = '7'
          elif (FMY == '08'):
            EFMY = '8'
          elif (FMY == '-9'):
            EFMY = ' '
          if (FSY == '03'):
            EFSY = '3'
          elif (FSY == '04'):
            EFSY = '4'
          elif (FSY == '05'):
            EFSY = '5'
          elif (FSY == '06'):
            EFSY = '6'
          elif (FSY == '07'):
            EFSY = '7'
          elif (FSY == '08'):
            EFSY = '8'
          elif (FSY == '-9'):
            EFSY = ' '    
          # find floe size for any grey 84/4 ice
          FG = '-9'
          EFG = ' '
          if (SA1 == '84'):
            FG = FA1
            EFG = ft.GetField('E_FA')
          if (SB1 == '84'):
            FG = FB1
            EFG = ft.GetField('E_FB')
          if (SC1 == '84'):
            FG = FC1
            EFG = ft.GetField('E_FC')
          if (SigCD == '84'):
            FG = FC1                    # Since no floe size recorded for D column, just assign same floe size as C column
            EFG = ft.GetField('E_FC')   # Since no floe size recorded for D column, just assign same floe size as C column

          # find floe size for any greywhite 85/5 ice
          FGW = '-9'
          EFGW = ' '
          if (SA1 == '85'):
            FGW = FA1
            EFGW = ft.GetField('E_FA')
          if (SB1 == '85'):
            FGW = FB1
            EFGW = ft.GetField('E_FB')
          if (SC1 == '85'):
            FGW = FC1
            EFGW = ft.GetField('E_FC')
          if (SigCD == '85'):
            FGW = FC1                   #Since no floe size recorded for D column, just assign same floe size as C column
            EFGW = ft.GetField('E_FC')  #Since no floe size recorded for D column, just assign same floe size as C column

          # floe sizes for new ice is always Sigrid '99' or Egg 'X'
          FN = '99' 
          EFN = 'X'

          # floe sizes for icebergs is always Sigrid '10' or Egg '9'
          FBerg = '10' 
          EFBerg = '9'

          # i.3) Set default values for columns that are often blank ... will be overwritten if needed (ignore E_SE and E_FE as always blank and don't change)
          CN1_new = '-9' # Sigrid column for ice type of trace amounts
          ESO_new = ' '  # Egg column for ice type of trace amounts
          CD_new = '-9'
          ECD_new = ' '
          ESD_new = ' '
          EFD_new = ' '
          ECS_new = ' ' # Egg column for concentration of ice in strips and patches

          # 1.4.0) determine what goes in the trace column of the new egg
          if (CMY == 0.3):
            CN1_new = '97'
            ESO_new = '9.'
          else:
            if (CSY == 0.3):
              CN1_new = '96'
              ESO_new = '8.'
            else:
              if (CGW == 0.3):
                CN1_new = '85'
                ESO_new = '5'
              else:
                if (CG == 0.3):
                  CN1_new = '84'
                  ESO_new = '4'
                else:
                  if(CN == 0.3):  # This case should never happen
                    CN1_new = '81'
                    ESO_new = '1'
                  else:
                    CN1_new = '-9'
                    ESO_new = ' '

          # i.4.1) determine what goes in column A of the new egg
          # NOTE: if a concentration of bergs exists, then it always goes in column A
          if (CBerg > 0.2):
            CA_new = str(int(CBerg*10))
            SA_new = '98'
            FA_new = '10'
            ECA_new = str(int(CBerg))
            ESA_new = 'L'
            EFA_new = '9'
          elif (CBerg <= 0.2) and (CMY > 0.3):
            if (CMY > 0.3) and (CMY < 9.7):
              CA_new = str(int(CMY*10))
              SA_new = '97'
              FA_new = FMY
              ECA_new = str(int(CMY))
              ESA_new = '9.'
              EFA_new = EFMY
            elif (CMY == 9.7):
              CA_new = '-9' # CT = CT_tot will = 91
              SA_new = '97'
              FA_new = FMY
              ECA_new = ' ' # E_CT = CT_tot will = 9+
              ESA_new = '9.'
              EFA_new = EFMY
            elif (CMY == 10.0):
              CA_new = '-9'  # CT = CT_tot will = 92
              SA_new = '97'
              FA_new = FMY  #'08' 
              ECA_new = ' '  # E_CT = CT_tot will = 10
              ESA_new = '9.'
              EFA_new = EFMY  #'8' 
          elif (CBerg <= 0.2) and (CMY <= 0.3):
            if (CSY > 0.3):
              if (CSY > 0.3) and (CSY < 9.7):
                CA_new = str(int(CSY*10))
                SA_new = '96'
                FA_new = FSY
                ECA_new = str(int(CSY))
                ESA_new = '8.'
                EFA_new = EFSY
              elif (CSY == 9.7):
                CA_new = '-9'  # CT = CT_tot will = 91
                SA_new = '96'
                FA_new = FSY
                ECA_new = ' '  # E_CT = CT_tot will = 9+
                ESA_new = '8.'
                EFA_new = EFSY
              elif (CSY == 10.0):
                CA_new = '-9'  # CT = CT_tot will = 92
                SA_new = '96'
                FA_new = FSY  #'08'
                ECA_new = ' '  # E_CT = CT_tot will = 10
                ESA_new = '8.'
                EFA_new = EFSY  #'8'
            elif (CSY <= 0.3):
              if (CGW > 0.3):
                if (CGW > 0.3) and (CGW < 9.7):
                  CA_new = str(int(CGW*10))
                  SA_new = '85'
                  FA_new = FGW
                  ECA_new = str(int(CGW))
                  ESA_new = '5'
                  EFA_new = EFGW
                elif (CGW == 9.7):
                  CA_new = '-9'  # CT = CT_tot will = 91
                  SA_new = '85'
                  FA_new = FGW
                  ECA_new = ' '  # E_CT = CT_tot will = 9+
                  ESA_new = '5'
                  EFA_new = EFGW
                elif (CGW == 10.0):
                  CA_new = '-9'  # CT = CT_tot will = 92
                  SA_new = '85'
                  FA_new = FGW  #'08'
                  ECA_new = ' '  # E_CT = CT_tot will = 10
                  ESA_new = '5'
                  EFA_new = EFGW  #'8'
              elif (CGW <= 0.3):
                if (CG > 0.3):
                  if (CG > 0.3) and (CG < 9.7):
                    CA_new = str(int(CG*10))
                    SA_new = '84'
                    FA_new = FG
                    ECA_new = str(int(CG))
                    ESA_new = '4'
                    EFA_new = EFG
                  elif (CG == 9.7):
                    CA_new = '-9'  # CT = CT_tot will = 91
                    SA_new = '84'
                    FA_new = FG
                    ECA_new = ' '  # E_CT = CT_tot will = 9+
                    ESA_new = '4'
                    EFA_new = EFG
                  elif (CG == 10.0):
                    CA_new = '-9'  # CT = CT_tot will = 92
                    SA_new = '84'
                    FA_new = FG  #'08'
                    ECA_new = ' '  # E_CT = CT_tot will = 10
                    ESA_new = '4'
                    EFA_new = EFG  #'8'
                elif (CG <= 0.3):
                  if (CN > 0.3):
                    if (CN > 0.3) and (CN < 9.7):
                      CA_new = str(int(CN*10))
                      SA_new = '81'
                      FA_new = FN
                      ECA_new = str(int(CN))
                      ESA_new = '1'
                      EFA_new = EFN
                    elif (CN == 9.7):
                      CA_new = '-9'  # CT = CT_tot will = 91
                      SA_new = '81'
                      FA_new = FN
                      ECA_new = ' '  # E_CT = CT_tot will = 9+
                      ESA_new = '1'
                      EFA_new = EFN
                    elif (CN == 10.0):
                      CA_new = '-9'  # CT = CT_tot will = 92
                      SA_new = '81'
                      FA_new = FN  #'08'
                      ECA_new = ' '  # E_CT = CT_tot will = 10
                      ESA_new = '1'
                      EFA_new = EFN  #'8'

          # i.5) determine what goes in column B of the new egg
          if (SA_new == '98'):
            if (CMY > 0.3):
              if (CMY > 0.3) and (CMY < 9.7):
                CB_new = str(int(CMY*10))
                SB_new = '97'
                FB_new = FMY
                ECB_new = str(int(CMY))
                ESB_new = '9.'
                EFB_new = EFMY
            elif (CMY <= 0.3):
              if (CSY > 0.3):
                if (CSY > 0.3) and (CSY < 9.7):
                  CB_new = str(int(CSY*10))
                  SB_new = '96'
                  FB_new = FSY
                  ECB_new = str(int(CSY))
                  ESB_new = '8.'
                  EFB_new = EFSY
              elif (CSY <= 0.3):
                if (CGW > 0.3):
                  if (CGW > 0.3) and (CGW < 9.7):
                    CB_new = str(int(CGW*10))
                    SB_new = '85'
                    FB_new = FGW
                    ECB_new = str(int(CGW))
                    ESB_new = '5'
                    EFB_new = EFGW
                elif (CGW <= 0.3):
                  if (CG > 0.3):
                    if (CG > 0.3) and (CG < 9.7):
                      CB_new = str(int(CG*10))
                      SB_new = '84'
                      FB_new = FG
                      ECB_new = str(int(CG))
                      ESB_new = '4'
                      EFB_new = EFG
                  elif (CG <= 0.3):
                    if (CN > 0.3):
                      if (CN > 0.3) and (CN < 9.7):
                        CB_new = str(int(CN*10))
                        SB_new = '81'
                        FB_new = FN
                        ECB_new = str(int(CN))
                        ESB_new = '1'
                        EFB_new = EFN
                    else:
                      CB_new = '-9'
                      SB_new = '-9'
                      FB_new = '-9'
                      ECB_new = ' '
                      ESB_new = ' '
                      EFB_new = ' '
          elif (SA_new == '97'):
            if (CSY > 0.3):
              if (CSY > 0.3) and (CSY < 9.7):
                CB_new = str(int(CSY*10))
                SB_new = '96'
                FB_new = FSY
                ECB_new = str(int(CSY))
                ESB_new = '8.'
                EFB_new = EFSY
            elif (CSY <= 0.3):
              if (CGW > 0.3):
                if (CGW > 0.3) and (CGW < 9.7):
                  CB_new = str(int(CGW*10))
                  SB_new = '85'
                  FB_new = FGW
                  ECB_new = str(int(CGW))
                  ESB_new = '5'
                  EFB_new = EFGW
              elif (CGW <= 0.3):
                if (CG > 0.3):
                  if (CG > 0.3) and (CG < 9.7):
                    CB_new = str(int(CG*10))
                    SB_new = '84'
                    FB_new = FG
                    ECB_new = str(int(CG))
                    ESB_new = '4'
                    EFB_new = EFG
                elif (CG <= 0.3):
                  if (CN > 0.3):
                    if (CN > 0.3) and (CN < 9.7):
                      CB_new = str(int(CN*10))
                      SB_new = '81'
                      FB_new = FN
                      ECB_new = str(int(CN))
                      ESB_new = '1'
                      EFB_new = EFN
                  else:
                    CB_new = '-9'
                    SB_new = '-9'
                    FB_new = '-9'
                    ECB_new = ' '
                    ESB_new = ' '
                    EFB_new = ' '
          elif (SA_new == '96'):
            if (CGW > 0.3):
              if (CGW > 0.3) and (CGW < 9.7):
                CB_new = str(int(CGW*10))
                SB_new = '85'
                FB_new = FGW
                ECB_new = str(int(CGW))
                ESB_new = '5'
                EFB_new = EFGW
            elif (CGW <= 0.3):
              if (CG > 0.3):
                if (CG > 0.3) and (CG < 9.7):
                  CB_new = str(int(CG*10))
                  SB_new = '84'
                  FB_new = FG
                  ECB_new = str(int(CG))
                  ESB_new = '4'
                  EFB_new = EFG
              elif (CG <= 0.3):
                if (CN > 0.3):
                  if (CN > 0.3) and (CN < 9.7):
                    CB_new = str(int(CN*10))
                    SB_new = '81'
                    FB_new = FN
                    ECB_new = str(int(CN))
                    ESB_new = '1'
                    EFB_new = EFN
                else:
                  CB_new = '-9'
                  SB_new = '-9'
                  FB_new = '-9'
                  ECB_new = ' '
                  ESB_new = ' '
                  EFB_new = ' '
          elif (SA_new == '85'):
            if (CG > 0.3):
              if (CG > 0.3) and (CG < 9.7):
                CB_new = str(int(CG*10))
                SB_new = '84'
                FB_new = FG
                ECB_new = str(int(CG))
                ESB_new = '4'
                EFB_new = EFG
            elif (CG <= 0.3):
              if (CN > 0.3):
                if (CN > 0.3) and (CN < 9.7):
                  CB_new = str(int(CN*10))
                  SB_new = '81'
                  FB_new = FN
                  ECB_new = str(int(CN))
                  ESB_new = '1'
                  EFB_new = EFN
              else:
                CB_new = '-9'
                SB_new = '-9'
                FB_new = '-9'
                ECB_new = ' '
                ESB_new = ' '
                EFB_new = ' '
          elif (SA_new == '84'):
            if (CN > 0.3):
              if (CN > 0.3) and (CN < 9.7):
                CB_new = str(int(CN*10))
                SB_new = '81'
                FB_new = FN
                ECB_new = str(int(CN))
                ESB_new = '1'
                EFB_new = EFN
            else:
              CB_new = '-9'
              SB_new = '-9'
              FB_new = '-9'
              ECB_new = ' '
              ESB_new = ' '
              EFB_new = ' '
          elif (SA_new == '81'):
            CB_new = '-9'
            SB_new = '-9'
            FB_new = '-9'
            ECB_new = ' '
            ESB_new = ' '
            EFB_new = ' '  
          
          # i.6) determine what goes in column C of the new egg
          if (SB_new == '97'):
            if (CSY > 0.3):
              if (CSY > 0.3) and (CSY < 9.7):
                CC_new = str(int(CSY*10))
                SC_new = '96'
                FC_new = FSY
                ECC_new = str(int(CSY))
                ESC_new = '8.'
                EFC_new = EFSY
            elif (CSY <= 0.3):
              if (CGW > 0.3):
                if (CGW > 0.3) and (CGW < 9.7):
                  CC_new = str(int(CGW*10))
                  SC_new = '85'
                  FC_new = FGW
                  ECC_new = str(int(CGW))
                  ESC_new = '5'
                  EFC_new = EFGW
              elif (CGW <= 0.3):
                if (CG > 0.3):
                  if (CG > 0.3) and (CG < 9.7):
                    CC_new = str(int(CG*10))
                    SC_new = '84'
                    FC_new = FG
                    ECC_new = str(int(CG))
                    ESC_new = '4'
                    EFC_new = EFG
                elif (CG <= 0.3):
                  if (CN > 0.3):
                    if (CN > 0.3) and (CN < 9.7):
                      CC_new = str(int(CN*10))
                      SC_new = '81'
                      FC_new = FN
                      ECC_new = str(int(CN))
                      ESC_new = '1'
                      EFC_new = EFN
                  else:
                    CC_new = '-9'
                    SC_new = '-9'
                    FC_new = '-9'
                    ECC_new = ' '
                    ESC_new = ' '
                    EFC_new = ' '
          elif (SB_new == '96'):
            if (CGW > 0.3):
              if (CGW > 0.3) and (CGW < 9.7):
                CC_new = str(int(CGW*10))
                SC_new = '85'
                FC_new = FGW
                ECC_new = str(int(CGW))
                ESC_new = '5'
                EFC_new = EFGW
            elif (CGW <= 0.3):
              if (CG > 0.3):
                if (CG > 0.3) and (CG < 9.7):
                  CC_new = str(int(CG*10))
                  SC_new = '84'
                  FC_new = FG
                  ECC_new = str(int(CG))
                  ESC_new = '4'
                  EFC_new = EFG
              elif (CG <= 0.3):
                if (CN > 0.3):
                  if (CN > 0.3) and (CN < 9.7):
                    CC_new = str(int(CN*10))
                    SC_new = '81'
                    FC_new = FN
                    ECC_new = str(int(CN))
                    ESC_new = '1'
                    EFC_new = EFN
                else:
                  CC_new = '-9'
                  SC_new = '-9'
                  FC_new = '-9'
                  ECC_new = ' '
                  ESC_new = ' '
                  EFC_new = ' '
          elif (SB_new == '85'):
            if (CG > 0.3):
              if (CG > 0.3) and (CG < 9.7):
                CC_new = str(int(CG*10))
                SC_new = '84'
                FC_new = FG
                ECC_new = str(int(CG))
                ESC_new = '4'
                EFC_new = EFG
            elif (CG <= 0.3):
              if (CN > 0.3):
                if (CN > 0.3) and (CN < 9.7):
                  CC_new = str(int(CN*10))
                  SC_new = '81'
                  FC_new = FN
                  ECC_new = str(int(CN))
                  ESC_new = '1'
                  EFC_new = EFN
              else:
                CC_new = '-9'
                SC_new = '-9'
                FC_new = '-9'
                ECC_new = ' '
                ESC_new = ' '
                EFC_new = ' '
          elif (SB_new == '84'):
            if (CN > 0.3):
              if (CN > 0.3) and (CN < 9.7):
                CC_new = str(int(CN*10))
                SC_new = '81'
                FC_new = FN
                ECC_new = str(int(CN))
                ESC_new = '1'
                EFC_new = EFN
            else:
              CC_new = '-9'
              SC_new = '-9'
              FC_new = '-9'
              ECC_new = ' '
              ESC_new = ' '
              EFC_new = ' '
          elif (SB_new == '81') or (SB_new == '-9'):
            CC_new = '-9'
            SC_new = '-9'
            FC_new = '-9'
            ECC_new = ' '
            ESC_new = ' '
            EFC_new = ' '  
          
          # i.7) determine what goes in column D of the new egg ... no floe sizes for this column ... for Sigrid: only field CD (=SOD of remaining ice type); for Egg: only E_CD and E_SD (E_FD left blank)
          if (SC_new == '96'):
            if (CGW > 0.3):
              if (CGW > 0.3) and (CGW < 9.7):
                CD_new = '85'
                ECD_new = str(int(CGW))
                ESD_new = '5'
                EFD_new = ' '
            elif (CGW <= 0.3):
              if (CG > 0.3):
                if (CG > 0.3) and (CG < 9.7):
                  CD_new = '84'
                  ECD_new = str(int(CG))
                  ESD_new = '4'
                  EFD_new = ' '
              elif (CG <= 0.3):
                if (CN > 0.3):
                  if (CN > 0.3) and (CN < 9.7):
                    CD_new = '81'
                    ECD_new = str(int(CN))
                    ESD_new = '1'
                    EFD_new = ' '
                else:
                  CD_new = '-9'
                  ECD_new = ' '
                  ESD_new = ' '
                  EFD_new = ' '
          elif (SC_new == '85'):
            if (CG > 0.3):
              if (CG > 0.3) and (CG < 9.7):
                CD_new = '84'
                ECD_new = str(int(CG))
                ESD_new = '4'
                EFD_new = ' '
            elif (CG <= 0.3):
              if (CN > 0.3):
                if (CN > 0.3) and (CN < 9.7):
                  CD_new = '81'
                  ECD_new = str(int(CN))
                  ESD_new = '1'
                  EFD_new = ' '
              else:
                CD_new = '-9'
                ECD_new = ' '
                ESD_new = ' '
                EFD_new = ' '
          elif (SC_new == '84'):
            if (CN > 0.3):
              if (CN > 0.3) and (CN < 9.7):
                CD_new = '81'
                ECD_new = str(int(CN))
                ESD_new = '1'
                EFD_new = ' '
            else:
              CD_new = '-9'
              ECD_new = ' '
              ESD_new = ' '
              EFD_new = ' '
          elif (SC_new == '81') or (SC_new == '-9'):
            CD_new = '-9'
            ECD_new = ' '
            ESD_new = ' '
            EFD_new = ' '
                      
          # i.8) double-check Fast Ice eggs ... anytime CT_tot = 10 (fast ice) ... floe size '8' goes in right-hand most column
          # First check if CT_tot == 10 and if more than one column, set last column F = 8              
          if (CT_tot == 10.0):
            if (CC_new != '-9'):
              FC_new = '08'
              EFC_new = '8'
            elif (CC_new == '-9') and (CB_new != '-9'):
              FB_new = '08'
              EFB_new = '8'
            elif (CC_new == '-9') and (CB_new == '-9'):  
              FA_new = '08'
              EFA_new = '8'

          # Then make sure don't have floe size '8' in more than one column (could happen if 8 was already assigned above) ... if this occurs, give the duplicate-8 column(s) to the left of the Fast Ice column a generic floe size since not important for Atlas 
          if (CT_tot == 10.0):
            if (CC_new != '-9') and ((FC_new == '08') and (FB_new == '08')): 
              FB_new = '04' #assign some generic non-fast floe size
              EFB_new = '4' #assign some generic non-fast floe size
            elif (CC_new != '-9') and ((FC_new == '08') and (FA_new == '08')): 
              FA_new = '05' #assign some generic non-fast floe size
              EFA_new = '5' #assign some generic non-fast floe size
            elif (CC_new != '-9') and ((FC_new == '08') and (FB_new == '08') and (FA_new == '08')):
              FB_new = '04' #assign some generic non-fast floe size
              EFB_new = '4' #assign some generic non-fast floe size
              FA_new = '05' #assign some generic non-fast floe size
              EFA_new = '5' #assign some generic non-fast floe size
            elif (CC_new == '-9') and ((FB_new == '08') and (FA_new == '08')):
              FA_new = '05' #assign some generic non-fast floe size
              EFA_new = '5' #assign some generic non-fast floe size
                

          # i.9) Strips and Patches ... 
          # NOTE: These are not being coded in our Sigrids ... but need to make sure floe size columns are -9 or blank in this case
          if (CT_tot >= 1.0) and (CT_tot < 10.0):
            if (FA1 == '-9') and (FB1 == '-9') and (FC1 == '-9'):  # implies must be strips / patches
              FA_new = '-9'
              FB_new = '-9'
              FC_new = '-9'
              EFA_new = ' '
              EFB_new = ' '
              EFC_new = ' '
              ECS_new = '9+'  # populate the E_CS column with a generic concentration for the ice in the strips, because ... why not?  

          # i.10) For single column eggs ... CA = '-9' and E_CA = ' ' (because they are simply equivalent to the total CT) ...
          # ... check if Egg only has a single column, if yes then set CA='-9'/E_CA=' ' in case there is a value in that field (seems to only happen in Strips/Patches cases)
          if (CA_new != '-9') and ((CB_new == '-9') and (CC_new == '-9')):
            CA_new = '-9'
            ECA_new = ' '
          
          # j) update Sigrid fields ('CT','CA','SA','FA','CB','SB','FB','CC','SC','FC','CN','CD') 
          # CT (row[1]) stays the same
          ft.SetField('CA', CA_new)
          ft.SetField('SA', SA_new)
          ft.SetField('FA', FA_new)
          ft.SetField('CB', CB_new)
          ft.SetField('SB', SB_new)
          ft.SetField('FB', FB_new)
          ft.SetField('CC', CC_new)
          ft.SetField('SC', SC_new)
          ft.SetField('FC', FC_new)
          ft.SetField('CN', CN1_new)
          ft.SetField('CD', CD_new)

          # k) update Egg fields ('E_CT','E_CA','E_CB','E_CC','E_CD','E_SO','E_SA','E_SB','E_SC','E_SD','E_SE','E_FA','E_FB','E_FC','E_FD','E_FE','E_CS')
          # E_CT (row[13]) stays the same
          ft.SetField('E_CA', ECA_new)
          ft.SetField('E_CB', ECB_new)
          ft.SetField('E_CC', ECC_new)
          ft.SetField('E_CD', ECD_new)
          ft.SetField('E_SO', ESO_new)
          ft.SetField('E_SA', ESA_new)
          ft.SetField('E_SB', ESB_new)
          ft.SetField('E_SC', ESC_new)
          ft.SetField('E_SD', ESD_new)
          #row[23] = ESE_new ... stays the same (blank)
          ft.SetField('E_FA', EFA_new)
          ft.SetField('E_FB', EFB_new)
          ft.SetField('E_FC', EFC_new)
          #row[27] = EFD_new ... blank
          #row[28] = EFE_new ... stays the same (blank)
          ft.SetField('E_CS', ECS_new) # ... stays the same (blank at the moment, but should have a value like '9' or '9+' (sigrid 19 or 91) based on Egg_attr value at the end) ... 


          #### l) update Egg_Attr field ('EGG_ATTR') ... first check if this field is present ... not present in new SIGRIDS
          if 'EGG_ATTR' in fields:
            # First create the new Egg_Attr for the polygon
            Egg_Attr_new = ''
            ECD_new = ' '  # The E_CD field is populated in the Egg columns but not in the Egg_Attr for some reason ...
            ESE_new = ' '
            EFD_new = ' '
            EFE_new = ' '
            Egg_fields_newVals = [CT1,ECA_new,ECB_new,ECC_new,ECD_new,ESO_new,ESA_new,ESB_new,ESC_new,ESD_new,ESE_new,EFA_new,EFB_new,EFC_new,EFD_new,EFE_new,ECS_new]
            # for kk in Egg_fields_newVals:
            #    if (kk in EMPTY):
            #        kk = '@'
            for kk in range(0, len(Egg_fields_newVals)):
              if (Egg_fields_newVals[kk] in EMPTY):
                Egg_fields_newVals[kk] = '@'        
            if (ECS_new != ' '):
              ECS_newS = '~' + ECS_new
            else:
              ECS_newS = '@'
            # Egg_Attr_new = CT1 + '_' + ECA_new + '_' + ECB_new + '_' + ECC_new + '_' + ECD_new + '_' + ESO_new + '_' + ESA_new + '_' + ESB_new + '_' + ESC_new + '_' + ESD_new + '_' + ESE_new + '_' + EFA_new + '_' + EFB_new + '_' + EFC_new + '_' + EFD_new + '_' + EFE_new + '_' + ECS_newS
            Egg_Attr_new = Egg_fields_newVals[0] + '_' + Egg_fields_newVals[1] + '_' + Egg_fields_newVals[2] + '_' + Egg_fields_newVals[3] + '_' + Egg_fields_newVals[4] + '_' + Egg_fields_newVals[5] + '_' + Egg_fields_newVals[6] + '_' + Egg_fields_newVals[7] + '_' + Egg_fields_newVals[8] + '_' + Egg_fields_newVals[9] + '_' + Egg_fields_newVals[10] + '_' + Egg_fields_newVals[11] + '_' + Egg_fields_newVals[12] + '_' + Egg_fields_newVals[13] + '_' + Egg_fields_newVals[14] + '_' + Egg_fields_newVals[15] + '_' + ECS_newS    

            # Then update the Egg_Attr field in the dbf file / attribute table
            ft.SetField('EGG_ATTR', Egg_Attr_new)
        
        # apply changes to feature
        layer.SetFeature(ft)

    logging.info('completed')

  except Exception as e:
    raise baseException(f'could not apply October01 patch to {fn}', baseException.ERR_CODE_LEVEL, e)