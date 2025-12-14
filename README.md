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

Die Anwendung hat vier Pages, die auf der linken Seite in einer horizontalen Navigationsleiste ausgewählt werden können.
Auf der Startseite der Anwendung wird eine Übersicht über den aktuellen Finanzstatus angezeigt.
Unter dem Kontostand befindet sich ein tagesaktuelles Liniendiagramm, dass den Verlauf des Kontostands der 
letzten 30 Tage darstellt. Darunter werden die letzten zehn Transaktionen angezeigt.

![balance chart](/assets/balance_chart.png)

Auf der Seite *Transactions* befindet sich im oberen Bereich ein Formular, mit dem Transaktionen angelegt werden können.
Nach Auswahl der Kategorie kann die passende Unterkategorie ausgewählt und der entsprechende Betrag eingegeben werden.
Mit einem Klick auf *Add transaction* wird die Transaktion entgegengenommen und erscheint als neuste Buchung im darunter
liegenden Fenster. Hier sind alle bisher getätigten Transaktionen von der aktuellsten zur ältesten Buchung aufgelistet. 
Mit dem Formular darüber kann nach Kategorien gefiltert werden.

![transaction menu](/assets/transactions.png)

Befindet man sich auf der Seite *Budgets* sieht man im oberen Bereich, ob schon Budgets für bestimmte Kategorien angelegt
sind. Für jede Kategorie kann genau ein Budget angelegt werden, das die Höhe der Ausgaben für den aktuellen Monat limitiert.
Würde eine neue Transaktion ein gesetztes Budgetlimit überschreiten, kann die Transaktion nicht durchgeführt werden.

![budgets](/assets/budgets.png)

## Systembeschreibung für Entwickler*innen



### UML-Diagramm

Das UML-Klassendiagramm stellt die statische Struktur des Finanzverwaltungssystems dar und zeigt die zentralen Klassen, ihre Attribute, Methoden sowie die Beziehungen zwischen ihnen. Die Architektur orientiert sich an einer Schichtenarchitektur, die eine klare Trennung von Zuständigkeiten ermöglicht.

#### Model-Schicht

Die Model-Schicht enthält die fachlichen Datenobjekte des Systems.

Die Klasse Transaction repräsentiert eine einzelne finanzielle Transaktion.
Sie enthält Attribute wie Betrag, Kategorie, Unterkategorie und Datum.
Diese Klasse dient ausschließlich als Datencontainer und enthält keine Logik zur Datenpersistenz.

Die Klasse Category (bzw. ein entsprechendes Enum) modelliert die möglichen Kategorien von Transaktionen.
Sie stellt eine zentrale, typisierte Definition der Kategorien dar und wird von anderen Klassen zur Konsistenz der Daten verwendet.

#### Persistenz-Schicht

Die Persistenz-Schicht ist für den Zugriff auf die SQLite-Datenbank zuständig.

Die Klasse SqliteDb kapselt sämtliche Datenbankoperationen.
Sie ist verantwortlich für das Speichern, Laden, Aktualisieren und Löschen von Transaktionen sowie für die Verwaltung von Budgets.

Öffentliche Methoden wie
save_transaction(...),
load_all_transactions(),
load_transactions_by_date_range(...) oder
save_budget(...)
stellen eine klar definierte Schnittstelle für andere Schichten bereit.

Interne Methoden zur Initialisierung der Datenbanktabellen (z. B. _create_table_transactions() und _create_table_budgets()) sind als private Methoden implementiert und werden im Konstruktor aufgerufen.
Diese Methoden sind Implementierungsdetails und dienen ausschließlich der technischen Initialisierung.

Die Persistenz-Schicht kennt die Model-Klassen, insbesondere Transaction, ist jedoch unabhängig von Controller- oder UI-Logik.

#### Controller- / Anwendungslogik

Die Controller- bzw. Anwendungslogik nutzt die Persistenz-Schicht, um auf gespeicherte Daten zuzugreifen, und verarbeitet diese für die weitere Verwendung in der Anwendung (z. B. Anzeige, Filterung oder Auswertung).

Der Zugriff erfolgt ausschließlich über die öffentlichen Methoden der Klasse SqliteDb, wodurch eine lose Kopplung zwischen Anwendungslogik und Datenbank gewährleistet wird.

Datenbank-Initialisierung (DbCreator)

Die Klasse DbCreator dient der Initialisierung und Befüllung der Datenbank mit Testdaten und wird ausschließlich beim Start der Anwendung in der Entwicklungsphase verwendet.

Sie erzeugt bei Bedarf die benötigten Tabellen und fügt realistisch simulierte Transaktionen über mehrere Jahre hinweg ein.

Die Klasse greift direkt auf die SQLite-Datenbank zu und ist thematisch der Persistenz zuzuordnen.

Sie ist jedoch kein Bestandteil der regulären Schichtenarchitektur, da sie nicht im normalen Anwendungsablauf verwendet wird, sondern lediglich als Hilfswerkzeug zur Datenbankvorbereitung dient.

Aus diesem Grund wird DbCreator entweder separat im UML-Diagramm dargestellt oder bewusst nicht in das Hauptdiagramm der Anwendungsarchitektur aufgenommen.

#### Zusammenfassung

Das UML-Diagramm verdeutlicht die klare Trennung zwischen Datenmodell, Persistenz und Anwendungslogik.
Durch die Kapselung der Datenbankzugriffe in der Persistenz-Schicht sowie die Auslagerung der Datenbankinitialisierung in ein separates Hilfsmodul wird eine wartbare, erweiterbare und übersichtliche Systemstruktur erreicht.

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