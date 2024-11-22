# Funkcja obliczająca przeliczenie euro na złotówki
def przelicz_na_zlotowki(euro, kurs):
    return euro * kurs

# Główna funkcja programu
def main():
    print("Kalkulator Walutowy: Euro na Złotówki")
    
    # Pobieranie kursu wymiany od użytkownika
    try:
        kurs = float(input("Podaj aktualny kurs wymiany euro na złotówki: "))
    except ValueError:
        print("Proszę podać prawidłowy kurs.")
        return

    # Pobieranie kwoty w euro od użytkownika
    try:
        euro = float(input("Podaj kwotę w euro: "))
    except ValueError:
        print("Proszę podać prawidłową kwotę w euro.")
        return
    
    # Obliczanie przeliczenia
    zlotowki = przelicz_na_zlotowki(euro, kurs)
    
    # Wyświetlanie wyniku
    print(f"{euro} EUR to {zlotowki:.2f} PLN.")
    
# Uruchomienie programu
if __name__ == "__main__":
    main()
