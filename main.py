import customtkinter as ctk
import json
import os
import datetime
#from winotify import Notification
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class App():
    def __init__(self):
        self.janela=ctk.CTk()
        self.janela.geometry("500x600")
        self.janela.title("to do list")
        self.janela.resizable(False,False)
        self.janela.iconbitmap('C:/Users/fledson/Downloads/icon.ico')
        
        self.arquivo_json='tarefas.json'
        self.tarefas=self.carregar_tarefas() 
        self.interface()
    def carregar_tarefas(self):
        if os.path.exists(self.arquivo_json):
            try:
                with open(self.arquivo_json,'r',encoding='utf-8') as arquivo:
                        return json.load(arquivo)
            except :
                return[]
        return []
    def salvar_tarefas(self,tarefas):
        if tarefas is None:
            tarefas = self.tarefas
        with open(self.arquivo_json,'w',encoding='utf-8') as arquivo:
            json.dump(tarefas,arquivo)

    def interface(self):
        self.frame_principal=ctk.CTkFrame(self.janela)
        self.frame_principal.place(relx=0,rely=0,relwidth=1,relheight=1)
        titulo=ctk.CTkLabel(self.frame_principal,
                            text="lista de tarefas",
                            font=('arial',12),
                            text_color='white')
        titulo.pack(pady=20)
        butao_new_task=ctk.CTkButton(self.frame_principal,text='nova tarefa',command=self.new_task,fg_color='blue')
        butao_new_task.pack(pady=10,padx=10,fill="x")
        self.frame_lista=ctk.CTkScrollableFrame(self.frame_principal,
                                                height=400)
        self.frame_lista.pack(pady=10,padx=20,fill="both",expand=True)
        self.exibir_tarefas()
        self.janela.mainloop()
    def exibir_tarefas(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        if not self.tarefas:
            ctk.CTkLabel(self.frame_lista,text='nenhuma tarefa encontrada',text_color='white').pack(pady=10,padx=10)
            return
        for i, tarefa in enumerate(self.tarefas):
            frame_tarefa=ctk.CTkFrame(self.frame_lista)
            frame_tarefa.pack(pady=5,padx=10,fill="x")
            ver_checkbox=ctk.IntVar(value=1 if tarefa['concluida'] else 0)
            checkbox=ctk.CTkCheckBox(frame_tarefa,text='',variable=ver_checkbox,
                                     command=lambda idx=i: self.toggle_tarefa(idx),width=30)
            checkbox.pack(side='left',padx=5)
            
            frame_texto=ctk.CTkFrame(frame_tarefa,fg_color='transparent')
            frame_texto.pack(side='left',fill="x",expand=True)
            estilo_fonte=('arial',12,'bold')
            if tarefa['concluida']:
                estilo_fonte=('arial',12,'overstrike')
            nome_tarefa=ctk.CTkLabel(frame_texto,
                                     text=tarefa['nome'],
                                     font=estilo_fonte,
                                     text_color='white' if tarefa['concluida'] else 'gray',anchor='w')
            nome_tarefa.pack(anchor='w')
            info=ctk.CTkLabel(frame_texto,
                                  text=self.tarefas[i]['info'],
                                  font=('arial',10),
                                  text_color='white' if tarefa['concluida'] else 'gray',anchor='w',
                                  wraplength=350)
            info.pack(anchor='w')
            data=ctk.CTkLabel(frame_texto,
                              text=self.tarefas[i]['data'],
                              font=('arial',10),
                              text_color='red' if tarefa['concluida'] else 'gray',anchor='w',
                              wraplength=300)
            data.pack(anchor='w')
            boton_excluir=ctk.CTkButton(frame_tarefa,
                                        text='excluir',
                                        command=lambda idx=i: self.excluir_tarefa(idx),
                                        fg_color='red')
            boton_excluir.pack(side='right',padx=5)
    def toggle_tarefa(self,indice):
        self.tarefas[indice]['concluida']=not self.tarefas[indice]['concluida']
        self.salvar_tarefas(self.tarefas)
        self.exibir_tarefas()
    def excluir_tarefa(self,indice):
        del self.tarefas[indice]
        self.salvar_tarefas(self.tarefas)
        self.exibir_tarefas()
    
    def limpar_tela(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    def new_task(self):
        self.limpar_tela()
        self.title=ctk.CTkLabel(self.frame_principal,
                                text='nova tarefa',
                                font=('arial',12),
                                text_color='white')
        self.title.pack(pady=10,padx=10)
        
        frame_entrada =ctk.CTkFrame(self.frame_principal)
        frame_entrada.pack(pady=10,padx=20,fill="x")
        
        self.nome_tarefa=ctk.CTkEntry(frame_entrada,placeholder_text='nome da tarefa',text_color='white')
        self.nome_tarefa.pack(pady=10,padx=10)
        
        self.info=ctk.CTkTextbox(frame_entrada,height=100,font=('arial',10))
        self.info.pack(pady=10,padx=10,fill="x")
        
        self.data_entry=ctk.CTkEntry(self.frame_principal,placeholder_text='data (dd/mm/aaaa)',width=200)
        self.data_entry.pack(pady=10,padx=10)
        self.data_entry.bind('<KeyRelease>',self.formatar_data)
        
        frame_butao=ctk.CTkFrame(self.frame_principal,fg_color='transparent')
        frame_butao.pack(pady=10,padx=20,fill="x")

        butao_salvar=ctk.CTkButton(frame_butao,text='salvar tarefa',command=self.criar_arquivo,fg_color='green')
        butao_salvar.pack(pady=10,padx=10,fill="x")
        
        butao_cancelar=ctk.CTkButton(frame_butao,text='cancelar',command=self.interface,fg_color='red')
        butao_cancelar.pack(pady=10,padx=10,fill="x")
    
    def formatar_data(self,event):
        texto=self.data_entry.get()
        apenas_numeros=''.join(filter(str.isdigit,texto))
        if len(apenas_numeros)>8:
            apenas_numeros=apenas_numeros[:8]
        data_formatada=''
        for i, digito in enumerate(apenas_numeros):
            if i==2 or i==4:
                data_formatada+='/'
            data_formatada+=digito
        self.data_entry.delete(0, 'end')
        self.data_entry.insert(0, data_formatada)
    def criar_arquivo(self):
        nome=self.nome_tarefa.get().strip()
        info=self.info.get("1.0","end").strip()
        data=self.data_entry.get().strip()
        if not data:
            data=datetime.datetime.now().strftime("%d/%m/%Y")
        data_atual=datetime.datetime.now().strftime("%d/%m/%Y")
        if data == data_atual:
            from winotify import Notification
            notificacao = Notification(
            app_id='To Do List',
            title='Tarefa para hoje!', 
            msg=f'Você tem uma tarefa: {nome}', 
            duration='short',
            icon='C:/Users/fledson/Downloads/icon.ico'                            )
            notificacao.show()
        if not nome:
            ctk.CTkLabel(self.frame_principal,text='o nome da tarefa é obrigatório',text_color='red').pack(pady=10,padx=10)
            self.frame_principal.after(2000,self.interface)
            return
        
        nova_tarefa={
            'nome':nome,
            'info':info,
            'data':data,
            'concluida':False
        }
        self.tarefas.append(nova_tarefa)
        self.salvar_tarefas(self.tarefas)
        return self.voltar_pricipal()
    def voltar_pricipal(self):
        self.limpar_tela()
        self.interface()
App() 