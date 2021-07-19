import  sqlite3
import os
from tkinter import *
import tkinter.font as font
#from tkinter.ttk import *
folder1=os.getcwd()
BDdispo=[]
files=os.listdir(folder1)
def escolhertbs():
    ########################
    def abrirtbs():
        c.execute("SELECT * from '{}'".format(variable2.get()))
        #
        OriginalINFO=[]
        NewINFO=[]
        NomeTabelaAtual=variable2.get()
        #
        tbshow=Toplevel()
        #
        ROWSzada = list(map(lambda x: x[0], c.description))
        ROWSzadaSTR=''
        for i in ROWSzada:
            ROWSzadaSTR+=' '+str(i)+'/'
        ROWSzadaSTR=ROWSzadaSTR[:-1]
        #
        tbshow.title("Editando BD: {} (Máx. 1500 linhas)-(Colunas: {}) ".format(variable2.get(), ROWSzadaSTR))
        tbshow.geometry("648x400+350+150")
        AT1=Label(tbshow, text=variable2.get())
        AT1.place(x=1, y=1)
        ###################V      E    R     T    I         C        A         L
        main_frame=Frame(tbshow)
        main_frame.pack(fill=BOTH, expand=1)
        #
        my_canvas=Canvas(main_frame)
        my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
        #
        my_scrollbar=Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        #
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        #
        second_frame=Frame(my_canvas)
        #
        my_canvas.create_window((0,0), window=second_frame, anchor='nw')
        ###################
        ####
        voidchecker=0
        if c.fetchone() is None:
            c.execute("SELECT * from '{}'".format(NomeTabelaAtual))
            ROWSzada = list(map(lambda x: x[0], c.description))
            NUMROWS=len(ROWSzada)
            voidfiller=0
            STRfiller=''
            while voidfiller<NUMROWS:
                if voidfiller==0:
                    STRfiller+="('"+ROWSzada[voidfiller]
                if voidfiller>0:
                    STRfiller+="', '"+ROWSzada[voidfiller]
                voidfiller+=1
            STRfiller+="')"
            c.execute("INSERT INTO '{}' VALUES {} ".format(NomeTabelaAtual, STRfiller))
            conex.commit()
        ###
        c.execute("SELECT * from '{}'".format(variable2.get()))
        
        CNumber=(len(c.fetchone())+1) ####+1 COM ROWID
        ###################
        tbshowSELEC=c.execute("SELECT rowid, * from '{}'".format(variable2.get()))
        tbsI=0
        OriginalINFO=[]
        for multi in tbshowSELEC:
            OI3=[]
            for tbsJ in range(len(multi)):
                e=Entry(second_frame, width=10, fg='blue')
                e.grid(row=tbsI, column=tbsJ)
                e.insert(END, multi[tbsJ])
                e['font']=myFont2a
                if tbsJ==0:
                    e.config(state='disabled')
                if len(OI3)<CNumber:
                    OI3.append(multi[tbsJ])
                if len(OI3)==CNumber:
                    OriginalINFO.append(OI3)
                    OI3=[]
                #e.config(state=DISABLED)
            tbsI+=1
            if tbsI>1500:
                break
        #######^^^^^^^^^^^^^^^^^LIMIT
        def Diff(l1, l2):
            difers=[]
            for i in l1:
                num1=l1.index(i)
                if i!=l2[num1]:
                    difers.append(l2[num1])
            return difers
        #######
        
        InfoW=second_frame.winfo_children()
        NewRAW=[]
        NewINFO=[]
        
        def getEntries(p):
            NI3=[]
            childrenW=p.winfo_children()
            for child_widget in childrenW:
                if child_widget.winfo_class()=='Entry':
                    NewRAW.append(child_widget.get())
            for i in NewRAW:
                if len(NI3)<CNumber:
                    if i.isdigit()==True:
                        NI3.append(int(i))
                    if i.isdigit()==False:
                        NI3.append(i)
                if len(NI3)==CNumber:
                    NewINFO.append(NI3)
                    NI3=[]
            ToChange=list(Diff(OriginalINFO, NewINFO))
            c.execute("SELECT * from '{}'".format(NomeTabelaAtual))
            NamesColunasAtual = list(map(lambda x: x[0], c.description))
            NumColunas=len(NamesColunasAtual)
            for i in ToChange:
                num=0
                for x in i:
                    rownum=i[0]
                    if num>0:
                        c.execute("UPDATE '{}' SET {} = '{}' WHERE rowid = {}".format(NomeTabelaAtual, NamesColunasAtual[num-1], str(x), str(rownum)))
                        conex.commit()
                    num+=1
        table=Frame(second_frame)
        for _ in range(3):
            Entry(table).pack()
        #
        c.execute("SELECT * from '{}'".format(NomeTabelaAtual))
        NamesColunasAtual = list(map(lambda x: x[0], c.description))
        #
        NumColumnCreate=CNumber-1
        #
        def closea1():
            tbshow()
            tbshow.destroy()
        a1=Button(tbshow, text='Finalizar edição', bg='#e1e8ed', font=myFont2a,
            command=lambda w=table: [(getEntries(second_frame)), (closea1)]).pack(padx=5, pady=15, side=RIGHT)
        #
        def criarlinhaBUT():
            rowcreate=Toplevel()
            rowcreate.title("Criando linha BD: {} (Obs: É necessário criar uma linha sem número preexistente)".format(variable2.get()))
            #rowcreate.geometry("700x200+325+268")
            if len(NamesColunasAtual)<=6:
                rowcreate.geometry("700x200+325+268")
            if len(NamesColunasAtual)>6:
                rowcreate.geometry("1300x200+20+274")
            for i in NamesColunasAtual:
                e=Entry(rowcreate)
                e.pack(side=LEFT)
                a=Label(rowcreate, text=i)
                a.place(in_=e, y=-25)
                
            childrenL=rowcreate.winfo_children()
            def criarlinhaBUT2():
                DataInsert=[]
                for child_widget in childrenL:
                    if child_widget.winfo_class()=='Entry':
                        DataInsert.append(child_widget.get())
                DataInsert2=(str(DataInsert).replace('[', '(')).replace(']', ')')
                c.execute("INSERT INTO '{}' VALUES {}".format(NomeTabelaAtual, DataInsert2))
                conex.commit()
                
                abrirtbs()
                rowcreate.destroy()
                tbshow.destroy()

                ##VPOLTAR
            rowcBUT=Button(rowcreate, text='Criar nova linha', command=criarlinhaBUT2)
            rowcBUT.pack(side=BOTTOM)
            if len(NamesColunasAtual)<=6:
                rowcBUT['font']=myFont2
            if len(NamesColunasAtual)>6:
                rowcBUT['font']=myFont2
                rowcBUT['text']='Criar'
        #
        criarlinha=Button(tbshow, text='Criar linha', command=criarlinhaBUT)
        criarlinha.place(x=195,y=375)
        criarlinha.pack(padx=5, pady=15, side=RIGHT)
        criarlinha['bg']='#daf0d8'
        #
        ########
        def dellinhaBUT():
            rowdel=Toplevel()
            rowdel.geometry("265x120+350+150")
            #
            rowdelLBL=Label(rowdel, text='Digite o índice (número):')
            rowdelLBL.place(x=26,y=15)
            rowdelLBL['font']=myFont2
            #
            rowdelENT=Entry(rowdel)
            rowdelENT.place(x=60,y=45, height=30, width=140)
            rowdelENT['font']=myFont2
            #
            def dellinhaBUT2():
                NUM=rowdelENT.get()
                c.execute("SELECT * from '{}'".format(NomeTabelaAtual))
                if NUM.isdigit()==True and int(NUM)>0:
                    c.execute("SELECT rowid, * from '{}'".format(NomeTabelaAtual))
                    c.execute("DELETE from '{}' where rowid = {}".format(NomeTabelaAtual, int(NUM)))
                    conex.commit()

                    abrirtbs()
                    rowdel.destroy()
                    tbshow.destroy()
            #
            rowdelBUT=Button(rowdel, text='Deletar linha', command=dellinhaBUT2)
            rowdelBUT.pack(side=BOTTOM)
            rowdelBUT['font']=myFont2a
            #
            #
        dellinha=Button(tbshow, text='Deletar linha', command=dellinhaBUT)
        dellinha.place(x=390,y=375)
        dellinha.pack(padx=5, pady=15, side=RIGHT)
        dellinha['bg']='#f0d8d8'
        
    def criartbs():
        tbcr=Toplevel()
        tbcr.title('Criando tabela')
        tbcr.geometry("225x120+350+150")
        tbcr.resizable(0,0)
        #
        tbcrLBL=Label(tbcr, text='Título da tabela:')
        tbcrLBL.place(x=40,y=5)
        tbcrLBL['font']=myFont2
        #
        tbcrTXT=Entry(tbcr)
        tbcrTXT.place(x=30, y=30, height=26, width=160)
        tbcrTXT['font']=myFont2
        #
        tbcrNumIndices = StringVar(tbesc)
        tbcrNumIndices.set('Número de Colunas')
        #
        tbcrNUM=OptionMenu(tbcr, tbcrNumIndices,*[1,2,3,4,5,6,7,8,9,10])
        tbcrNUM.place(x=30, y=58, height=26, width=160)
        #
        def criartbsSQL():
            if str(tbcrNumIndices.get()).isdigit()==True:
                roofnum=int(tbcrNumIndices.get())
                stacking=1
                #
                CTsql=Toplevel()
                CTsql.title("Preencha as informações de criação.".format(variable2.get()))
                if roofnum<=6:
                    CTsql.geometry("700x200+325+268")
                if roofnum>6:
                    CTsql.geometry("1300x200+20+274")
                #
                while stacking<=roofnum:
                    e1=Entry(CTsql)
                    e1.pack(side=LEFT)
                    #
                    a=Label(CTsql, text='Nome da coluna {}:'.format(stacking))
                    a.place(in_=e1, y=-25)
                    stacking+=1
                def criartbsSQL2():
                    childrenCRIAR=CTsql.winfo_children()
                    DataInsert=[]
                    for child_widget in childrenCRIAR:
                        if child_widget.winfo_class()=='Entry':
                            DataInsert.append(child_widget.get())
                    DataInsert2=(str(DataInsert).replace('[', '(')).replace(']', ')')
                    DataInsert3=DataInsert2.replace("'","")
                    c.execute("CREATE TABLE '{}' {}".format(str(tbcrTXT.get()),DataInsert2))
                    conex.commit()
                    #
                    escolhertbs()
                    tbesc.destroy()
                    tbcr.destroy()
                    CTsql.destroy()
                
                finalCTsql=Button(CTsql, text='Criar tabela', command=criartbsSQL2)
                finalCTsql.pack(side=BOTTOM)
                finalCTsql['font']=myFont2
        #
        tbcrBUT=Button(tbcr, text='Criar tabela', command=criartbsSQL)
        tbcrBUT.place(x=48,y=86, height=30, width=120)
        tbcrBUT['font']=myFont2a
        
    def deltbs():
        deltbs=Toplevel()
        deltbs.title('Deletando tabela')
        deltbs.geometry("225x120+350+150")
        deltbs.resizable(0,0)
        #
        deltbsLBL=Label(deltbs, text='Selecione a tabela:')
        deltbsLBL.place(x=40,y=15)
        deltbsLBL['font']=myFont2
        #
        variable3 = StringVar(tbesc)
        variable3.set(listaNomeTable[0])
        #
        deltbsBUT=OptionMenu(deltbs, variable3, *listaNomeTable)
        deltbsBUT.place(x=40,y=45, height=30, width=140)
        deltbsBUT['font']=myFont2
        #
        def deltbsSQL():
            c.execute("DROP TABLE '{}'".format(str(variable3.get())))
            conex.commit()

            
            escolhertbs()
            tbesc.destroy()
            deltbs.destroy()
            
        deltbsBUT=Button(deltbs, text='Deletar tabela', command=deltbsSQL)
        deltbsBUT.place(x=48,y=80, height=30, width=120)
        deltbsBUT['font']=myFont2a
        #(command=??)
        
        
    ########################
    conex=sqlite3.connect(variable.get())
    c = conex.cursor()
    #
    c.execute("SELECT rowid, name from sqlite_master WHERE type='table';")
    listaIndices=[]
    listaNomeTable=[]
    for i in c.fetchall():
        listaIndices.append(i[0])
        listaNomeTable.append(i[1])
    #
    tbesc=Toplevel()
    tbesc.title("Escolha de Tabela")
    tbesc.geometry('300x160+530+280')
    tbesc.resizable(0,0)
    #tbesc.configure(bg='gray')
    #
    ET1=Label(tbesc, text='Escolha a Tabela:')
    ET1.place(x=50,y=20)
    ET1['font']=myFont3
    #
    variable2 = StringVar(tbesc)
    variable2.set(listaNomeTable[0])
    # default value
    ETdp=OptionMenu(tbesc, variable2, *listaNomeTable)
    ETdp.place(height=34, width=140, x=80, y=60)
    ETdp['font']=myFont1a
    #
    ETbut=Button(tbesc, text='Abrir tabela', command=abrirtbs, bg='#e1e8ed')
    ETbut.place(x=110,y=110,width=80, height=30)
    #
    ETbutCRIAR=Button(tbesc, text='Criar', command=criartbs, bg='#daf0d8')
    ETbutCRIAR.place(x=25,y=110,width=70, height=30)
    #
    ETbutDEL=Button(tbesc, text='Deletar', command=deltbs, bg='#f0d8d8')
    ETbutDEL.place(x=205,y=110,width=70, height=30)
    
########################################################################TELA INICIAL########
for i in files:
    Istring=str(i)
    if Istring[-1]=='b' and Istring[-2]=='d' and Istring[-3]=='.':
        BDdispo.append(i)
#
window=Tk()
window.title("Interface Banco de Dados")
window.geometry("450x280+450+200")
window.resizable(0,0)
#
c = Canvas(window)
c.pack()
c.create_rectangle(500, 500, 0, 100, fill='#F5F5F5',outline='#F5F5F5')
#
myFont1=font.Font(size=20, family='Courier')
myFont1a=font.Font(size=14, family='Courier')
#
myFont2=font.Font(size=14)
myFont2a=font.Font(size=12)
myFont2b=font.Font(size=10)
#
myFont3=font.Font(size=18)
myFont4=font.Font(size=18, family='Calibri')
#
variable = StringVar()
if BDdispo!=[]:
    variable.set(BDdispo[0])
if BDdispo==[]:
    variable.set('[Nenhum arquivo encontrado]')
#
dropdown = OptionMenu(window, variable, *BDdispo)
dropdown.place(height=40, width=280, x=85, y=120)
if BDdispo!=[]:
    dropdown['font']=myFont1
#
selectbut=Button(window, text='Abrir', command=escolhertbs)
selectbut.place(x=185,y=200,width=80, height=40)
selectbut['font']=myFont2
#
#
titulo=Label(window, text='Interface Banco de Dados')
#titulo.place(x=90,y=18)
titulo.place(x=90,y=25)
titulo['font']=myFont4
#
titulo2=Label(window, text='Escolha o banco de dados a ser aberto:')
titulo2.place(x=8,y=60)
titulo2['font']=myFont3

############################################################################################
window.mainloop()
conex.commit()
conex.close()
