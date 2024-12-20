# Edit Distance with Autocorrect and Phrase Suggestions

Një projekt i bazuar në Python që implementon një algoritëm të autokorrektimit. Përdor algoritmin për të sugjeruar korrigjime dhe fraza alternative bazuar në një fjalor. Përfshin një ndërfaqe grafike të ndërtuar me `tkinter`.

- Rita Berisha [@ritaberishaa](https://github.com/ritaberishaa)
- Shpat Mjeku [@shpatmjeku](https://github.com/shpatmjeku)
- Yll Sheremeti [@YllSheremeti](https://github.com/YllSheremeti)
- Yll Pllana [@YlliPllana](https://github.com/YlliPllana)
---

## Karakteristikat
- **Edit Distance Algorithm**: Llogarit numrin minimal të operacioneve (shtime, fshirje, zëvendësime) të nevojshme për të transformuar një fjalë ose frazë në një tjetër.
- **Korrigjimi i Frazave**: Mbështet llogaritjen e distancës së editimit në nivel fraze.
- **Sugjerime Autokorrektimi**: Sugjeron alternativa bazuar në një fjalor të ngarkuar paraprakisht, me një prag të konfiguruar për distancën e editimit.
- **Graphical User Interface (GUI)**: Përfshin një ndërfaqe grafike interaktive për përdorim të lehtë.

---


## Instalimi

1. Klononi depozitën:
    ```bash
    git clone https://github.com/emri-juaj/edit-distance-autocorrect.git
    cd edit-distance-autocorrect
    ```
2. Sigurohuni që Python është instaluar në sistemin tuaj.

---

## Përdorimi
1. Run "main.py"
2. Futni frazën tuaj të kërkimit në kutinë e hyrjes.

3. Shtypni **Get Suggestions** ose klikoni `Enter` për të parë sugjerimet bazuar në algoritmin e distancës së editimit.

4. Sugjerimet do të shfaqen në një tabelë që tregon:
    - Fraza e sugjeruar.
    - Distanca e llogaritur e editimit nga kërkesa juaj.

---

## Si funksionon
### Komponentët kryesorë
- **Edit Distance**:
    Funksioni `edit_distance` llogarit numrin minimal të operacioneve për të transformuar një fjalë në një tjetër.
    
- **Distanca e Editimit të Frazave**:
    Funksioni `phrase_edit_distance` aplikon distancën e editimit në nivel fjale në fraza të tëra.

- **Motori i Sugjerimeve**:
    Funksioni `suggest_corrections` rendit sugjerimet nga fjalori bazuar në distancën e tyre të editimit ndaj frazës së kërkuar.

- **Ngarkimi i Fjalorit**:
    Funksioni `load_dictionary` lexon një skedar teksti që përmban të dhënat e fjalorit, duke siguruar ekzistencën dhe formatimin e duhur të tij.

- **Ndërfaqja Grafike (GUI)**:
    Ndërtuar duke përdorur `tkinter`, GUI lejon përdoruesit të fusin kërkesa, të shikojnë sugjerime dhe të bashkëveprojnë me mjetin lehtë.

---

## Struktura e projektit
- `main.py`: File kryesor që përmban të gjitha funksionalitetet dhe logjikën.
- `dictionary.txt`: Skedari i fjalorit i përdorur për të sugjeruar korrigjime.

---



## Screenshots
**

