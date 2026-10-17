# Atlas des gisements mondiaux — World Twin (v0.5, 17/10/2026)

Atlas des gisements des sept hubs de la flotte monde, en données PUBLIQUES sourcées et étiquetées. Cet atlas répond au reste P2 « FAOSTAT multi-pays » : chaque hub porte désormais ses chiffres publics de contexte, croisés entre sources.

## Méthode et étiquettes

- `DONNÉES RÉELLES (source, campagne)` : statistique publique croisée, au minimum une source primaire (ministère, institut professionnel, FAOSTAT) ; en cas d'écart entre sources, la fourchette est donnée.
- `ILLUSTRATION` : ratio de littérature scientifique ou produit dérivé (ratio x surface publique). Jamais utilisé pour calibrer le moteur.
- Doctrine PI : les volumes adressables business (parts de marché, prix, potentiels nets) restent HORS du dépôt. Les chiffres ci-dessous sont des ordres de grandeur publics de contexte, destinés à la simulation et à la crédibilité du discours.
- Double check : l'oléiculture et la yerba mate alternent fortement d'une campagne à l'autre — toute citation externe doit porter la campagne. Les chiffres doivent être re-vérifiés à chaque usage externe (date de constitution : 17/10/2026).

## Vue d'ensemble

| Hub | Pays | Gisements publics de contexte | Étiquette |
| --- | --- | --- | --- |
| fr-rhone | France | Raisin 4,7-6,2 Mt ; maïs 14,7 Mt ; riz 72 kt ; noix 27,7 kt (FAOSTAT) | DONNÉES RÉELLES |
| ch-leman | Suisse | Vignes suisses ~15 000 ha ; Vaud 3 783 ha, un quart du vin suisse | DONNÉES RÉELLES |
| it-puglia | Italie | Huile 241 kt (2022) ; Puglia ~40 % de l'huile italienne ; olives de table 80-90 kt | DONNÉES RÉELLES |
| es-extremadura | Espagne | Huile 765-900 kt selon campagne ; oliveraie >300 kha, 14 % du verger national | DONNÉES RÉELLES |
| ar-cuyo | Argentine | Vigne Mendoza 145 393 ha, 70-75 % du vignoble argentin | DONNÉES RÉELLES |
| ar-misiones | Argentine | Yerba mate ~210 kha (87 % Misiones) ; feuille verte ~813-880 kt/an | DONNÉES RÉELLES |
| ma-atlas | Maroc | Olives 1,07-1,97 Mt selon campagne ; Fès-Meknès 320 kha, >32 % du verger national | DONNÉES RÉELLES |

## Fiches par hub

### fr-rhone — France (pilote v0)

Extraction FAOSTAT v0.1 : raisin 4,7 à 6,2 Mt/an, maïs 14,7 Mt/an, riz paddy 72 kt/an, noix 27,7 kt/an. Le détail complet vit dans pilote-france-2027.md ; le potentiel national business reste hors dépôt (doctrine PI).

### ch-leman — Suisse (Lavaux-Léman)

Surface viticole suisse totale : 14 793 ha (OFAG, 2015 ; environ 15 000 ha). Canton de Vaud : 3 783 ha de vignes, environ un quart de la production suisse de vin, huit appellations AOC dont Lavaux — terrasses classées au patrimoine mondial de l'UNESCO (2007). Potentiel sarments vaudois `ILLUSTRATION` : 3 783 ha x 1-3 t MS/ha ≈ 3,8 à 11,3 kt MS/an.

### it-puglia — Italie (Puglia-Tavoliere, Foggia)

Huile d'olive italienne : 241 kt (2022, ISMEA sur données Agea, −27 % lié au climat et à l'alternance) ; l'Italie reste le deuxième producteur mondial derrière l'Espagne (854 kt, 2023, FAOSTAT/COI). La Puglia produit environ 40 % de l'huile italienne (analyses sectorielles convergentes). Olives de table nationales : 80 à 90 kt/an (MASAF). Contexte : la crise Xylella a réduit le verger apulien ; les replantations en variétés résistantes sont en cours. Gisement cible du hub : grignons d'olive (ratio `ILLUSTRATION` 0,4-0,6 t par tonne d'olives triturées).

### es-extremadura — Espagne (Estrémadure)

Huile d'olive espagnole : prévision 765,3 kt pour la campagne 2023/24 (MAPA), campagne finale autour de 850-900 kt ; premier producteur mondial. Oliveraie d'Estrémadure : plus de 300 000 ha (2025), environ 14 % de la surface oléicole nationale, dont 75 956 ha d'olives de table en propre et 71 434 ha à double aptitude. Rendements des plantations intensives récentes : 10 000 à 12 000 kg d'olives par hectare. Observable réel de croisement : en Andalousie 2024/25, 4,45 Mt d'olives de mouture ont donné 852 943 t d'huile (Junta de Andalucía), soit environ 19 % de rendement — cohérent avec le ratio `ILLUSTRATION` 15-20 %.

### ar-cuyo — Argentine (Cuyo-Mendoza, hémisphère Sud)

Vignoble de Mendoza : 145 393 ha plantés (2024 ; les analyses sectorielles convergent autour de 146-150 kha), soit 70 à 75 % des surfaces et de la production de vin argentines. Potentiel sarments `ILLUSTRATION` : 145 393 ha x 1-3 t MS/ha ≈ 145 à 436 kt MS/an, disponible pendant la fenêtre de taille hivernale de juin à août — l'anti-saison parfait de l'hémisphère Nord.

### ar-misiones — Argentine (Misiones, hémisphère Sud)

Yerba mate argentine : environ 210 000 ha cultivés (87 % Misiones, 13 % Corrientes ; INYM). Production de feuille verte : 703 312 t (2011) → 812 995 t (2020) (INYM), autour de 880 000 t/an récemment. Tissu productif : environ 12 700 producteurs et 15 000 tareferos. Nuance réelle de zafra 2025 : Corrientes, avec moins de 15 % de la surface, a dépassé Misiones en feuille verte en début de campagne — la répartition régionale évolue, à suivre année par année.

### ma-atlas — Maroc (Al-Atlas, Meknès)

Production nationale d'olives : 1,968 Mt (2021/22) ; 1,086 Mt (2022/23) ; environ 1,072 Mt (2023/24) — forte fluctuation liée au déficit hydrique. Région Fès-Meknès : 320 000 ha, plus de 32 % de la surface oléicole nationale, dont 40 000 ha sur la seule province de Meknès ; la production régionale a déjà dépassé 1 Mt (2017/18 : 1 027 573 t, direction régionale de l'Agriculture). Premier bassin oléicole du royaume.

## Ratios de conversion (ILLUSTRATION, littérature)

- Grignons d'olive : 0,4 à 0,6 t de grignons bruts par tonne d'olives triturées.
- Sarments de vigne : 1 à 3 t MS/ha/an (1 à 5 selon cépage et conduite).
- Rendement huile : 15 à 20 % du poids d'olives (croisé avec l'observable réel andalou 2024/25 ≈ 19 %).

Ces ratios alimentent l'ordre de grandeur, jamais le calibrage : le moteur World Twin reste non calibré et toutes ses sorties restent étiquetées SYNTHÉTIQUE.

## Version machine

engine/atlas_gisements.py porte les mêmes données sous forme de constantes Python, avec la même étiquette par chiffre, et un contrôle de couverture automatique contre les hubs de engine/monde.py.

## Sources

FAOSTAT (division statistique de la FAO) ; Conseil Oléicole International ; MAPA (Espagne) ; Junta de Andalucía (aforo 2024/25) ; ISMEA/Agea (Italie) ; MASAF (Italie) ; INYM (Argentine) ; OFAG (Suisse) ; presse agricole vérifiée reprenant des données ministérielles (Agrimaroc, LesEco, Extremadura21, Misiones Plural, Clarín Rural) ; littérature scientifique sur les résidus agricoles pour les ratios. Détail des accès : sources-donnees.md.

## Étape suivante

La lecture des résultats Monte Carlo vit dans engine/lecture_resultats.py (v0.5) : classement des hubs, sensibilité au figeage, synthèse du dernier run. Reste P2+ : fiches pays réglementaires, croisement GEOGLAM, FIRMS historique multi-saison.
