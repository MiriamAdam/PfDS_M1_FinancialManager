# Systembeschreibung Finanzmanager

Die Finanzmanager-Anwendung ermöglicht es Einzelpersonen, ihre Ausgaben und Einnahmen zu dokumentieren.
Mit Hilfe von monatlichen Budgets ist es möglich einzelne Ausgaben-Kategorien zu beschränken. Transaktionen, die das 
gewählte Limit überschreiten würden, werden nicht zugelassen. Grafiken veranschaulichen die aktuelle finanzielle Situation
und es gibt die Möglichkeit, sich Einnahmen und Ausgaben bezogen auf den prozentualen Anteil der Kategorien 
am Gesamtanteil für einen ausgewählten Monat anzeigen zu lassen.

## Userbeschreibung

### Installation

Um die Anwendung zu starten, müssen Backend und Frontend in zwei separaten Terminals gestartet werden.

**Backend**

1. In das Backend-Verzeichnis wechseln:

    > cd backend

2. Eine virtuelle Umgebung erstellen und starten:

   - Windows:
    > python -m venv venv
   >
   > venv\Scripts\activate

    - Mac / Linux:
    > python -m venv venv
   > 
   > source venv/bin/activate

3. Benötigte Programme installieren:

    > npm install -r requirements.txt

4. Wieder in den Hauptordner des Projekts wechseln und das Backend starten:

    > cd ..
   > 
   > python -m backend.app

5. In der Konsole erscheint jetzt das Startmenü. Es muss ausgewählt werden, 
ob die Anwendung (1.) mit leerer Datenbank, (2.) mit neuen Testdaten oder (3.) mit einer bestehenden
Datenbank gestartet werden soll. Bei Auswahl (2.) muss die Anzahl der Jahre, für die Daten erstellt werden sollen angegeben werden.

    >![setup](/assets/setup_menu.png)

**Frontend**

1. In das Frontend-Verzeichnis wechseln:

    > cd react-frontend

2. Programme installieren:

    > npm install

3. Frontend starten:

    > npm run build
   > 
   > npm run preview

**Jetzt kann die Anwendung im Browser über http://localhost:4173/ aufgerufen werden.**

### Anwendungsbeschreibung

Die Anwendung ist auf Englisch und hat vier Pages, die auf der linken Seite in einer horizontalen Navigationsleiste 
ausgewählt werden können.
Auf der Startseite der Anwendung wird eine Übersicht über den aktuellen Finanzstatus angezeigt.
Unter dem Kontostand befindet sich ein tagesaktuelles Liniendiagramm, dass den Verlauf des Kontostands der 
letzten 30 Tage darstellt. Darunter werden die letzten zehn Transaktionen angezeigt.

![overview](/assets/overview_sm.png)

Auf der Seite **Transactions** befindet sich im oberen Bereich ein Formular, mit dem Transaktionen angelegt werden können.
Nach Auswahl der Kategorie kann die passende Unterkategorie ausgewählt und der entsprechende Betrag eingegeben werden.
Mit einem Klick auf *Add transaction* wird die Transaktion entgegengenommen und erscheint als neuste Buchung im darunter
liegenden Fenster. Hier sind alle bisher getätigten Transaktionen von der aktuellsten zur ältesten Buchung aufgelistet. 
Mit dem Formular darüber kann nach Kategorien gefiltert werden.

![transaction menu](/assets/transactions_sm.png)

Befindet man sich auf der Seite **Budgets** sieht man im oberen Bereich, ob schon Budgets für bestimmte Kategorien angelegt
sind. Für jede Kategorie kann genau ein Budget angelegt werden, das die Höhe der Ausgaben für den aktuellen Monat limitiert.
Würde eine neue Transaktion ein gesetztes Budgetlimit überschreiten, kann die Transaktion nicht durchgeführt werden.
Sobald ein bereits bestehendes Budget neu gesetzt wird, wird es überschrieben. Im Fenster daneben können existierende
Budgets gelöscht werden. 

![budgets](/assets/budgets_sm.png)

Auf der Seite **Reports** befinden sich drei Grafiken, die sich dynamisch an die monatlichen Ausgaben anpassen. Das 
oberste Chart ist ein Balkendiagramm. Jeder Balken steht für ein gesetztes Budget. Je nachdem wie viel Geld bezogen auf das 
Budgetlimit bereits ausgegeben wurde, erscheint der Balken in grün (weniger als 50 % ausgegeben), gelb (50 -80 % ausgegeben)
und rot (über 80 % ausgegeben). Eine gestrichelte Linie gibt das Budgetlimit pro Balken an.

![bar chart](/assets/bar_chart_sm.png)

Für die beiden Doughnut-Charts darunter kann ausgewählt werden, für welchen Monat in welchem Jahr sie angezeigt werden sollen.
Default wird der aktuelle Monat angezeigt.
In der Mitte der Diagramme stehen jeweils die Gesamtausgaben/Gesamteinnahmen des Monats. 
Auf den Wedges befindet sich der prozentuale Anteil der Kategorie am gesamten Betrag und außen steht der 
Kategoriename mit den jeweiligen Ausgaben/Einnahmen in Euro.

![doughnut chart spending](/assets/spending_chart_sm.png)
![doughnut chart income](/assets/income_chart_sm.png)

## Systembeschreibung für Entwickler*innen

Die Anwendung wurde im Backend mit Python und dem Web-Framework Flask erstellt. Die Datenpersistenz erfolgt über SQLite. 
Für das Frontend wurde das React-Framework in Kombination mit Vite eingerichtet.

### UML-Diagramm

Das UML-Klassendiagramm stellt die grundlegende Struktur des Finanzverwaltungssystems dar und zeigt die zentralen Klassen, 
ihre Attribute, Methoden sowie die Beziehungen zwischen ihnen. Die Architektur orientiert sich an einer 
Schichtenarchitektur, die eine klare Trennung von Zuständigkeiten ermöglicht.

Die Struktur gliedert sich von unten nach oben in vier Hauptschichten:

- Domain Layer (Domänenschicht): Der Kern der Anwendung, frei von Infrastruktur.
- Persistence Layer (Persistenzschicht): Verantwortlich für die Speicherung der Domänenobjekte.
- Service Layer (Serviceschicht): Koordiniert Anwendungsfälle und wendet Geschäftsregeln an.
- API Layer (Präsentationsschicht): Definiert die Schnittstelle zum Frontend.

Die Abhängigkeitsrichtung ist von oben nach unten und folgt demnach dem Unabhängigkeitsprinzip. Höhere Schichten 
können auf niedrigere Schichten zugreifen, aber niedrigere Schichten haben keine Abhängigkeiten zu höheren Schichten.

![uml diagramm](/assets/uml.png)
<div style="text-align: right">(erstellt mit https://plantumlonlineeditor.com/)</div>

### Domain Layer

Die Domänenschicht ist der Kern der Anwendung und enthält das **Domänenmodell**. Sie kapselt die grundlegenden 
Geschäftsregeln und Datenobjekte des Systems (`Transaction`, `Budget`, `Category`) und ist frei von jeglicher Logik 
zur Datenpersistenz oder Präsentation.

#### Category

Die Klasse `Category` implementiert ein Enum und modelliert die möglichen Kategorien von Transaktionen.
Sie stellt eine zentrale Definition der Kategorien dar und wird von anderen Klassen zur Konsistenz der 
Daten verwendet. Ihre Hauptfunktion besteht darin, die Geschäftslogik der Kategorisierung 
(Definition, Unterkategorien, Einnahme/Ausgabe-Status) an einer zentralen Stelle zu definieren. 

Jedes Mitglied des Enums repräsentiert eine Hauptkategorie und speichert in seinem Wert einen Tupel mit den 
folgenden drei Elementen:

- *category_name*, str --> Anzeigename der Kategorie (z.B. `Income`, `Food`, `Education`, ...)
- *sub_category*, List[str] --> Liste der möglichen Unterkategorien (für `Food` z.B. [`Mensa`, `Bakery`, `Rewe`, ...])
- *is_income*, bool --> speichert, ob Kategorie Einnahme (= `True`) oder Ausgabe (= `False`) ist, um die absolut 
gespeicherten Beträge richtig verwenden zu können

Um Zugriff auf die Tupel zu ermöglichen, enthält die Klasse drei @property_Methoden:

- *category_name*, str --> Übergibt das Element an Tupel-Stelle 0 = Anzeigename
- *sub_category*, List[str] --> Übergibt das Element an Tupel-Stelle 1 = Liste mit zugehörigen Unterkategorien
- *is_income*, bool --> Übergibt das Element an Tupel-Stelle 2 = `True`/`False`

Die Methode *from_category_as_string*(cls, category_name: str) ermöglicht es anderen Teilen des Systems, 
ein Category-Enum-Mitglied anhand des Anzeigenamens (z.B. dem in der Datenbank gespeicherten String) zu finden 
und das entsprechende Enum-Objekt zurückzugeben.

#### Transaction

Die Klasse `Transaction` repräsentiert eine einzelne finanzielle Transaktion. Sie dient ausschließlich als 
Datencontainer und enthält keine Logik zur Datenpersistenz. Ihre Hauptaufgabe ist die Bündelung aller 
relevanten Attribute, die eine Transaktion eindeutig beschreiben, bevor diese von anderen Modulen 
(z.B. API-Endpunkten oder Datenbank-Handlern) weiterverarbeitet, persistiert oder in Berichten zusammengefasst werden.

Sie enthält die folgenden Attribute:

- *amount*, float --> Betrag der Transaktion, wird immer als Absolutbetrag gespeichert und auf zwei Dezimalstellen gerundet
- *category_name*, str --> der Name der Hauptkategorie (z.B. `Income`, `Food`, `Education`, ...)
- *sub_category*, str --> der Name der Unterkategorie (für `Food` z.B. `Mensa`, `Bakery`, `Rewe`...)
- *date*, datetime --> der genaue Zeitpunkt der Transaktion im Format 'YYYY-MM-DDTHH:MM:SS'

#### Budget

Die Klasse `Budget` repräsentiert das Budgetlimit für eine bestimmte, vordefinierte Hauptkategorie (`Category`). 
Sie dient dazu einen Überblick über den aktuellen finanziellen Status einer Kategorie mit limitiertem Budget zu erhalten, 
indem sie das maximale Ausgabenlimit speichert und die bereits getätigten Ausgaben verfolgt.

Die Klasse enthält die folgenden Attribute:

- *category*, Category --> das zugrunde liegende Category-Objekt, für das das Budget gilt
- *limit*, float --> der Maximalbetrag, der für diese Kategorie ausgegeben werden darf (das Budgetlimit)
- *spent*, float --> der Betrag, der bereits für diese Kategorie ausgegeben wurde (Standardwert ist 0.0)

Die Klasse bietet folgende Methoden zur Verwaltung des Budgets:

- *add_expense(amount: float)* --> Erhöht den Wert des Attributs `spent` um den übergebenen Betrag `amount`.
Diese Methode wird verwendet, um neue Ausgaben zur Budgetverfolgung hinzuzufügen.
- *get_remaining() -> float* --> Berechnet den noch verfügbaren Betrag im Budget.
Die Berechnung erfolgt durch Subtraktion der bisherigen Ausgaben vom Limit: `self.limit` - `self.spent`.
- *reset_spent()* --> Setzt den Wert des Attributs `spent` auf 0.0 zurück. Dies wird typischerweise zum Monatsanfang verwendet.

### Persistenz Layer

Die Persistenzschicht ist für den Zugriff auf die SQLite-Datenbank zuständig.

#### SqliteDb

Die Klasse SqliteDb kapselt sämtliche Datenbankoperationen unter Verwendung der sqlite3-Bibliothek.
Sie ist verantwortlich für das Speichern, Laden, Aktualisieren und Löschen von Transaktionen, 
sowie für die Verwaltung von Budgets.

Die öffentlichen Methoden sind die Schnittstelle für andere Schichten:

- *save_transaction(transaction: Transaction)* --> speichert ein übergebenes `Transaction`-Objekt dauerhaft in der `transactions`-Tabelle
- *load_all_transactions()* -> List[Transaction] --> ruft alle Transaktionen aus der Datenbank ab, sortiert nach Datum absteigend und 
gibt eine Liste der `Transaction`-Objekten zurück
- *load_transactions_by_exact_date(date: str)* -> List[Transaction] --> ruft alle Transaktionen ab, die exakt am 
angegebenen Datum stattgefunden haben
- *load_transactions_by_date_range(start_date: str, end_date: str)* -> List[Transaction] --> ruft alle Transaktionen ab, 
die innerhalb des angegebenen Datumsbereichs liegen (inklusive Grenzen)
- *load_transactions_by_from_date (start_date: str, category_name: str)* -> List[Transaction] --> ruft alle Transaktionen 
vom Startdatum an ab. Optional wird nach `category_name` gefiltert.
- *load_transactions_by_until_date(end_date: str)* -> List[Transaction] --> ruft alle Transaktionen bis zum Enddatum ab (inklusive Enddatum)
- *load_transactions_by_category(category_name: str)* -> List[Transaction] --> ruft alle Transaktionen ab, die zu der 
angegebenen Hauptkategorie gehören
- *load_transactions_by_sub_category(sub_category: str)* -> List[Transaction] --> ruft alle Transaktionen ab, die zu der 
angegebenen Unterkategorie gehören
- *save_budget(category_name: str, limit: float)* --> speichert oder aktualisiert das Budgetlimit `limit` für die angegebene Kategorie
- *get_budget_reset_month(category_name: str)*	-> str/None	--> ruft den gespeicherten Monatsstempel `last_reset_month` ab, 
der angibt, wann das Budget zuletzt zurückgesetzt wurde
- *update_budget_reset_month(category_name: str, month: str)* --> aktualisiert den Monatsstempel für das Budget der angegebenen Kategorie
- *load_all_budgets()* -> Dict[str, float] --> ruft alle Budgets ab und gibt sie als Dictionary zurück, wobei der 
Kategoriename der Schlüssel und das Limit der Wert ist
- *delete_budget(category_name: str)* --> löscht das Budget der angegebenen Kategorie aus der Datenbank

Interne Methoden zur Initialisierung der Datenbanktabellen *_create_table_transactions* und *_create_table_budgets* sind 
als private Methoden implementiert und werden im Konstruktor aufgerufen. Sie dienen ausschließlich der 
Initialisierung der Datenbankstruktur.

Die Persistenzschicht kennt die Model-Klassen (insbesondere `Transaction`), hat jedoch keine Abhängigkeiten zum
API-Layer oder Frontend.

### Setup / Utility

Die Setup/Utility-Sektion dient der Initialisierung der Anwendungsumgebung und ist für die Generierung von
Beispieldaten notwendig. Diese Komponente sit vom eigentlichen Laufzeit-Geschäftsprozess entkoppelt und dient
der Vereinfachung des Setups.

#### DbCreator

Die Klasse `DbCreator` ist ein Datenbank-Creator und eine Utility-Klasse, deren Hauptaufgabe darin besteht, eine 
funktionsfähige Datenbank `finances.db` zu erstellen und diese mit einem realistischen Set von Transaktionsdaten 
zu befüllen. Sie stellt somit eine wichtige Komponente für die Demonstration und das Testen der Anwendung dar
und wird ausschließlich beim Start der Anwendung in der Entwicklungsphase verwendet. Da sie direkt auf die 
SQLite-Datenbank zugreift, ist sie thematisch der Persistenz zuzuordnen.

Der Konstruktor der Klasse bekommt als Parameter `years: int` übergeben, der festlegt, für wie viele vollen Jahre bis
zum aktuellen Datum Testdaten erzeugt werden sollen. Er ruft die Methoden zur Erstellung der Datenbanktabellen 
`_create_table` und `_create_table_budgets` auf, um die Datenbankstruktur vorzubereiten.

Die Methode *run_creator()* führt die Hauptlogik zur Generierung der Transaktionen aus. Es wird monatsweise von der 
definierten Startzeit bis zum Enddatum iteriert und dabei realistische Beispieldaten erzeugt:

- Feste monatliche Einnahmen und Ausgaben (z. B. `Rent`, `Job`) zum Monatsbeginn
- Zufällige Ausgaben für andere Kategorien (`Food`, `Sport`, `Other`, ...), wobei mindestens 20 zufällige Einträge pro 
Monat generiert werden, um eine realistische Datenbasis zu schaffen

Diese werden mit der Methode *add()* in der `transactions`-Tabelle gespeichert.

Die Funktion *add_random_time(dt)* liegt außerhalb der Klasse, da sie keinen Zugriff auf Klasseninhalte benötigt.
Sie wird zur Erstellung eines realistischen Zeitstempels für die Transaktionen verwendet, 
um die Datum- und Uhrzeit-Informationen zufälliger zu gestalten.

### Service Layer

Die Serviceschicht bildet die Schnittstelle zwischen der API-Schicht und der darunter liegenden Domänen- und Persistenzschicht.

Diese Schicht ist für die Koordination der Anwendungsfälle und die Ausführung der Geschäftsregeln verantwortlich. 
Sie nimmt Daten entgegen, verwendet das Domänenmodell (`Transaction`, `Category`, `Budget`) und die Persistenzschicht 
`SqliteDb`, um komplexe Aktionen durchzuführen.

#### TransactionsService

Die Klasse `TransactionsService` beinhaltet die gesamte Logik rund um das Hinzufügen, Abrufen und Filtern von 
Transaktionen. Sie stellt sicher, dass alle Geschäftsregeln (z. B. Budgetprüfungen) eingehalten werden, 
bevor Daten persistent gespeichert werden. Sie benötigt eine Instanz von `SqliteDb` zur Datenpersistenz und 
eine Instanz des `BudgetsService` zur Durchsetzung der Budget-Geschäftslogik.

`TransactionService` beinhaltet die folgenden Methoden:

- *add_transaction(data: dict)* -->	Fügt eine Transaktion zur Datenbank hinzu. Enthält wichtige Validierungslogik: 
Prüft vor dem Speichern, ob die Ausgabe das Budgetlimit für die betreffende Kategorie überschreiten würde. 
Löst einen ValueError aus, falls das Budget nicht ausreicht.
- *get_transactions(category_name: str, as_dict: bool)* ->	List[Transaction] oder List[dict] --> Ruft alle 
Transaktionen ab. Ermöglicht optional die Filterung nach Kategorienamen. Kann die Rückgabe in eine Liste von Objekten 
oder zur direkten API-Ausgabe in eine Liste von Dictionaries konvertieren.
- *get_transactions_by_date*(exact_date: str, start_date: str, end_date: str, as_dict: bool) -> List[Transaction] 
oder List[dict]	--> Bietet eine komplexe Abfrageschnittstelle zur Filterung von Transaktionen nach exaktem Datum, 
Startdatum, Enddatum oder Datumsbereich. Delegiert die eigentliche Datenbankabfrage an die SqliteDb. Über `as_dict` 
kann die Rückgabe als Liste von Objekten oder zur direkten API-Ausgabe als Liste von Dictionaries erfolgen.
- *get_transactions_by_sub_category(sub_category: str, as_dict: bool)* -> List[Transaction] oder List[dict]	--> 
Ruft alle Transaktionen ab, die einer bestimmten Unterkategorie zugeordnet sind. Über `as_dict` 
kann die Rückgabe als Liste von Objekten oder zur direkten API-Ausgabe als Liste von Dictionaries erfolgen.
- *get_all_categories() -> List[dict] --> Ruft alle verfügbaren Kategorien aus dem Domänenmodell `Category`-Enum ab 
und formatiert sie für die API-Ausgabe.

Interne Hilfsmethoden sind:

- *_signed_amount(t)* --> Konvertiert den absolut gespeicherten Betrag der Transaktion in einen Betrag mit Vorzeichen 
(negativ für Ausgaben, positiv für Einnahmen), basierend auf dem is_income-Attribut der `Category`.
- *_convert_if_needed(transactions, as_dict)* --> Wird as_dict=True übergeben, wird die aus der Persistenzschicht
abgerufene Liste von `Transaction`-Objekten in eine Liste von Dictionaries umgewandelt. Bei as_dict=False erfolgt die 
Weitergabe als Liste von `Transaction`-Objekten.



Die Flask-Routen wurden im UML-Diagramm als Controller-Klassen abstrahiert dargestellt, um die logische Struktur der API unabhängig vom verwendeten Framework zu modellieren.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


~/PycharmProjects/PfDS_M1_FinancialManager$ python -m backend.app