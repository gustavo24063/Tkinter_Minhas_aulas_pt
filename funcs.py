import sqlite3
class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.nome_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)               
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def add_cliente(self):
        self.variaveis()
        if self.nome_entry.get() == "":
            msg = "Para cadastrar um novo cliente é necessário \n"
            msg += "que seja digitado pelo menos um nome"
            messagebox.showinfo("Cadastro de clientes - Aviso!!!", msg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_cliente()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """,
                            (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()
    def images_base64(self):
        self.btnovo_base64 = 'R0lGODlhcAAzAOf8AA0fRBcoRB4nVCMlXhcrThAuYxctWBQveQU+IwRAFSM0URI2eA5FDCs4PSA6YxM8kDA6Sg5PCRlDix1DgytAeiFEewxUGRFWJhdKqBNVNQ9XQxxKtS9KdDhKWQhfEh1Noj1LUEVIWipVJTpLaAJmAiZRmihSkj1VRi5UiyBUxQxqHCBarzNYgkRWgU5Wa0xWczVZsUNadhpgxyRevURbbypfqVBZZVJZYDFenztbpgt2JRxuTDhglxR1OgR9GSxlujduNxl0YkljkF5hY09kdzdqkgKHEVVlhCF3dmBleRiCMSVw2kZptF9odT1zdixyyD5utzNytixy0S95kFB0U0Vwq01yjWVudFBwrRCTHHBucj95r0J6oBmRLGlyfyeLS1p0oGVzk2lziB+TPjCD5TaLejKJrkeMWD6RQ1SCyDmJ4laA5D6J2D+PkESRa0iIyVCIrW+BlWqCn3R/oGSDsFCJvneCj3yAl2aGv4CBo4GGiFWRqmKOoYKJkGuL4zOsO0eX8lSYxC2uUlCY222adVaa1FSfomCavIyPpIOSonOVxH+TslCe7XOV11af01qoWkqtWkurhZKWmVGudZyat3CmzmOsxGOr1Vms7mGr32Gt55ugt0PEUZmiqZOjtXypxo+h44arkn+o4Xe0gU3EY4irumu0vWu3oX+r60vGdI6tpmm16V3FeHPAeZms3nC2/5Gv2qSq32+81KSs0Ziw0WDIiWu95Hi55m+/9aG0x46296yxyXjHiq2zvErYeHPJm32/+LS0tLeyzYjHk3bG8HnI4ai9uoTH0GrWiXzSiXjL66HGnMO8tbHB2KDKs73A1bPC5cHBw7zCy7bE0srBtILam6zG887FuJjZn5nYq8nHytDJwq7R7c/M6cbR6MbS4MLU2s/S3LjdysnY1cHY+7ngvsvbx7vjsaHuptza2OzX3dff99ji6t3i8uLi7NDn+a/3urj3y+js7Ont+fXq/dP53dL70eX14fzv9eP3/+D66vD2//Xp6fXp6fXp6fXp6SH+EUNyZWF0ZWQgd2l0aCBHSU1QACwAAAAAcAAzAAAI/gC9sRtIkOCzXc2gNdtVqmGpTw4d0ppIC9YsWBgzwvqkMeNEjRRDfozlkZank55KbZrYqFFFja5cYfxEE2KuZt0K6tzJk903cLtyeZpzpEWLGEiRsmCRNMbSp1BZGOVAtepSpxxYVO3AtYODrw6ohh1BtizZqlSbol3L4Qiiad96yi3o7ZuwRUWN6t1rlCnSFk9jtCAi9a9To03VcjA7AuzYxYzPovXrN+vSFlTLJkm0Ca7AuTvr7spzRPBeIULAqJbDmvWc13Fiy47dunbt2bhxv37dOg5v273nuH4dJkzRGFRfeLmDKNezuKAH1qUVxyjq62HAzFnEvRTK7+C//m8Cv+jkpk250qefNavZtGbwm82a9l6YsF3sZ6lXLz7X+Yn+UbLIHGFgNgINLyRhxybffCZXXbkUeB1qYHBnIXfgbUJJep5sEtR++52n3i4k7kLfNM/9FE443aTDTjfffBPON9o8I80z7y20iyfpBeVjibtIcyN7c1hxVFlE5DKNg6GB44kcE6Imx4XcbUdleeGNNx4lGf4nopL0PfMMOGI+5w00P9VonzD7eYdlh8Y0dFKPu6w5Cy1zCAHZCDF48gyTBX2zyxwtTAgGHbsJ15pwFlp5pYWePFpeeVyi1+M0a6Io5DPu2Ucieik1NKAhiZSqiioOmZcLifM1kydg/hw4EIYwDYY2jSdRHjrgb8DJkeiUVVqYx5WvLQKshVquuiqJzdwX4nmRGsvHtNOWKgcYcUzbnXc85jILQoromVkYzUBHUDjP5JLndYcKR4dq8K52LXC8KeoaonQMN+Vrwzo656pf+jdetMYmwocc1L7GRxwIT9twd+Vtoh8sdGBGVQuLgMPkN7dGSUe+8YYMb2sjkwxGr3J8zNrJizqKJbQ8EpwIwrVN66gcBlMLhrYXevIRFiygQJUQuTj4TbpFsfuuyEwzfW3TUIdc2yKIDIxSKYtQu/LJfBS7iMrUHsw1Hxd+MhEePKAgtANWmGsXrtdZsVrUdNdt98kuW5jz/rTx6jtgIoqKTLOFZjeCRdoUUDDCJgMd7UnSqGFx9+STz7t1hQM2GjYfUvu6q69PO+3oJ43gUQUKFGgVR1yCVleoEHIfSvnsULf89HZzKMJdw3x3Llwev9Xu63aKlF4FDhQILcY07HCTixAt8BC5akvTDu/H2Ft/PR4fH8J7730jOrzJTbNGhyLo48EEDqi3tQs77SwSvfRCVGH9It7k700p2NPRjP4fa1r/qneoAcJhc4IT324uJzLOTYsOeIggE0zQvjAULRwVi179sCC5kTFtgHTAn/6g0b//5a9/1AMh9ri3NAjCgQ6b49zJWJYyd/EqdPDi2wMjqD61qc2C/t7gBhhYwAMeVKEKHfTg9VQYQv3lj38fM6E3mEhFA8IBDnvYHHAQpSh7kY9pcIhgGqCAg7SZ4AhFmwVginjEJM6tgEzEgyKceCbsSbF/PKyiFemQxbCNzXO/qRcDm4YFPIwxBzgwwRmLBgseEJEJTECiG1MYRznS0Ru0iOAdIRjBT0gRGrP42sdmoT/u1eGK+suFDBexiwadqRkD2pdr6MYHLtQBClXYAgxywINFekMRjuRBDiKJxHjpkYdzzJ8JoXGIQ0iRh3gg5SW98YlDKOIT+stkHeqAzfxljQ9Fm+aTviZKAoaMC3u44hG3kAMoIBIMufjGJ5bCA0i2sYNU/sRDM/fZTUyakBbO1F8z8UAL/TXjmtDQXzUD6o1mBGKbJmxGFkuRSjwsIqHeVAQVc1jLK8LhiFAIaQ1qAE9qLgUFkIwkByWnwn269BD9pEU3v8FQb+wTo8xsZj+b0UyK5u8Q29RfKfawh2XyoXv6mwX6Nqoaj8Jhm9sUaQ2wUDRaCCFo7STmSgeoz5fyM5uV+KcU92lQl7oyp4fQHywCAQsAEjWp/cOpIg7RP6LycQ8fc+pT6/CGOjwBCj/4QUmbAYbkwSCkkdwCFvb6sa569RCW6CcsLiGLEQo0EJXI5j4tgdNAeLagZwoERiV6CBFikq7NxOkAD0HU1jbzqVeE/uob3sCGKAS2pNOQAwpwcFgoMMG3i4XqNj1L3H06IrJqvcQlMOrEQBziEmW1hCWgmz9oOMKzmc1fPz/hXDok1azVZW33HttMOtQBqJ6dLRugYNuSfmMOLMABDn4QUihsQbjDJW4gHLFZR2TXG5Ol7CUdcVyMfsMRyu2nKwh8XeaG96YPhmlZyfvSbaK3EIVgw3oBC88YJYIHJZhvfe9bB8+WeL+e5S+BLXFcUSRXuVL8qXRB6w1XVEIWzK0Egx3RVifSwhLNtASND/oJ5n5CuhTeJ1QDgeFBaJi9UejwN3CFgxr8IAr23QJxMVwI4u74EpVQrovzF2ABO7ESaLZE/oydGGAEE5iO01XuJdQ8TQDLWbpA9mqetzwIJ693C1GOpzdyAQYclODKUoACGzzL5R2vWM5ifjGMzyyKSkwXFg5uhiwgfQkCf5LTc8a0EzUN6jnjGc/KlS6X+0zbNwCaDvFkxzTykIMS1CAKT9DwIJiMYTcTuNTABnUlRDFnBFc62MpFMLKXzew795rVbHB1FGAtkCkLocq43gIbBkHgXiu72cGWBbFZfAlRbBrc6E63nI/baWi/IaRg2IVAwrGLMJgAB7jONbcdnWx1Q7oStpizcm/s74KnuxCDmO27oTCHaeRE1nLgwa1zzQZGMILBl8iEwSEtbktPV9zIzoTG/jdecEckfLZQwMIinkGQacwBBTmIghTYoAaLO2Lk60bwuYXNaYJbYtiikG4lbrHzUouc5CU/+bur4AlzPePl8/0BzS2+Ck2su9OULXrPw5x1jw8bFpXGCNdloXXl4hzp4Bb5ydlLVafnoQUmgMETpFBzRmhC5KtYtyVucQtI513ONyb70L0uClFg5BZczzqnRX52tC+b8SffQhXkIG+DJIIDJljBD2ZecU2swhYiny5/p/tzgZse8GC+RZ6FjuZfQ/rbmbAF6BvveFAzHuGz3YIQEAGOQBF6AjWAAucZkYnPyz7VgZAupJW//Dh7vJnJP4RzwdxvOcde9oynfe0z/n773NsvF+Ggyzd6Ye+Q5roQN5d92dF93eSDGdXAvj72Gb/9xd++EHXYwhaKIAdANW4TR4ADkJQGb3Bzl6B+Wkd21md2R9dprrcKtxBwq/B3oCZ7Fjh72od22ecI+Jd/RVAEs2AuBdENz4AI15ZLb7BfCHaBLNiC84d3jDeBExiDFChnLdiA9Zd9mcCB+AcHXGAFi1ArPCEocrAUKMhkyvaC8seCOiiDxSeDUBiFUch3TuhvGAd7R3d0PHhK+5cIz/Eg07AIYcACRZBLaZAG6HdzOriGTziDeCeFTviGa+iGOJeBzYZ31tdt23RFXLAIsfYg4KAuR1AERoQFb5AG/iroaGyYhRnXiBr3iNy3iGxIcr9mgK+HYXu4Bdrxh3NhF4gQBoSBA1UQUnWAiFvGZWnIYPq1iqyYiI72iq/Ifmq4gxe3Y8KlfxXCiXPhDeCwCXdwBCclikdUBfhVjHiAX3qVjLFVjPllYiUmfYmYbDsmXQSWiClWjfwVCE71g3Ogi6BxNJ3gBUTgAkRwBOZoBeiYjuqYjiGzju74juoIL07lWvvUio+FX3QQCHkFB/BiBXLAIOEXHY0DDsEgCVrgBQjZBERQjuZ4jul4BPCIjkewkAwJkVbQkBjpkHITO2CARXe1B+RFXFCFV1Z0RWBgBWEQB3bQCc8QkALJDiuiNw0FqQd9gJAIKQY4iZPFURw6yZM5mZM3iZM2+ZNEuZO0UTPYQ14gdFRHpTK9ERs4KQm74JKhERAAOw=='
        self.btalterar_base64 = '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'
