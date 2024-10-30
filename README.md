# Integracja GRYF SMART z home assistant

## 🌟 **Nowe możliwości integracji Gryf Smart z Home Assistant** 🌟

Integracja **Gryf Smart** z **Home Assistant** wynosi Twój inteligentny dom na nowy poziom, dając pełną kontrolę nad sprzętami RTV i AGD oraz oferując szeroki wachlarz zaawansowanych funkcji. Sprawdź, co możesz zyskać:

---

#### 🎛️ **Wsparcie dla urządzeń RTV i AGD**

Dzięki integracji zyskujesz dostęp do sterowania urządzeniami, które wcześniej były trudniejsze do połączenia z systemami smart home, w tym:

- **Telewizory**
- **Pralki**
- **Lodówki**
- **Zmywarki**

To daje pełną kontrolę nad sprzętem i **monitorowanie ich pracy w czasie rzeczywistym**.

---

#### ⚙️ **Zaawansowane scenariusze automatyzacji**

Twórz własne, **spersonalizowane automatyzacje** i scenariusze, które ułatwią codzienne czynności:

- 🕒 **Uruchamiaj pralkę** o wybranej porze,
- 🌞 **Dostosowuj jasność telewizora** w zależności od pory dnia.

Integracja pozwala na połączenie urządzeń z **czujnikami ruchu** czy **oświetleniem**, co otwiera nowe możliwości w Twoim inteligentnym domu.

---

#### 📊 **Rozbudowane dashboardy**

Gryf Smart umożliwia tworzenie **pięknych, intuicyjnych dashboardów**, które wyświetlają stan i status urządzeń na jednym ekranie. Możesz dopasować wygląd i układ informacji, by **monitorować kluczowe parametry**, takie jak:

- 🧺 **Status prania**,
- ❄️ **Temperatura lodówki**.

Wszystko po to, by zarządzanie urządzeniami było **proste i przyjemne**.

---

#### 🌐 **Dostęp zdalny i powiadomienia**

Dzięki integracji możesz:

- **Otrzymywać powiadomienia** o stanie urządzeń na urządzenia mobilne, co zwiększa **bezpieczeństwo** i **wygodę**.
- **Zdalnie kontrolować urządzenia** — np. wyłączyć telewizor, jeśli zapomniałeś to zrobić, wychodząc z domu.

Idealne rozwiązanie dla tych, którzy cenią sobie **pełną kontrolę** w każdej chwili.

---

💡 Integracja Gryf Smart z Home Assistant to krok w stronę **bardziej funkcjonalnego** i **oszczędnego domu**, zapewniając zaawansowane zarządzanie sprzętem oraz automatyzację codziennych zadań.

## Konfiguracja

#### integracja home assistanta wspiera całą masę urządzeń:

* Urządzenia podpinane pod wyjścia przekaźnikowe (O)
  1. lights - lampki albo zwykle wyjscia do zastosowania własnego
  2. lock - zamek w drzwiach
  3. climate - element wykonawczy regulatora
* Urządzenia podpinane pod wejścia (I)
  1. buttons - przyciski , panel (wspierają krótkie i długie naciśnięcie)

     ```
     stan encji odpowiadających tym przyciską to :
         0 - stan 0
         1 - stan 1
         2 - krótkie naciśnięcie
         3 - długie naciśnięcie 
     ```
  2. doors - kontraktrony w drzwiach
  3. windows - kontraktrony w oknach
* urządzenia podpinane pod złączna temperaturowe (TEMP)
  1. temperature - klasyczny termometr z wykresem
  2. climate - element pomiarowy regulatora

## Schemat wpisywania konfiguracji 

#### wrzystkie encje do utworzenia wpisujemy w pliku configuration.yaml. Naszą integracje deklarujemy nazwą gryf_smart.

```
gryf_smart:
  port: "/dev/ttyS0"
  ...
