from opcua import Client
import schedule, time 
from datetime import datetime


# client = Client("opc.tcp://127.0.0.1:4050")
# client.connect()
# print('connect')
# #
# # array = ['GD06.UF01UD01.KS01.GPA11.MPA.CTM_POP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.CTMA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVD_SGG_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CS_GG.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СTGB_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVD_SGG_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СPGA_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVD_PGG_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CTGB_ST_MAX.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVB_K.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CS_GG_PRIV.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.CT_UP_RK_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTMB_OGGT.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVB_K.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.CT_UP_UK_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GQK.CFG_PO.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GQK.CFG_CGU_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.СPMA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СPGB_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СPGD_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СPGA_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTMB_OGGK.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVB.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.СPM_UP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СTGA_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СPGA_SGU.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVB.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GQK.CFGT_M.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CTGB_GG_AVR.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.СPM_OP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.CTM_POP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPGB_TGG_PLN.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPGB_TGG_PLN.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CTVA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СPGD_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPSUF.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTM_ZOP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CTGB_GG_AVR.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTMB_PST.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GQK.CFGT.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СTGB_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVD_ST_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.CTM_MBD.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CPVD_PGG_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СTGA_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.CT_UP_RK_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.СPMA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CTGB_ST.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CTVA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CS_ST.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.MPA.СPM_OP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CS_GG.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CTGB_ST_MAX.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CTGB_ST.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPSUF.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.СPGA_SGU.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPN.CT_UP_UK_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.СPM_UP_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPN.СPGB_N.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTM_MBD.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GQK.CFG_CGU_V.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CS_GG_PRIV.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA12.GPT.CPVD_ST_ATM.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.MPA.CTMA_D.Socket_IOS.Value', 'GD06.UF01UD01.KS01.GPA11.GPT.CS_ST.Socket_IOS.Value']
# #
# root = client.get_node("ns=2;i=1")
# print(root)
#
# # node_begin = client.get_node("ns=1;s=" + "GD06.UF01UD01.KS01.GPA11.MPA.CTM_POP_N.aH_Value")
# node = client.get_node("ns=1;s=" + "GD06.UF01UD01.KS01.GPA11.GQK.CFGT.Socket_IOS.Value")
#
#
# # print(node_begin.get_data_value())
# print(node.get_data_value())
#
# client.disconnect()
#
# # value = node.get_value()
#
# # print(value)


# list  = [('none', 90), ('none', 28), ('none', 37), ('none', 109), ('none', 26), ('none', 108), ('none', 98), ('none', 115), ('none', 103), ('GP034.AI.GP034_AI_T_GAS_IN_KOL', 38)]#, ('GP001.AI.GP005_AI_P_PZT_230_A', 23), ('GP034.AI.GP034_AI_T_GAS_OUT_KOL', 39)]

# for i in list:
#     print(i[0])


def test1():
    print("Хуяк хуяк я задачка  1" + str(datetime.now()))

def test2():
    print("Хуяк пиздык я задачка 2" + str(datetime.now()))

def test3():
    print("Хуяк пиздык хуяк я задачка 3" + str(datetime.now()))


schedule.every(5).minutes.at(":00").do(test1)
schedule.every(5).minutes.at(":30").do(test2)
schedule.every(5).minutes.at(":59").do(test3)

while True:
    schedule.run_pending()
    time.sleep(1)
