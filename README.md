

# 📊 Étude des données foncières (DVF)

Ce projet utilise les données issues de la base **Demandes de valeurs foncières (DVF)**, qui recense les transactions immobilières en France.
L’objectif est de réaliser des analyses pour l’investissement immobilier : prix au m², typologie des biens, rendement locatif, évolution du marché.

---

## 🔑 Variables principales (investissement immobilier)

1. **valeur\_fonciere** → Prix de vente du bien.
2. **surface\_reelle\_bati** → Surface habitable réelle.
3. **nombre\_pieces\_principales** → Typologie du logement (studio, T2, T3…).
4. **type\_local** → Nature du bien (Appartement, Maison, Dépendance…).
5. **localisation** :

   * **code\_postal**, **code\_commune**, **nom\_commune**
   * **adresse\_nom\_voie**, **adresse\_numero**
   * **longitude**, **latitude**
6. **date\_mutation** → Date de la transaction.

Ces variables sont **essentielles** pour calculer le prix au m², comparer avec les loyers, et estimer le rendement locatif.

---

## 📍 Variables secondaires (localisation et structure)

* **code\_departement** → Regroupement régional (ex : 75, 94, 91).
* **nombre\_lots**, **lotX\_surface\_carrez**, **lotX\_numero** → Infos sur les lots (cave, parking…).
* **id\_parcelle / ancien\_id\_parcelle** → Référence cadastrale.

---

## 🌱 Variables spécifiques (peu utiles en résidentiel)

* **nature\_culture / code\_nature\_culture** → Type de culture (vigne, verger, terre…).
* **nature\_culture\_speciale / code\_nature\_culture\_speciale** → Informations agricoles/forestières.

---

## 🏁 Priorisation pour un investisseur

1. **Prix et surface** → valeur\_fonciere, surface\_reelle\_bati.
2. **Typologie** → nombre\_pieces\_principales, type\_local.
3. **Localisation** → commune, code\_postal, latitude/longitude.
4. **Temporalité** → date\_mutation.
5. **Informations complémentaires** → lots, parcelles, culture (secondaire).


Veux-tu que je t’écrive aussi une **version anglaise** (README bilingue), pour que ton repo soit compréhensible par un public plus large ?
