from abc import ABC, abstractmethod
from datetime import datetime

class Bicikli(ABC):
    def __init__(self, tipus, ar, allapot) -> None:
        self.tipus=tipus
        self.ar=ar
        self.allapot=allapot
        self.kolcsonzesek = []

    def szabad_e(self, kezdo_datum, veg_datum):
        for kolcsonzes in self.kolcsonzesek:
            if not (datetime.strptime(kolcsonzes.veg_datum,'%Y-%m-%d') < kezdo_datum or datetime.strptime(kolcsonzes.kezdo_datum,'%Y-%m-%d') > veg_datum):
                return False
        return True

    def kolcsonzes_lemond(self,tipus, kezdo_datum):
        for kolcsonzes in self.kolcsonzesek:
            if datetime.strptime(kolcsonzes.kezdo_datum,'%Y-%m-%d') == kezdo_datum and self.tipus==tipus:
                self.kolcsonzesek.remove(kolcsonzes)

    def kolcsonoz(self, kezdo_datum, veg_datum):
        if self.szabad_e(kezdo_datum, veg_datum):
            self.kolcsonzesek.append(Kolcsonzes(self,kezdo_datum,veg_datum))
            return f"A {self.tipus} bicikli kölcsönözve lett {kezdo_datum} - {veg_datum}."
        else:
            return f"A {self.tipus} bicikli már ki lett kölcsönözve ebben az időszakban."
        pass

    def kolcsonzes_datumok(self):
        kolcsonzesek_str_list = []
        for kolcsonzes in self.kolcsonzesek:
            if isinstance(kolcsonzes.kezdo_datum,datetime):
                kezdo_datum_str = datetime.strftime(kolcsonzes.kezdo_datum,'%Y-%m-%d')
            else:
                kezdo_datum_str = kolcsonzes.kezdo_datum
            if isinstance(kolcsonzes.veg_datum,datetime):
                veg_datum_str = datetime.strftime(kolcsonzes.veg_datum,'%Y-%m-%d')
            else:
                veg_datum_str = kolcsonzes.veg_datum
            kolcsonzes_ara=self.ar*(datetime.strptime(veg_datum_str,'%Y-%m-%d')-datetime.strptime(kezdo_datum_str,'%Y-%m-%d')).days
            kolcsonzesek_str_list.append(f"{kezdo_datum_str} - {veg_datum_str}, ár: {kolcsonzes_ara}")
        return ", ".join(kolcsonzesek_str_list)

    @abstractmethod
    def __str__(self):
        pass

class OrszagutiBicikli(Bicikli):
    def __str__(self):
        kolcsonzesek_str = self.kolcsonzes_datumok()
        return f"Országúti bicikli. A bicikli típusa: {self.tipus}, Ár: {self.ar}, Kölcsönzések: {kolcsonzesek_str if kolcsonzesek_str else 'Nincsenek kölcsönzések'}"

class HegyiBicikli(Bicikli):
    def __str__(self):
        kolcsonzesek_str = self.kolcsonzes_datumok()
        return f"Hegyi bicikli. A bicikli típusa: {self.tipus}, Ár: {self.ar}, Kölcsönzések: {kolcsonzesek_str if kolcsonzesek_str else 'Nincsenek kölcsönzések'}"

class Kolcsonzo:
    def __init__(self,kolcsonzonev) -> None:
        self.biciklik=[]
        self.kolcsonzonev=kolcsonzonev

    def bicikli_hozzaadas(self, bicikli: Bicikli):
        self.biciklik.append(bicikli)

    def adatfeltoltes(self):
        self.bicikli_hozzaadas(OrszagutiBicikli('KTM', 15000, 'Használt'))
        self.bicikli_hozzaadas(HegyiBicikli("Gepida", 16000, 'Új'))
        self.bicikli_hozzaadas(HegyiBicikli("Kross", 14000, 'Új'))
        self.bicikli_hozzaadas(HegyiBicikli("Kellys", 15500, 'Új'))
        self.bicikli_hozzaadas(HegyiBicikli("Trek", 14500, 'Használt'))

        self.kolcsonzes('Gepida','2023-12-10','2023-12-15')
        self.kolcsonzes('Kross','2023-12-10','2023-12-13')
        self.kolcsonzes('Kellys','2023-12-10','2023-12-11')

    def kolcsonzesek_lekerdezese(self):
        return '\n'.join(str(bicikli) for bicikli in self.biciklik)

    def kolcsonzes(self, tipus, kezdo_datum, veg_datum):
        for bicikli in self.biciklik:
            if bicikli.tipus == tipus:
                return bicikli.kolcsonoz(kezdo_datum, veg_datum)
        return "Bicikli nem található."
    
    def lemondas(self, tipus, kezdo_datum):
        for bicikli in self.biciklik:
            if bicikli.tipus == tipus:
                return bicikli.kolcsonzes_lemond(tipus, kezdo_datum)
        return "Bicikli nem található."

class Kolcsonzes:
    def __init__(self, bicikli, kezdo_datum, veg_datum) -> None:
        self.bicikli=bicikli
        self.kezdo_datum=kezdo_datum
        self.veg_datum=veg_datum

# Főprogram
def kolcsonzesi_folyamat(kolcsonzo: Kolcsonzo):
    kolcsonzo.adatfeltoltes()

    while True:
        valasztas = input("Mit szeretne tenni? (kolcsonzes, lemondas, listazas, kilep): ")
        if valasztas == "listazas":
            print(kolcsonzo.kolcsonzesek_lekerdezese())
        elif valasztas == "kolcsonzes":
            tipus = input("Adja meg a típust: ")
            kezdo_datum_str = input("Adja meg a kezdő dátumot (yyyy-mm-dd): ")
            veg_datum_str = input("Adja meg a végső dátumot (yyyy-mm-dd): ")
            kezdo_datum = datetime.strptime(kezdo_datum_str, '%Y-%m-%d')
            veg_datum = datetime.strptime(veg_datum_str, '%Y-%m-%d')
            print(kolcsonzo.kolcsonzes(tipus, kezdo_datum, veg_datum))
        elif valasztas == "lemondas":
            tipus = input("Adja meg a típust: ")
            kezdo_datum_str = input("Adja meg a kezdő dátumot (yyyy-mm-dd): ")
            kezdo_datum = datetime.strptime(kezdo_datum_str, '%Y-%m-%d')
            print(kolcsonzo.lemondas(tipus, kezdo_datum))
        elif valasztas == "kilep":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás.")

kolcsonzo = Kolcsonzo("Bike Corner")
kolcsonzesi_folyamat(kolcsonzo)
