# SI Sokrates v0.2

from tkinter import *

class Gracz():
	def __init__(self, imie):
		self.imie = imie
		self.dna = {'arystoteles':0, 'platon':0, 'epikur':0, 'stoik':0, 'sceptyk':0, 'zaden':0}

class Application(Frame):
	""" """
	# baza twierdzen filozoficznych
	baza = []
	# zmienna pozwalająca stopniowo przechodzić przez tematy w bazie
	licznik_bazy = 0
	liczba_graczy = 0
	lista_graczy = []


	# liczba określająca ilość kliknięć, po przekroczeniu których nastąpi zmiana treści tematu pytań
	liczba_klik = 0

	prawda = {
	 		'epikur':'Każde poznanie zmysłowe jest absolutnie prawdziwe.\nBłąd to niewłaściwa interpretacja wrażeń zmysłowych.',
         	'platon':'Prawdę odkrywamy we wnętrzu własnego umysłu.\nPoznanie zmysłowe nie ma większej wartości.',
         	'stoik':'Nasze poznanie zmysłowe, \no ile trwa długo, a zmysły są zdrowe, \n informuje nas o tym, jaki świat jest naprawdę.',
         	'arystoteles':'Stosując odpowiednie metody, możemy poznać świat\n takim,jakim jest.\n Prawda polega na zgodności naszych myśli z rzeczywistością.',
         	'sceptyk':'Każdy człowiek inaczej postrzega i rozumie świat.\nŻaden punkt widzenia\n nie jest uprzywilejowany. \nWszyscy mają rację i wszyscy jej nie mają.',
         	'zaden':'Sorki, ale nic nie pasuje.'
        }

	dobro = {
		'stoik':'Dobro to życie rozumne. Zło to życie nierozumne.\n Życie rozumne to niezależność od dóbr zewnętrznych.',
        'arystoteles':'Dobro w życiu człowieka polega na \npełnym rozwoju swojej natury, wtedy będziemy szczęśliwi.',
       	'sceptyk':'Jedyny sposób na szczęście, to powstrzymać się od formułowania\n jakichkolwiek ocen na jakikolwiek temat. \nNie oceniaj, a będziesz szczęściliwy. ',
        'platon':'Wszystko co jest, jest dobre. Najcenniejsze są dobra duchowe.',
       	'epikur':'Dobro to przyjemność. Przyjemność jest już wtedy, gdy nie ma cierpienia.',
        'zaden':'Co ja poradzę, że nic nie pasuje :(.'
        }

	bog = {
		"platon":"Nie ma Boga. Poza naszym światem \n istnieje boska rzeczywistość.",
		"epikur":"Jeżeli bogowie istnieją, to nie interesują się życiem ludzi.",
		'stoik':'Bóg jest światem, a świat jest Bogiem.\nMy jesteśmy częścią boskiej rzeczywistości.',
		"sceptyk":"Nie ma dowódów na istnienie bóstwa. Nie ma dowódów na nie istnienie bóstwa.\nNajmądrzej będzie, gdy nie przyjmiemy żadnych twierdzeń na ten temat.",
		"arystoteles":"Bóg jest istotą duchową i najdoskonalszą, a cały świat do Niego dąży.",
		"zaden":"Nic z powyższych."}

	czlowiek = {
     		'arystoteles':"Człowiek jest jednością duchowo-cielesną. Człowiek jest wolny i rozumny.",
     		'platon':"Człowiek jest czystym duchem. Ciało jest więzieniem człowieka.",
     		'epikur':"Człowiek jest istotą materialną i śmiertelną.",
    		'stoik':"Człowiek jest częścią natury. Powinien żyć zgodnie prawami \nwyznaczającymi porządek całej rzeczywistości.",
     		'sceptyk':"Nie ma żadnej przekonującej teorii człowieka, \nwięc najlepiej jest nie opowiadać się za żadną teorią.",
     		'zaden':"Myślę zupełnie inaczej niż wszscy wymienieni."}

	spoleczenstwo = {
       		'epikur':'Wszyscy jesteśmy egoistami. W społeczeństwie będzie dobrze się działo,\n gdy ludzie będą rozumnymi egoistami.',
       		'sceptyk':'Prawda jest niepoznawalna, więc w życiu społecznym najważniejsze jest\nwskazywanie tego, co jest fałszywe.',
      		'platon':'Każdy aspekt życia człowieka powinien być kontrolowany przez\n mędrców/ekspertów, wówczas będzie nam się żyło szczęśliwie.',
     		'stoik':'Społeczeństwo to organiczna całość. Wzajemnie od siebie zależymy. \nIdeałem jest społeczeństwo ogólnoludzkie.',
     		'arystoteles':'Nie tyle ustój jest ważny, ile to, aby władza\ndbała o dobro wspólne, a nie o własne.',
     		'zaden':'Nic nie pasuje.'}

	baza.append(czlowiek)
	baza.append(bog)
	baza.append(spoleczenstwo)
	baza.append(dobro)
	baza.append(prawda)
	ilosc_pytan=len(baza)
	# inicjalizacja frame
	def __init__(self,master):
		super(Application,self).__init__(master)

		self.create_widgets()

	def utworzenie_graczy(self):
		#atrybut okna przechowujący listę graczy

		if Application.liczba_graczy > 0:
			Application.lista_graczy.append(Gracz(self.entry_str_graczy.get()))
			self.pole_txt.delete(0.0,END)
			self.pole_txt.insert(0.0, self.entry_str_graczy.get() + " został przyjęty do gry.\n")
			Application.liczba_graczy-=1
			self.entry_str_graczy.delete(0, END)

		if Application.liczba_graczy == 0:
			Application.liczba_graczy=len(Application.lista_graczy)
			self.pole_txt.delete(0.0,END)
			lista = ""
			for gracz in Application.lista_graczy:
				lista += '\n' + gracz.imie
			self.pole_txt.insert(0.0, "\n\nZaczyna " + Application.lista_graczy[0].imie)
			self.pole_txt.insert(0.0, "Będą grali " + lista)
			self.btn_imie_gracza.config(state=DISABLED)
			self.entry_str_graczy.delete(0, END)
			self.entry_str_graczy.config(state=DISABLED)

			self.tworzenie_przyciskow(Application.baza[Application.licznik_bazy])
			self.dalej = Button(self, text = 'Dalej', command = self.aktualizacja).grid(
					row=12,column=1,sticky=W, padx=55, pady=10)


	def licz_graczy(self):
		Application.liczba_graczy = int(self.entry_int_graczy.get())
		self.pole_txt.delete(0.0,END)
		self.pole_txt.insert(0.0,"Liczba graczy:\t"
					+ str(Application.liczba_graczy))
		self.btn_liczba_graczy.config(state=DISABLED)
		self.entry_int_graczy.delete(0, END)
		self.entry_int_graczy.config(state=DISABLED)

	def create_widgets(self):
		self.pack(fill=BOTH,expand = 1)
		self.columnconfigure(1,weight=1)
		self.config(relief=SUNKEN)

		Label(self,text="Analizator starożytnego DNA filozoficznego").grid(
					row = 0, column = 0, columnspan = 1, sticky = N, padx=5, pady=4)
		Label(self,text="Wybierz jedną odpowiedź NAJBARDZIEJ PASUJĄCĄ do twoich poglądów:").grid(
					row = 1, column = 0, columnspan = 1, padx=5, pady=4, sticky=W)



		self.pole_txt=Text(self, width=30,height=15, wrap=WORD,)
		self.pole_txt.grid(row=1,column=2,columnspan=3, rowspan = 20, padx=50,pady=10)

		self.pole_txt.delete(0.0,END)
		self.pole_txt.insert(0.0,"Do przemyślenia będzie "
					+ str(Application.ilosc_pytan) + " zagadnień.")
		#############################
		Label(self,text="Ilość graczy").grid(
					row = 22, column = 0, sticky=E, padx=10,pady=2)
		Label(self,text="Nazwy graczy:").grid(
					row = 24, column = 0,  sticky=E, padx=10,pady=2)
		self.entry_int_graczy = Entry(self)
		self.entry_int_graczy.grid(row=23,column=0,sticky=E, padx=10,pady=2)
		self.entry_str_graczy = Entry(self)
		self.entry_str_graczy.grid(row=25,column=0,sticky=E, padx=10,pady=2)
		self.btn_liczba_graczy = Button(self)
		self.btn_liczba_graczy.config(text = 'Potwierdź ilość', command = self.licz_graczy)
		self.btn_liczba_graczy.grid(
						row=23,column=1,sticky=W)
		self.btn_imie_gracza = Button(self)
		self.btn_imie_gracza.config(text = 'Wprowadź nazwę gracza',command = self.utworzenie_graczy)
		self.btn_imie_gracza.grid(row=25,column=1,sticky=W)

		# tworzenie listy, której elementami są obiekty klasy Radiobutton
		self.btns = []
		for i in range(6):
			self.btns.append(Radiobutton(self))


		# wypełnianie treścią obiektów klasy Radionbutton
		# Pobieranie informacji z pierwszego elementu(słownika) bazy
		# przeniosłem do funkcji twórz graczy



	def tworzenie_przyciskow(self, baza_wiedzy):
		self.wartosc_wyboru = StringVar()
		self.wartosc_wyboru.set(None)
		rzad=3
		button=0
		for szkola, teza in baza_wiedzy.items():
			self.btns[button]["text"] = teza
			self.btns[button]["variable"] = self.wartosc_wyboru
			self.btns[button]["value"] = szkola
			self.btns[button].grid(
				row=rzad, column=0, columnspan=2,rowspan=1,padx=1,pady=3, sticky=W)
			rzad+=1
			button+=1


	def aktualizacja(self):
		if Application.liczba_klik < Application.liczba_graczy-1:
			for szkola in Application.lista_graczy[Application.liczba_klik].dna:
				if szkola in self.wartosc_wyboru.get():
					Application.lista_graczy[Application.liczba_klik].dna[szkola]+=20
			self.wartosc_wyboru.set(None)
			self.pole_txt.delete(0.0,END)
			Application.liczba_klik+=1
			self.pole_txt.insert(0.0, "\nTeraz gra "
						+ Application.lista_graczy[Application.liczba_klik].imie )

		elif Application.liczba_klik == Application.liczba_graczy-1:
			for szkola in Application.lista_graczy[Application.liczba_klik].dna:
				if szkola in self.wartosc_wyboru.get():
					Application.lista_graczy[Application.liczba_klik].dna[szkola]+=20
			self.wartosc_wyboru.set(None)
			self.pole_txt.delete(0.0,END)
			Application.liczba_klik=0
			Application.licznik_bazy+=1
			Application.ilosc_pytan-=1
			self.pole_txt.insert(0.0, "\nNowe ZAGADNIENIE!!\n Pozostało: "
						+ str(Application.ilosc_pytan)
						+".\n"
						+ "\nGra: " + Application.lista_graczy[Application.liczba_klik].imie)
			if Application.licznik_bazy == 5:
				return self.koniec()

			self.tworzenie_przyciskow(Application.baza[Application.licznik_bazy])


	def koniec(self):
		wynik = ""
		self.pole_txt.delete(0.0,END)
		for gracz in Application.lista_graczy:
			for szkola in gracz.dna:
				if gracz.dna[szkola] > 0:
					if szkola == 'zaden':
						wynik += 'nic starożytnego ' + ': \t\t\t' + str(gracz.dna[szkola]) + ' %\n'
					else:
						wynik += szkola + ': \t\t\t' + str(gracz.dna[szkola]) + ' %\n'
			self.pole_txt.insert(0.0, 'Oto wynik gracza: ' + gracz.imie + '\n' + wynik + '\n')
			wynik = ""






#MAIN
root=Tk()
root.title("SI 'Sokrates'")
root.geometry("1100x550")

app=Application(root)

root.mainloop()
