import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import mysql
import pandas as pd
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Configuração da conexão com o banco de dados MySQL

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",     
        database="receitas_db"
    )

#CRUD - create, read, update, delete

def inserir_receita(nome, ingredientes, modo, tempo, dificuldade, foto):
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        INSERT INTO receitas (nome, ingredientes, modo_preparo, tempo, dificuldade, foto)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, ingredientes, modo, tempo, dificuldade, foto))
    conn.commit()
    conn.close()

def listar_receitas():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM receitas", conn)
    conn.close()
    return df

def atualizar_receita(id, nome, ingredientes, modo, tempo, dificuldade, foto):
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        UPDATE receitas
        SET nome=%s, ingredientes=%s, modo_preparo=%s, tempo=%s, dificuldade=%s, foto=%s
        WHERE id=%s
    """
    cursor.execute(sql, (nome, ingredientes, modo, tempo, dificuldade, foto, id))
    conn.commit()
    conn.close()

def excluir_receita_bd(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receitas WHERE id=%s", (id,))
    conn.commit()
    conn.close()


#Cores do tema
COR_FUNDO = "#7302AF"
COR_CARD = "#7343DC"
COR_BOTAO = "#4A98E2"
COR_BOTAO_HOVER = "#357ABD"
COR_TEXTO = "#FFFFFF"

#Botão estilizado
def botao_estilizado(master, texto, comando):
    btn = tk.Button(
        master,
        text=texto,
        command=comando,
        font=("Arial", 12, "bold"),
        bg=COR_BOTAO,
        fg="white",
        activebackground=COR_BOTAO_HOVER,
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=7
    )
    return btn


#Janela principal
janela = tk.Tk()
janela.title("🍽️ App de Receitas - MySQL")
janela.geometry("450x300")
janela.configure(bg=COR_FUNDO)

tk.Label(janela, text="🍽️ App de Receitas", font=("Arial", 22, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)
tk.Label(janela, text="Gerencie suas receitas com facilidade!", font=("Arial", 12), bg=COR_FUNDO).pack()



tk.Label(janela, text="Desenvolvido por Beatriz C. Haberman Severo Alves", font=("Arial", 10), bg=COR_FUNDO).pack(side="bottom", pady=10)



# FUNÇÕES DA INTERFACE

#exibir imagem ao clicar
def abrir_imagem(url):
        try:
            resp = requests.get(url)
            img = Image.open(BytesIO(resp.content))
            img = img.resize((350, 350))
            imgTk = ImageTk.PhotoImage(img)


            janela_img = tk.Toplevel(janela)
            janela_img.title("Foto da Receita")
            lbl = tk.Label(janela_img, image=imgTk)
            lbl.image = imgTk
            lbl.pack()


        except:
            messagebox.showerror("Erro", "Não foi possível carregar a imagem.")
#Tela de Cadastro

def abrir_tela_cadastro():
    cadastro = tk.Toplevel(janela)
    cadastro.title("Cadastrar Receita")
    cadastro.geometry("450x600")
    cadastro.configure(bg=COR_FUNDO)

    card = tk.Frame(cadastro, bg=COR_CARD, bd=2, relief="groove")
    card.pack(pady=20, padx=20, fill="both")

    tk.Label(card, text="Cadastrar Nova Receita", font=("Arial", 16, "bold"), bg=COR_CARD).pack(pady=15)

    def criar_label_entrada(texto):
        tk.Label(card, text=texto, font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
        entrada = tk.Entry(card, width=40)
        entrada.pack(pady=5)
        return entrada

    e_nome = criar_label_entrada("Nome")
    e_tempo = criar_label_entrada("Tempo (min)")
    e_foto = criar_label_entrada("Foto (URL)")

    tk.Label(card, text="Ingredientes", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
    e_ing = tk.Text(card, height=4, width=40)
    e_ing.pack(pady=5)

    tk.Label(card, text="Modo de Preparo", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
    e_modo = tk.Text(card, height=4, width=40)
    e_modo.pack(pady=5)

    tk.Label(card, text="Dificuldade", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
    cb_dif = ttk.Combobox(card, values=["Fácil", "Médio", "Difícil"], state="readonly")
    cb_dif.pack(pady=5)

    tk.Label(cadastro, text="Foto (URL)").pack()
    e_foto = tk.Entry(cadastro, width=40)
    e_foto.pack()

    def salvar():
        inserir_receita(
            e_nome.get(),
            e_ing.get("1.0", tk.END),
            e_modo.get("1.0", tk.END),
            e_tempo.get(),
            cb_dif.get(),
            e_foto.get()
        )
        messagebox.showinfo("OK", "Receita cadastrada com sucesso!")
        cadastro.destroy()

    botao_estilizado(card, "Salvar Receita", salvar).pack(pady=20)



 
    #Tela de Listagem

def abrir_tela_listagem():
    lista = tk.Toplevel(janela)
    lista.title("Receitas Cadastradas")
    lista.geometry("900x500")
    lista.configure(bg=COR_FUNDO)

    tk.Label(lista, text="Receitas Cadastradas", font=("Arial", 18, "bold"), bg=COR_FUNDO, fg="white").pack(pady=10)

    # FRAME DA TABELA
    frame_tabela = tk.Frame(lista)
    frame_tabela.pack(pady=10)

    df = listar_receitas()

    tabela = ttk.Treeview(frame_tabela, columns=list(df.columns), show="headings", height=10)
    tabela.pack(side="left", fill="both", expand=True)

    # FRAME DA IMAGEM
    frame_img = tk.Frame(lista, bg=COR_FUNDO)
    frame_img.pack(side="right", fill="both", padx=20)

    lbl_img = tk.Label(frame_img, text="Selecione uma receita", bg=COR_FUNDO, fg="white")
    lbl_img.pack()

    #
    def mostrar_foto(event=None):
        item = tabela.selection()
        if not item:
            return

        valores = tabela.item(item)["values"]
        url = valores[-1]   # última coluna = foto

        foto = carregar_imagem(url)

        if foto:
            lbl_img.config(image=foto, text="")
            lbl_img.image = foto
        else:
            lbl_img.config(text="Imagem não disponível", image="")

    def abrir_detalhes_duplo_click(event):
        item = tabela.selection()
        if item:
            dados = tabela.item(item, "values")
        abrir_tela_detalhes(dados)

    tabela.bind("<Double-1>", abrir_detalhes_duplo_click)




    # Configurar colunas
    for col in df.columns:
        tabela.heading(col, text=col)
        tabela.column(col, width=120)

    # Preencher tabela
    for _, row in df.iterrows():
        tabela.insert("", tk.END, values=list(row))

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

  
    # FUNÇÃO DE EDITAR RECEITA
    
    def editar_receita():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma receita para editar!")
            return
        
        item = item[0]
        dados = tabela.item(item, "values")
        abrir_tela_editar(dados)

   
    # FUNÇÃO DE EXCLUIR RECEITA
 
    def excluir_receita():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma receita para excluir!")
            return
        
        item = item[0]
        dados = tabela.item(item, "values")
        id_rec = dados[0]

        confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta receita?")
        if not confirmar:
            return

        excluir_receita_bd(id_rec)  
        tabela.delete(item)
        messagebox.showinfo("OK", "Receita excluída com sucesso!")

    
    # ÁREA DE FILTROS
   
    frame_filtro = tk.Frame(lista, bg=COR_FUNDO)
    frame_filtro.pack(pady=20)

    tk.Label(frame_filtro, text="Buscar por Nome:", bg=COR_FUNDO, fg="white").grid(row=0, column=0, padx=5)
    e_busca = tk.Entry(frame_filtro, width=25)
    e_busca.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtro, text="Dificuldade:", bg=COR_FUNDO, fg="white").grid(row=1, column=0, padx=5)
    cb_dif = ttk.Combobox(frame_filtro, values=["Todos", "Fácil", "Médio", "Difícil"], state="readonly")
    cb_dif.set("Todos")
    cb_dif.grid(row=1, column=1, padx=5)

    # FUNÇÃO APLICAR FILTROS
    def aplicar_filtros():
        df = listar_receitas()

        nome = e_busca.get().strip()
        if nome:
            df = df[df["nome"].str.contains(nome, case=False)]

        dif = cb_dif.get()
        if dif != "Todos":
            df = df[df["dificuldade"] == dif]

        tabela.delete(*tabela.get_children())

        for _, row in df.iterrows():
            tabela.insert("", tk.END, values=list(row))

    
    # BOTÕES (LADO A LADO)
    
    botao_estilizado(frame_filtro, "Aplicar Filtros", aplicar_filtros).grid(row=2, column=0, pady=10, padx=5)
    botao_estilizado(frame_filtro, "Editar Receita", editar_receita).grid(row=2, column=1, pady=10, padx=5)
    botao_estilizado(frame_filtro, "Excluir Receita", excluir_receita).grid(row=2, column=2, pady=10, padx=5)


#tela de editar receita
def abrir_tela_editar(dados):
        id_rec = dados[0]
        nome_atual = dados[1]
        ingredientes_atual = dados[2]
        modo_atual = dados[3]
        tempo_atual = dados[4]
        dificuldade_atual = dados[5]
        foto_atual = dados[6]

        editar = tk.Toplevel(janela)
        editar.title("Editar Receita")
        editar.geometry("450x600")
        editar.configure(bg=COR_FUNDO)

        card = tk.Frame(editar, bg=COR_CARD, bd=2, relief="groove")
        card.pack(pady=20, padx=20, fill="both")

        tk.Label(card, text="Editar Receita", font=("Arial", 16, "bold"), bg=COR_CARD).pack(pady=15)

        def criar_label_entrada(texto, valor):
            tk.Label(card, text=texto, font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
            entrada = tk.Entry(card, width=40)
            entrada.insert(0, valor)
            entrada.pack(pady=5)
            return entrada

        e_nome = criar_label_entrada("Nome", nome_atual)
        e_tempo = criar_label_entrada("Tempo (min)", tempo_atual)

        tk.Label(card, text="Ingredientes", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
        e_ing = tk.Text(card, height=4, width=40)
        e_ing.insert("1.0", ingredientes_atual)
        e_ing.pack(pady=5)

        tk.Label(card, text="Modo de Preparo", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
        e_modo = tk.Text(card, height=4, width=40)
        e_modo.insert("1.0", modo_atual)
        e_modo.pack(pady=5)

        tk.Label(card, text="Dificuldade", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
        cb_dif = ttk.Combobox(card, values=["Fácil", "Médio", "Difícil"], state="readonly")
        cb_dif.set(dificuldade_atual)
        cb_dif.pack(pady=5)

        tk.Label(card, text="Foto (URL)", font=("Arial", 11, "bold"), bg=COR_CARD).pack(anchor="w", padx=20)
        e_foto = tk.Entry(card, width=40)
        e_foto.insert(0, foto_atual)
        e_foto.pack(pady=5)

        def salvar_edicao():
            atualizar_receita(
                id_rec,
                e_nome.get(),
                e_ing.get("1.0", tk.END),
                e_modo.get("1.0", tk.END),
                e_tempo.get(),
                cb_dif.get(),
                e_foto.get()
            )
            messagebox.showinfo("OK", "Receita atualizada com sucesso!")
            editar.destroy()

        botao_estilizado(card, "Salvar Alterações", salvar_edicao).pack(pady=20)



# Tela de Detalhes da Receita
def abrir_tela_detalhes(dados):
    id_rec = dados[0]
    nome = dados[1]
    ingredientes = dados[2]
    modo = dados[3]
    tempo = dados[4]
    dificuldade = dados[5]
    foto_url = dados[6]

    detalhes = tk.Toplevel(janela)
    detalhes.title(f"Receita: {nome}")
    detalhes.geometry("600x800")
    detalhes.configure(bg=COR_FUNDO)

    # CARD PRINCIPAL
    card = tk.Frame(detalhes, bg=COR_CARD, bd=2, relief="groove")
    card.pack(pady=20, padx=20, fill="both", expand=True)

    # IMAGEM
    img = carregar_imagem(foto_url)

    if img:
        lbl_img = tk.Label(card, image=img, bg=COR_CARD)
        lbl_img.image = img
        lbl_img.pack(pady=10)
    else:
        tk.Label(card, text="Imagem não disponível", bg=COR_CARD, fg="white").pack(pady=10)

    # NOME
    tk.Label(card, text=nome, font=("Arial", 18, "bold"), bg=COR_CARD, fg="white").pack(pady=10)

    # TEMPO E DIFICULDADE
    tk.Label(card, text=f"Tempo: {tempo} min", font=("Arial", 12), bg=COR_CARD, fg="white").pack()
    tk.Label(card, text=f"Dificuldade: {dificuldade}", font=("Arial", 12), bg=COR_CARD, fg="white").pack()

    # INGREDIENTES
    tk.Label(card, text="Ingredientes:", font=("Arial", 14, "bold"), bg=COR_CARD, fg="white").pack(pady=10)

    txt_ing = tk.Text(card, height=8, width=50)
    txt_ing.insert("1.0", ingredientes)
    txt_ing.config(state="disabled")
    txt_ing.pack(pady=5)

    # MODO DE PREPARO
    tk.Label(card, text="Modo de Preparo:", font=("Arial", 14, "bold"), bg=COR_CARD, fg="white").pack(pady=10)

    txt_modo = tk.Text(card, height=10, width=55)
    txt_modo.insert("1.0", modo)
    txt_modo.config(state="disabled")
    txt_modo.pack(pady=5)


    


#Carregar imagens 

def carregar_imagem(url):
    try:
        resposta = requests.get(url)
        img = Image.open(BytesIO(resposta.content))
        img = img.resize((200, 200))  
        return ImageTk.PhotoImage(img)
    except:
        return None

#Botões na janela principal
botao_estilizado(janela, "Cadastrar Receita", abrir_tela_cadastro).pack(pady=10)
botao_estilizado(janela, "Ver Receitas", abrir_tela_listagem).pack(pady=10)

#Imagem 

#Iniciar a aplicação
janela.mainloop()




