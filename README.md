# Geheugendump Script voor Forensische Analyse

Welkom bij mijn geheugendump script! Dit script is speciaal ontwikkeld om de politie Nederland te helpen bij het analyseren van data van lopende processen op een computer. Met dit script kun je eenvoudig geheugendumps maken en analyseren voor forensisch onderzoek.

## Inhoud

- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Commands](#commands)
- [Veelvoorkomende Problemen en Oplossingen](#veelvoorkomende-problemen-en-oplossingen)
- [Bijdragen](#bijdragen)
- [Licentie](#licentie)
- [Ethisch Gebruik](#ethisch-gebruik)

## Installatie

Volg deze stappen om het script op je computer te installeren en voor te bereiden:

1. **Python Installeren**:
    - Download en installeer Python 3.x van [Python.org](https://www.python.org/downloads/).
    - Zorg ervoor dat je de optie "Add Python to PATH" aanvinkt tijdens de installatie.

2. **Vereiste Pakketten Installeren**:
    - Open de Command-Line Interface (CMD of PowerShell) als administrator.
    - Voer de volgende commando's uit om de benodigde pakketten te installeren:
      ```sh
      pip install frida psutil
      ```

## Gebruik

Hier is een korte uitleg over hoe je het script kunt gebruiken om een geheugendump te maken en te analyseren:

1. **Script Uitvoeren**:
    - Voer het script uit met de naam van het proces dat je wilt dumpen. Bijvoorbeeld:
      ```sh
      python Shadem.py <process_name>
      ```

2. **Proces Kiezen**:
    - Als je het script zonder procesnaam uitvoert, krijg je een lijst van lopende processen te zien. Kies het nummer van het proces dat je wilt dumpen en druk op Enter.

3. **Opties Configureren** (optioneel):
    - Je kunt verschillende opties toevoegen aan het commando om het gedrag van het script aan te passen.

## Commands

Hier zijn enkele commands en opties die je kunt gebruiken met het script:

1. **Basisgebruik**:
    - Dump het geheugen van een proces met de naam `my_app`:
      ```sh
      python Shadem.py my_app
      ```

2. **Specificeer een Uitvoermap**:
    - Dump het geheugen van een proces en sla de output op in een specifieke map:
      ```sh
      python Shadem.py my_app -o C:\path\to\output_directory
      ```

3. **Gebruik een USB-verbonden apparaat**:
    - Verbind met een proces dat draait op een USB-verbonden apparaat:
      ```sh
      python Shadem.py my_app -U
      ```

4. **Verbose logging inschakelen**:
    - Schakel gedetailleerde logging in voor debugging:
      ```sh
      python Shadem.py my_app -v
      ```

5. **Dump alleen read-only geheugen**:
    - Dump alleen de read-only gedeeltes van het geheugen:
      ```sh
      python Shadem.py my_app -r
      ```

6. **Strings analyse uitvoeren**:
    - Voer een strings-analyse uit op alle gedumpte bestanden:
      ```sh
      python Shadem.py my_app -s
      ```

7. **Maximale grootte van een dumpbestand instellen**:
    - Stel de maximale grootte van een dumpbestand in op 10 MB:
      ```sh
      python Shadem.py my_app --max-size 10485760
      ```

8. **Combinatie van opties**:
    - Combineer meerdere opties voor een specifiek gebruiksscenario:
      ```sh
      python Shadem.py my_app -o C:\path\to\output_directory -U -v -r -s --max-size 10485760
      ```

## Veelvoorkomende Problemen en Oplossingen

Hier zijn enkele veelvoorkomende problemen en hun oplossingen:

### Probleem: "Process not found"
- **Beschrijving**: Het script kan het opgegeven proces niet vinden.
- **Oplossing**:
  - Controleer de exacte naam van het proces zonder de extensie ".exe".
  - Zorg ervoor dat het proces daadwerkelijk draait.
  - Probeer de PID (Process ID) van het proces te gebruiken in plaats van de naam.

### Probleem: "Permission denied"
- **Beschrijving**: Het script heeft niet de benodigde rechten om het proces te injecteren.
- **Oplossing**:
  - Voer de command-line interface (CMD of PowerShell) uit als administrator.
  - Controleer of je voldoende rechten hebt om het doelproces te injecteren.

### Probleem: "Memory access violation"
- **Beschrijving**: Het script kan niet correct lezen van het opgegeven geheugenadres.
- **Oplossing**:
  - Dit kan normaal gedrag zijn bij sommige delen van het geheugen die beschermd zijn. Het script zal doorgaan met de volgende bereik.
  - Zorg ervoor dat je de juiste permissies hebt om toegang te krijgen tot het geheugen van het proces.

### Probleem: "Frida is not recognized as an internal or external command"
- **Beschrijving**: Frida is niet correct geïnstalleerd of de omgeving is niet correct geconfigureerd.
- **Oplossing**:
  - Zorg ervoor dat Frida correct is geïnstalleerd via pip:
    ```sh
    pip install frida
    ```
  - Controleer of de Python Scripts map is toegevoegd aan je PATH omgeving.

### Probleem: "Module not found"
- **Beschrijving**: De vereiste Python-modules zijn niet geïnstalleerd.
- **Oplossing**:
  - Zorg ervoor dat alle benodigde modules zijn geïnstalleerd:
    ```sh
    pip install frida psutil
    ```

## Bijdragen

Ik sta altijd open voor bijdragen en suggesties om dit project te verbeteren. Voel je vrij om een pull request in te dienen of een issue aan te maken als je een bug vindt of een functie wilt toevoegen.

## Licentie

Dit project is gelicentieerd onder de MIT-licentie. Zie het [LICENSE](LICENSE) bestand voor meer informatie.

## Ethisch Gebruik

Dit script is ontwikkeld voor ethische en legitieme doeleinden, zoals forensisch onderzoek en beveiligingstesten. Het is de verantwoordelijkheid van de gebruiker om ervoor te zorgen dat het script op een legale en ethische manier wordt gebruikt. Ongeautoriseerd gebruik van dit script voor kwaadaardige doeleinden is verboden en kan juridische gevolgen hebben. Gebruik dit script alleen voor doeleinden waarvoor je toestemming hebt.

Bedankt voor het gebruiken van mijn script! Als je vragen hebt of hulp nodig hebt, aarzel dan niet om contact met mij op te nemen.
