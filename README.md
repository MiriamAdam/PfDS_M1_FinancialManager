# Aufgabe 1 - Applikation: Finanzmanager

Die Finanzmanager-Anwendung wurde von Miriam Adam im Rahmen des Wahlpflichtmoduls "Einführung in Python for Data Science" 
im Wintersemester 2025/2026 an der Hochschule Bremen erstellt. Sie ist Teil von drei Aufgaben, die als erster Meilenstein 
des Moduls innerhalb von sechs Wochen in Dreiergruppen bearbeitet werden sollte. Unserer Gruppe hat sich nach längerem 
Überlegen dazu entschieden, dass jede Person alleine eine Aufgabe bearbeitet. 

Ziel dieser Aufgabe war es, einen persönlichen Finanzmanager zu entwickeln, der Nutzer*innen dabei hilft, seine/ihre 
Finanzen im Überblick zu behalten. Dabei soll er die Möglichkeit bieten, Einnahmen und Ausgaben zu erfassen, zu 
kategorisieren und auszuwerten. Während das Backend mit Python geschrieben werden sollte, war die Wahl des User-Interfaces 
den Studierenden überlassen.

# Systembeschreibung

Die hier erstellte Anwendung ermöglicht es Einzelpersonen, ihre Ausgaben und Einnahmen zu dokumentieren, indem Transaktionen
gespeichert und nach Kategorien und Datum gefiltert werden können.
Mithilfe von monatlichen Budgets ist es möglich einzelne Ausgaben-Kategorien zu beschränken. Transaktionen, die das 
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

Jetzt kann die Anwendung im Browser über http://localhost:4173/ aufgerufen werden.

### Anwendungsbeschreibung

Die Anwendung ist auf Englisch und hat vier Pages, die auf der linken Seite in einer horizontalen Navigationsleiste 
ausgewählt werden können.
Auf der Startseite der Anwendung wird eine Übersicht über den aktuellen Finanzstatus angezeigt.
Unter dem Kontostand befindet sich ein tagesaktuelles Liniendiagramm, dass den Verlauf des Kontostands der 
letzten 30 Tage darstellt. Darunter werden die letzten zehn Transaktionen angezeigt.

![overview](/assets/overview_sm.png)

Auf der Seite **Transactions** befindet sich im oberen Bereich ein Formular, mit dem Transaktionen angelegt werden können.
Nach Auswahl der Kategorie kann die passende Unterkategorie ausgewählt und der entsprechende Betrag eingegeben werden.
Mit einem Klick auf *Add transaction* wird die Transaktion entgegengenommen und erscheint als neuste Buchung im unteren Bereich. 
Hier sind alle bisher getätigten Transaktionen von der aktuellsten zur ältesten Buchung aufgelistet. 
Mit den Formularen darüber kann nach Kategorien und/oder Datum gefiltert werden.

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
- API Layer (Präsentationsschicht): Definiert die Schnittstelle zum Frontend. Die Flask-Routen wurden im UML-Diagramm 
als Controller-Klassen abstrahiert dargestellt, um die logische Struktur der API unabhängig vom verwendeten Framework 
zu zeigen.

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

- `category_name, str`: Anzeigename der Kategorie (z.B. `Income`, `Food`, `Education`, ...)
- `sub_category, List[str]`: Liste der möglichen Unterkategorien (für `Food` z.B. [`Mensa`, `Bakery`, `Rewe`, ...])
- `is_income, bool`: speichert, ob Kategorie Einnahme (= `True`) oder Ausgabe (= `False`) ist, um die absolut 
gespeicherten Beträge richtig verwenden zu können

Um Zugriff auf die Tupel zu ermöglichen, enthält die Klasse drei @property_Methoden:

- *category_name*, str: Übergibt das Element an Tupel-Stelle 0 = Anzeigename
- *sub_category*, List[str]: Übergibt das Element an Tupel-Stelle 1 = Liste mit zugehörigen Unterkategorien
- *is_income*, bool: Übergibt das Element an Tupel-Stelle 2 = `True`/`False`

Die Methode *from_category_as_string*(cls, category_name: str) ermöglicht es anderen Teilen des Systems, 
ein Category-Enum-Mitglied anhand des Anzeigenamens (z.B. dem in der Datenbank gespeicherten String) zu finden 
und das entsprechende Enum-Objekt zurückzugeben.

#### Transaction

Die Klasse `Transaction` repräsentiert eine einzelne finanzielle Transaktion. Ihre Hauptaufgabe ist die Bündelung aller 
relevanten Attribute, die eine Transaktion eindeutig beschreiben, bevor diese von anderen Schichten weiterverarbeitet, 
persistiert oder in Berichten zusammengefasst werden.

Sie enthält die folgenden Attribute:

- `amount, float`: Betrag der Transaktion, wird immer als Absolutbetrag gespeichert und auf zwei Dezimalstellen gerundet
- `category_name, str`: der Name der Hauptkategorie (z.B. `Income`, `Food`, `Education`, ...)
- `sub_category, str`: der Name der Unterkategorie (für `Food` z.B. `Mensa`, `Bakery`, `Rewe`...)
- `date, datetime`: der genaue Zeitpunkt der Transaktion im Format 'YYYY-MM-DDTHH:MM:SS'

#### Budget

Die Klasse `Budget` repräsentiert das Budgetlimit für eine bestimmte `Category`. 
Sie dient dazu einen Überblick über den aktuellen finanziellen Status einer Kategorie mit limitiertem Budget zu erhalten, 
indem sie das maximale Ausgabenlimit speichert und die bereits getätigten Ausgaben verfolgt.

Die Klasse enthält die folgenden Attribute:

- `category, Category`: das zugrunde liegende Category-Objekt, für das das Budget gilt
- `limit, float`: der Maximalbetrag, der für diese Kategorie ausgegeben werden darf (das Budgetlimit)
- `spent, float` der Betrag, der bereits für diese Kategorie ausgegeben wurde (Standardwert ist 0.0)

Die Klasse bietet folgende Methoden zur Verwaltung des Budgets:

- *add_expense(amount: float)*: Erhöht den Wert des Attributs `spent` um den übergebenen Betrag `amount`.
Diese Methode wird verwendet, um neue Ausgaben zur Budgetverfolgung hinzuzufügen.
- *get_remaining()* -> `float`: Berechnet den noch verfügbaren Betrag im Budget.
Die Berechnung erfolgt durch Subtraktion der bisherigen Ausgaben vom Limit: `self.limit` - `self.spent`.
- *reset_spent()*: Setzt den Wert des Attributs `spent` auf 0.0 zurück. Dies wird typischerweise zum Monatsanfang verwendet.

### Persistenz Layer

Die Persistenzschicht ist für den Zugriff auf die SQLite-Datenbank zuständig.

#### SqliteDb

Die Klasse SqliteDb beinhaltet sämtliche Datenbankoperationen unter Verwendung der sqlite3-Bibliothek.
Sie ist verantwortlich für das Speichern, Laden, Aktualisieren und Löschen von Transaktionen, 
sowie für die Verwaltung von Budgets.

Die öffentlichen Methoden sind die Schnittstelle für andere Schichten:

- *save_transaction(transaction: Transaction)*: speichert ein übergebenes `Transaction`-Objekt dauerhaft in der `transactions`-Tabelle
- *load_all_transactions(start_date: str = None, end_date: str = None)* -> `List[Transaction]`: ruft alle Transaktionen 
aus der Datenbank ab, optional gefiltert nach Datum, und gibt eine Liste der `Transaction`-Objekte zurück
- *load_transactions_by_category(category_name: str, start_date: str = None, end_date: str = None)* -> `List[Transaction]`: 
ruft alle Transaktionen ab, die zu der angegebenen Hauptkategorie gehören, optional gefiltert nach Datum
- *load_transactions_by_sub_category(sub_category: str, start_date: str = None, end_date: str = None)* -> `List[Transaction]`: 
ruft alle Transaktionen ab, die zu der angegebenen Unterkategorie gehören, optional gefiltert nach Datum
- *save_budget(category_name: str, limit: float)*: speichert oder aktualisiert das Budgetlimit `limit` für die angegebene Kategorie
- *get_budget_reset_month(category_name: str)*	-> `str` oder `None`: ruft den gespeicherten Monatsstempel `last_reset_month` ab, 
der angibt, wann das Budget zuletzt zurückgesetzt wurde
- *update_budget_reset_month(category_name: str, month: str)*: aktualisiert den Monatsstempel für das Budget der angegebenen Kategorie
- *load_all_budgets()* -> `Dict[str, float]`: ruft alle Budgets ab und gibt sie als Dictionary zurück, wobei der 
Kategoriename der Schlüssel und das Limit der Wert ist
- *delete_budget(category_name: str)*: löscht das Budget der angegebenen Kategorie aus der Datenbank

Interne Methoden zur Initialisierung der Datenbanktabellen *_create_table_transactions* und *_create_table_budgets* sind 
als private Methoden implementiert und werden im Konstruktor aufgerufen. Sie dienen ausschließlich der 
Initialisierung der Datenbankstruktur.

Die Persistenzschicht kennt die Model-Klassen, hat jedoch keine Abhängigkeiten zum API-Layer oder Frontend.

##### Datenbankschema

Die Anwendung verwendet eine einzige SQLite-Datenbankdatei. Das Schema besteht aus zwei Haupttabellen, deren Struktur 
durch die privaten Initialisierungsmethoden *_create_table_transactions()* und *_create_table_budgets()* definiert wird.

Die Tabelle `transactions` speichert alle Einnahmen und Ausgaben als einzelnen Transaktionen. Sie enthält die Attribute
`id` (INTEGER, PRIMARY KEY), `category_name` (TEXT), `sub_category` (TEXT), `amount` (REAL), `date` (TEXT) und `description` (TEXT).
Die Tabelle `budgets` speichert die monatlichen Budget-Limits pro Hauptkategorie und den Status des letzten Zurücksetzens.	
Ihre Attribute sind `category_name` (TEXT, PRIMARY KEY), `limit` (REAL), `last_reset_month` (TEXT)

Es werden die Standard-SQLite-Typen verwendet, wobei `date` und `last_reset_month` als Text im ISO 8601-Format 
(YYYY-MM-DD bzw. YYYY-MM) gespeichert werden. `amount` und `limit` werden als REAL als Fließkommazahlen gespeichert, 
um Währungsbeträge präzise zu speichern.

### Setup / Utility

Die Setup/Utility-Sektion dient der Initialisierung der Anwendungsumgebung und ist für die Generierung von
Beispieldaten notwendig. Diese Komponente ist vom eigentlichen Laufzeit-Geschäftsprozess entkoppelt und dient
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
eine Instanz des `BudgetsService` zur Einhaltung der Budget-Geschäftslogik.

`TransactionService` beinhaltet die folgenden Methoden:

- *add_transaction(data: dict)*: Fügt eine Transaktion zur Datenbank hinzu. Enthält wichtige Validierungslogik: 
Prüft vor dem Speichern, ob die Ausgabe das Budgetlimit für die betreffende Kategorie überschreiten würde. 
Löst einen ValueError aus, falls das Budget nicht ausreicht.
- *get_transactions(category_name: str, sub_category: str, start_date: str = None, end_date: str = None as_dict: bool=False)* 
-> `List[Transaction]` oder `List[dict]`: Ruft alle Transaktionen ab. Ermöglicht optional die Filterung nach Kategorien und Datum. 
Kann die Rückgabe in eine Liste von Objekten oder zur direkten API-Ausgabe in eine Liste von Dictionaries konvertieren.
- *get_all_categories()* -> `List[dict]`: Ruft alle verfügbaren Kategorien aus dem Domänenmodell `Category`-Enum ab 
und formatiert sie für die API-Ausgabe.

Interne Hilfsmethoden sind:

- *_signed_amount(t)*: Konvertiert den absolut gespeicherten Betrag der Transaktion in einen Betrag mit Vorzeichen 
(negativ für Ausgaben, positiv für Einnahmen), basierend auf dem is_income-Attribut der `Category`.
- *_convert_if_needed(transactions, as_dict)*:  Wird as_dict=True übergeben, wird die aus der Persistenzschicht
abgerufene Liste von `Transaction`-Objekten in eine Liste von Dictionaries umgewandelt. Bei as_dict=False erfolgt die 
Weitergabe als Liste von `Transaction`-Objekten.

#### BudgetsService

Die Klasse `BudgetsService` verwaltet die Budgets im System. Sie ist für das Setzen, Abrufen, Aktualisieren und 
Löschen von Budgets zuständig und implementiert die monatliche Reset-Logik. Im Gegensatz zum `TransactionsService` 
hält der `BudgetsService` den aktuellen Zustand aller Budgets im Speicher `self.budgets`, um schnelle Zugriffe zu ermöglichen.
Sie nutzt `SqliteDb` zur Persistenz und arbeitet direkt mit den Domänenobjekten `Category` und `Budget`.

Im Konstruktor wird der Service initialisiert. Es wird eine Instanz von `SqliteDb` erstellt und *_load_budgets_from_storage()* 
aufgerufen, um alle persistenten Budgets in den internen Speicher in das `self.budgets`-Dictionary zu laden.
Anschließend wird *ensure_budgets_are_current()* aufgerufen, um sicherzustellen, dass die Monatsbudgets aktuell sind.
Die Methode prüft anhand des gespeicherten `last_reset_month`-Stempels, ob ein neuer Monat begonnen hat. Falls ja, 
wird das Attribut `spent` des jeweiligen Budget-Objekts auf 0.0 zurückgesetzt und der Stempel in der Datenbank aktualisiert.

Die Methoden von `BudgetsService` sind:
- *set_budget(data: dict)*:	Setzt oder aktualisiert das Budgetlimit für eine Kategorie. Enthält Validierung: 
Prüft, ob die aktuellen Ausgaben im laufenden Monat das neue Limit bereits überschreiten, bevor es gespeichert wird.
- *get_all_budgets*	-> `List[dict]`: Ruft alle Budgets ab und berechnet für jedes Budget den aktuellen ausgegebenen 
`spent` und verbleibenden `remaining` Betrag.
- *get_current_spent_amount(category: str)* -> `float`: Ruft alle Transaktionen des aktuellen Monats für die gegebene 
Ausgaben-Kategorie von `SqliteDb` ab und summiert die enthaltenen `amounts` auf.
- *get_budget_for_category(category: Category)* -> `Budget` oder `None`: Gibt das gespeicherte Budget-Objekt für die 
gegebene Kategorie aus dem internen Speicher zurück.
- *delete_budget(category_string: str)*: Löscht das Budget sowohl aus dem internen Speicher `self.budgets` 
als auch permanent aus der Datenbank.

#### ReportsService

Die Klasse `ReportsService` ist für die Datenauswertung und die Visualisierung von Berichten zuständig. Sie nutzt die 
Rohdaten aus dem `TransactionsService` und verarbeitet sie mithilfe der Bibliotheken Pandas und Matplotlib, um 
Finanzmetriken zu berechnen, die Daten zusammenzufassen und sie für die Darstellung in Diagrammen zu nutzen. Die fertigen
Diagramme werden als Bilder (.png) zurückzugeben.

`ReportsService`benötigt Instanzen des `BudgetsService` und des `TransactionsService`, um auf alle 
Transaktions- und Budgetdaten zugreifen zu können.

Die folgenden Methoden werde vom `ReportsService` zur Berichtserstellung genutzt:

- *get_monthly_summary_chart_img* -> `BytesIO`:	Erstellt ein Liniendiagramm des Kontostands über die letzten 30 Tage. 
Mit Pandas wird der Startkontostand berechnet, ein DataFrame erstellt, cumsum() zur Berechnung des kumulierten Saldos angewendet
und fehlende Tage mit *ffill()* aufgefüllt, um einen lückenlosen Verlauf zu erhalten.
- *get_bar_chart_img* -> `BytesIO`: Erstellt ein Balkendiagramm, das die im aktuellen Monat ausgegebenen Beträge pro 
Kategorie den festgelegten Budgetlimits gegenüberstellt. Mit Matplotlib werden die ausgegebenen Beträge als Balken 
und das Limit als horizontale gestrichelte Linien `hlines` visualisiert. Die Farben der Balken zeigen den Auslastungsgrad 
des Budgets an.
- *get_monthly_spending_share_chart_img(year: int, month: int)*	-> `BytesIO`: Erzeugt ein Doughnut-Diagramm , das den 
prozentualen Anteil der Ausgaben jeder Kategorie für einen bestimmten Monat darstellt. 
Die Gesamtausgaben werden in der Mitte des Diagramms angezeigt.
- *get_monthly_income_share_chart_img(year: int, month: int)* -> `BytesIO`: Erzeugt ein Doughnut-Diagramm, das den 
prozentualen Anteil der Einnahmen pro Unterkategorie für einen bestimmten Monat darstellt. Die Gesamteinnahmen werden in 
der Mitte des Diagramms angezeigt.

### API Layer

Die Controller-Schicht ist die oberste Schicht des Backends und stellt sozusagen das Tor zur Außenwelt dar. Ihre Aufgabe 
ist das Routing von HTTP-Anfragen, die Validierung von Eingabedaten und die Formatierung der Responses.

Diese Schicht enthält keine Geschäftslogik. Sie delegiert alle komplexen Aufgaben an die Service Layer.

Alle Controller sind als Flask Blueprints implementiert. Die Blueprints sammeln alle Transaktions-Endpunkte und 
ermöglichen die einfache Registrierung der Routen in der Haupt-Flask-Anwendung `app.py`.

#### Transactions API Controller

Der Transactions API Controller stellt eine REST-Schnittstelle zur Verwaltung aller Finanztransaktionen und zur 
Abfrage von Kategoriedaten bereit. Jegliche Geschäftslogik wird vollständig an den `TransactionsService` weitergegeben.

Definierte REST-Endpunkte:

- /categories `GET`: Ruft alle definierten Kategorien über *transactions_service.get_all_categories()* ab. 
Gibt eine Liste der Kategorien als JSON zurück (Status: `200`).
- /transactions `GET` optional mit ?category=<name>, ?sub_category=<name>, ?start_date=<YYYY-MM-DD>, ?end_date=<YYYY-MM-DD>:
Ruft alle Transaktionen ab. Optional kann über die Parameter nach Kategorien und Datum gefiltert werden. 
Nutzt dafür *transactions_service.get_transactions()*.
- /transactions `POST`: Nimmt die Transaktionsdaten (Betrag, Kategorie, etc.) im JSON-Body entgegen und übergibt sie zur 
Validierung und Speicherung an *transactions_service.add_transaction()*. Gibt bei Erfolg den Status `201` Created zurück.


Die API-Routen enthalten eine grundlegende Fehlerbehandlung, die spezifische Geschäftsfehler (ValueError vom Service) 
mit dem Statuscode `400` Bad Request und allgemeine Serverfehler mit `500` Internal Server Error beantwortet.

#### Budgets API Controller

Der Budgets API Controller stellt die REST-Schnittstelle zur Verwaltung der Budgets pro Kategorie bereit. 
Er dient als Controller, der alle Anfragen an den `BudgetsService` weiterleitet und die Antworten für das Frontend formatiert.

Definierte REST-Endpunkte:

- `POST`: Setzen/Aktualisieren eines Budgets. Nimmt die Daten `category_name` und `limit` aus dem JSON body entgegen und leitet 
sie an *budgets_service.set_budget()* weiter. Löst `409` Conflict aus, wenn das Budgetlimit bereits überschritten wurde (ValueError).
- `GET`: Ruft die aktuelle Liste aller Budgets, inklusive berechnetem `spent` und `remaining`, vom `BudgetsService` ab.
- /<category_name>	`DELETE`: Löscht das Budget für die angegebene Kategorie. Verwendet den Kategorienamen als 
URL-Parameter und nutzt *budgets_service.delete_budget()*.


Zur Fehlerbehandlung wird bei fehlenden Feldern im JSON-Body (KeyError) ein `400`Bad Request zurückgegeben. Ein `409` 
Conflict wird zurückgegeben, wenn eine Budget-Setzung fehlschlägt, weil der bereits ausgegebene Betrag das neue Limit 
überschreitet (basierend auf der ValueError des Service). Zur allgemeinen Fehlerbehandlung wird `500` Internal Server Error verwendet.

#### Reports API Controller

Der Reports API Controller ist für das Abrufen und Bereitstellen von Berichten und Diagrammen zuständig, 
die durch den `ReportsService` generiert werden.

Da der ReportsService Bilder (.png) zurückgibt, ist die Hauptaufgabe dieses Controllers, das empfangene 
Binärdaten-Objekt `BytesIO` mithilfe der Flask-Funktion *send_file* korrekt zu verpacken und als `image/png` MIME-Type 
an den Client zu senden.

Definierte REST-Endpunkte für Berichte:

- /monthly-income-share-chart `GET`	mit ?year=<int>, ?month=<int>: Liefert ein Doughnut-Diagramm der Einnahmenanteile 
pro Unterkategorie für den angegebenen Monat/Jahr von *reports_service.get_monthly_income_share_chart_img()*.
- /monthly-spending-share-chart `GET` mit ?year=<int>, ?month=<int>: Liefert ein Doughnut-Diagramm der 
Ausgabenanteile pro Kategorie für den angegebenen Monat/Jahr. Dafür wird *reports_service.get_monthly_spending_share_chart_img()* genutzt.
- /monthly-summary `GET`: Liefert ein Liniendiagramm des Kontostandverlaufs der letzten 30 Tage von
*reports_service.get_monthly_summary_chart_img()*.
- /bar-chart `GET`: Liefert ein Balkendiagramm, das den aktuellen Budget-Verbrauch im Verhältnis zum Budget-Limit 
darstellt von *reports_service.get_bar_chart_img()*.

Alle Endpunkte geben den HTTP-Status 200 OK zurück. Anstelle von JSON-Daten senden die Endpunkte eine Binärdatei 
`image/png`, die direkt in der Frontend-Anwendung als Bild angezeigt werden kann. `500` Internal Server Error wird 
als allgemeiner Fallback-Fehlercode zurückgegeben, falls bei der Diagrammerstellung, Datenabfrage oder beim 
Verpacken der Datei ein unerwarteter interner Fehler auftritt.

### Frontend-Systembeschreibung

Das Frontend wurde unter Verwendung des React-Frameworks in Verbindung mit dem Build-Tool Vite als 
Single-Page Application (SPA) entwickelt.

Die React-Anwendung agiert als Client und kommuniziert ausschließlich über asynchrone REST API Calls mit der Backend-API Layer.

#### Routing und Seitenstruktur

Das Routing erfolgt client-seitig über die Bibliothek `react-router-dom`. Dies ermöglicht die Navigation innerhalb der 
Anwendung, ohne dass die Seite neu geladen werden muss. Die Hauptstruktur der Anwendung wird in der Komponente App.jsx definiert.
Der `<Router>` vom Typ BrowserRouter umschließt die gesamte Anwendung und aktiviert das client-seitige Routing. 
Innerhalb der `<Routes>`-Komponente werden die spezifischen URLs der Anwendung den entsprechenden Hauptkomponenten zugeordnet.
Jede Route lädt eine Page-Komponente (Home, Transactions, Budget oder Reports). Alle Page-Komponenten sind in die 
`<Layout>`-Komponente eingebettet. Diese Komponente fungiert als Rahmen, der Navigation, Header und andere 
wiederkehrende Elemente enthält, wodurch ein konsistentes Design über alle Seiten hinweg gewährleistet wird.

#### Globale Zustandsverwaltung und API-Kopplung

Zum State Management der Anwendung wird das React Context API verwendet.

Die Komponente `<TransactionsProvider>` umschließt alle `<Routes>`. Durch diese Anordnung wird sichergestellt, dass der 
gesamte Anwendungsbaum Zugriff auf den Zustand und die bereitgestellten Funktionen dieses Contexts hat.
Der TransactionsProvider wird in der Datei TransactionsContext.jsx implementiert. Die Datei enthält den Custom Hook 
*useTransactions()*. Dieser Hook stellt sicher, dass alle Komponenten effizient auf die Transaktionsdaten `transactions` 
und die Aktualisierungsfunktion `reload: loadTransactions` zugreifen können, ohne direkt mit dem Backend interagieren zu müssen.
Der Provider nutzt den React Hook `useEffect`, um die Funktion *loadTransactions()* beim erstmaligen Laden einer Page aufzurufen. 
Die Funktion *loadTransactions* akzeptiert optional vier Parameter (category, subCategory, start_date, end_date). 
Basierend auf diesen Parametern baut sie dynamisch die Query-String-URL für den asynchronen fetch-Aufruf an den 
Backend-Endpunkt GET /api/transactions auf und aktualisiert nach Empfang der JSON-Daten den lokalen Zustand.

#### Page-Komponenten

Die Komponenten im pages/-Verzeichnis stellen die Seiten der SPA dar. Sie nutzen entweder den globalen Zustand über 
den useTransactions-Hook oder führen direkte API-Aufrufe für spezifische, nicht-globale Daten wie Budgets oder Diagramme aus.

##### - Home (Home.jsx)

Home ist die Übersichtsseite, die den aktuellen Finanzstatus auf einen Blick zusammenfasst.
Kontostand und Transaktionen nutzen den Hook *useTransactions()* und berechnet den Gesamt-Kontostand `balance` aus allen 
Transaktionen. Außerdem werden die 10 neuesten Transaktionen angezeigt.
Für das Diagramm wird ein direkter Aufruf zum Backend-Endpunkt GET /api/chart/monthly-summary durchgeführt. 
Das Diagramm wird jedes Mal neu geladen, wenn sich die Transaktionen mit *useEffect([transactions])* ändern, um den Verlauf 
des Kontostands aktuell zu halten.

##### - Transactions (Transactions.jsx)

Transactions ist die zentrale Seite zur Anzeige, Verwaltung und Filterung von Transaktionen. Um die aktuellen 
Transaktionen zu bekommen, wird der Hook *useTransactions()* genutzt. Es wird ein fetch Request zu GET /api/categories 
ausgeführt, um die Liste der verfügbaren Kategorien für die Filterauswahl abzurufen.
Die Handler `handleCategoryChange`, `handleSubCategoryChange` und `handleDateChange` rufen die Context-Funktion 
*reload()* auf. Dies bewirkt, dass der Context einen gefilterten API-Aufruf (z.B. GET /api/transactions?category=Food) 
sendet und den Zustand des Formulars aktualisiert. Es können bis zu vier Parameter (category, subCategory, startDate, 
endDate) an den Context übergeben werden, um eine kombinierte Filterung zu ermöglichen 
(z.B. GET /api/transactions?sub_category=Fee&start_date=2025-10-01).

Die Komponente AddTransactionForm ruft nach erfolgreicher Erstellung einer Transaktion ebenfalls die *reload()*-Funktion 
des Contexts auf, um die neu erstellte Transaktion in der Liste anzuzeigen.

##### - Budgets (Budgets.jsx)

Die Seite Budgets dient zur Anzeige, Festlegung und Löschung monatlicher Budget-Limits.
Die Komponente ist nicht mit dem TransactionsContext verbunden, sondern verwaltet den Budget-Zustand `budgets` lokal.
Dafür führt die Funktion *loadBudgets()* einen direkten fetch Request zu GET /api/budgets aus.

Die Komponenten AddBudgetForm und DeleteBudgetForm rufen nach erfolgreicher Aktion die Funktion *loadBudgets()* auf, 
um die Budgetliste neu vom Backend abzurufen und die Seite zu aktualisieren. Dies stellt sicher, dass die Liste immer 
den aktuellen Zustand der Persistenzschicht widerspiegelt.

##### - Reports (Reports.jsx)

Reports ist die Seite zur Visualisierung von Finanzberichten. Diese Seite generiert dynamisch URLs, um Bilder vom 
Reports API Controller abzurufen. Beim Laden der Seite wird statisch das Balkendiagramm zum Budget-Verbrauch
mit GET /api/chart/bar-chart aufgerufen. Die dynamischen Berichte zu den monatlichen Einnahmen und Ausgaben werden mit
GET /api/chart/monthly-spending-share-chart und GET /api/chart/monthly-income-share-chart abgerufen. Dafür wird über 
die Auswahlfelder für Monat und Jahr die Funktion *reloadShareCharts()* ausgelöst. Diese Funktion erstellt die URLs neu 
und fügt einen Timestamp `&t=${Date.now()}` hinzu. Dieser Mechanismus sorgt dafür, dass der Browser gezwungen wird, 
die Bilder jedes Mal neu vom Backend anzufordern, wenn die Auswahl verändert wird.

#### Detail-Komponenten (components/)

Diese Komponenten sind wiederverwendbare Bausteine, die entweder für die Dateneingabe, die Datenansicht oder das Feedback 
zuständig sind.

##### - AddBudgetForm.jsx

AddBudgetsFrom ist ein Formular zum Erstellen oder Aktualisieren eines monatlichen Budgets.

Um die Kategorien zu filtern, wird beim Laden ein GET Request an /api/categories durchgeführt. Die Liste im Frontend ist
gefiltert, um nur die Ausgabenkategorien ohne `Sales` und `Income` für das Setzen eines Limits anzubieten.
Zum Festlegen eines Budgetlimits wird ein POST Request an den Endpunkt /api/budgets gesendet.

Es ist eine spezifische Behandlung für den Statuscode 409 Conflict implementiert. Dieser wird vom Backend ausgelöst, 
wenn der bereits ausgegebene Betrag das neue Limit überschritten wird, um dem/der Benutzer*in eine klare Fehlermeldung 
per Toast-Message anzuzeigen.
Um die Budgetliste in der Elternkomponente `Budgets.jsx` neu zu laden, wird *onSuccess()* aufgerufen.

##### - DeleteBudgetForm.jsx

DeleteBudgetForm ist ein Formular zum Löschen eines bestehenden Budgets.

Die Liste der löschbaren Budgets `props.budgets` wird von der Elternkomponente `Budgets.jsx` bereitgestellt.
Zum Löschen wird ein DELETE Request an den spezifischen Endpunkt /api/budgets/<category_name> weitergeleitet.
Um die Budgetliste in der Elternkomponente nach erfolgreicher Löschung zu aktualisieren, wird *onSuccess()* aufgerufen.

##### - BudgetList.jsx

BudgetList ist eine reine Darstellungskomponente für die Budget-Daten.

Sie erhält die Budgetdaten `props.budgets` als Array von der Elternkomponente `Budgets.jsx`. Die Daten werden formatiert 
(z.B. toFixed(2) für Beträge) und in einem responsiven Raster-Layout dargestellt. Außerdem werden Kategorie-Icons zur 
besseren Visualisierung genutzt.

##### - Toast.jsx

Die Toast-Komponente dient als Benachrichtigungssystem für Erfolgs- oder Fehlermeldungen für Useraktionen.
Sie akzeptiert als Typ `success` und `error`, um die Farbe des Toasts zu steuern (Erfolg=grün, Fehler=rot).
Der `useEffect`-Hook wird genutzt, um die Benachrichtigung nach 3 Sekunden automatisch auszublenden, indem *onClose* aufgerufen wird.