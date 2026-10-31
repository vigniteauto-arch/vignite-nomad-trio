# Fiches pays réglementaires — brûlage des résidus agricoles (v2.0, 31/10/2026)

Réédition sourcée des fiches réglementaires du brûlage des résidus agricoles pour les sept juridictions P2 du programme World Twin (fr-rhone, ch-leman, it-puglia, es-extremadura, ar-cuyo, ar-misiones, ma-atlas). Elle remplace la version v0.6 du 17/10/2026 et est portée au dépôt par la vague V1.9 avec le module machine engine/fiches_reglementation.py.

Chaque élément juridique a été revérifié le 31/10/2026 par croisement d'au moins deux sources, dont la source officielle primaire chaque fois qu'elle était accessible (Légifrance, Fedlex, Normattiva, Boletín Oficial del Estado, Diario Oficial de Extremadura, Infoleg, Digesto de Misiones, Secrétariat général du gouvernement marocain). Ce document est un registre de travail et de développement : il ne constitue pas une consultation juridique. Toute décision d'engagement opérationnel dans une juridiction donnée exige la validation par un conseil juridique local.

## Méthode et étiquettes

- `DONNÉES RÉELLES` : texte lu à la date indiquée sur la source primaire ou officielle.
- `À VÉRIFIER` : élément non confirmé à la date de vérification — à sourcer avant tout usage externe.
- Vérification effectuée le 31/10/2026 par recherche documentaire croisée. La réglementation évolue : toute citation externe exige une re-vérification datée.
- Aucune valeur calibrée n'est versionnée (doctrine PI — propriété intellectuelle) et tout résultat de simulation reste étiqueté SYNTHÉTIQUE.
- Lancement du module machine : `python3 engine/fiches_reglementation.py` (sommaire), `python3 engine/fiches_reglementation.py ar-cuyo` (fiche d'une juridiction), `python3 engine/fiches_reglementation.py croisement` (gardes complètes : couverture des hubs de engine/monde.py, structure, étiquettes, textes pivots, correctifs de la v2.0).

## Découverte centrale — la Ley 26.562 argentine se lit avec la Ley 26.815

La Ley 26.562 (Boletín Oficial du 16/12/2009, présupposés minimaux pour le contrôle des activités de brûlage) reste en vigueur mais est complétée et modifiée par la Ley 26.815 de gestion du feu (Boletín Oficial du 16/01/2013, modifiée par la Ley 27.591 du 14/12/2020) : Système fédéral de gestion du feu, Service national de gestion du feu, Fonds national de gestion du feu en fiducie (contribution de 3 pour mille des primes d'assurance hors vie), autorité d'application le ministère de la Sécurité de la Nation (confirmé par le Decreto 73/2026, Boletín Oficial du 30/01/2026). La v0.6 citait la seule Ley 26.562 : la v2.0 corrige cette lacune, les deux lois se lisent ensemble.

Contenu de la Ley 26.562 : article 2 définition de la quema (élimination de végétation ou de résidus par le feu en vue d'un usage productif du terrain), article 3 interdiction de toute quema sans autorisation de l'autorité locale, articles 4 à 6 conditions et informations exigées (données du responsable et du titulaire, consentement, identification de la parcelle, objectif, techniques d'allumage et d'extinction, mesures de sécurité, date et heure), article 7 normes provinciales complémentaires et sanctions supplétives (avertissement, amende jusqu'à 10 000 salaires de base de la catégorie initiale de l'administration publique nationale, suspension ou révocation), article 8 aucune exemption des normes forestières.

## Vue d'ensemble

| Hub | Juridiction | Statut du brûlage des résidus agricoles | Texte pivot | Sanction maximale identifiée |
| --- | --- | --- | --- | --- |
| fr-rhone | France (département du Rhône) | Interdiction de principe, dérogation préfectorale exceptionnelle à objectif sanitaire | Code de l'environnement, article L.541-21-1 II | Contravention de 4e classe, 750 €, forfaitaire 135 € |
| ch-leman | Suisse (canton de Vaud) | Interdiction de principe, incinération admise uniquement en installation | Ordonnance sur la protection de l'air (OPair), article 26a | Régime pénal de la loi sur la protection de l'environnement (LPE) |
| it-puglia | Italie (région Pouilles) | Encadré : tas de 3 m³ par hectare et par jour hors périodes de haut risque, chaumes soumis au régime du ringrano | Décret législatif 152/2006, article 182, alinéa 6-bis | Régime de la loi 353/2000 et de la loi régionale (LR) 38/2016 |
| es-extremadura | Espagne (Estrémadure) | Interdiction générale des résidus végétaux agricoles et forestiers, exceptions encadrées | Ley 7/2022 du 8 avril, article 27.3 | Régime d'infractions de la Ley 7/2022 et du plan Infoex |
| ar-cuyo | Argentine (province de Mendoza) | Autorisation obligatoire à trois niveaux (fédéral, provincial, communal) | Ley 26.562 lue avec la Ley 26.815, Ley 6.099 de Mendoza | Amende fédérale supplétoire jusqu'à 10 000 salaires de base, 70 millions de pesos argentins à Mendoza en 2026 |
| ar-misiones | Argentine (province de Misiones) | Interdiction générale en milieu rural, exceptions agricoles soumises à plan approuvé — régime le plus restrictif des sept | Résolution 293/2020 de Misiones | Régime provincial du plan de gestion du feu, montants par voie locale |
| ma-atlas | Maroc (région de l'Atlas) | Aucune norme nationale dédiée identifiée, cadres généraux de l'air et des déchets | Loi 13-03 sur la pollution de l'air, Loi 28-00 sur les déchets | Sanctions des lois 13-03 et 28-00, à vérifier |

## Fiche fr-rhone — France (département du Rhône)

Statut : interdiction de principe. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur Légifrance).

Cadre. L'article L.541-21-1 II du code de l'environnement, en vigueur depuis le 1er janvier 2021, dispose que les biodéchets ne peuvent être éliminés par brûlage à l'air libre ni au moyen d'équipements ou de matériels extérieurs. À titre exceptionnel et aux seules fins d'éradication d'épiphytie ou d'élimination d'espèces végétales envahissantes, des dérogations individuelles peuvent être délivrées par le représentant de l'État dans le département. La circulaire du 18 novembre 2011 constitue la base historique de l'interdiction.

Conditionnalité agricole. La fiche Telepac 2026 de la politique agricole commune (PAC) confirme la condition de bonne condition agricole et environnementale numéro 3 (BCAE 3) : le brûlage des chaumes et autres résidus de culture est interdit, sauf dérogation préfectorale à objectif sanitaire. Le manquement constaté en contrôle entraîne une réduction des aides de 3 % au premier constat, puis de 9 % en cas de récidive sur trois ans.

Sanctions. L'article R.541-78 du code de l'environnement punit le brûlage illicite d'une contravention de 4e classe, passible de 750 € au maximum, avec amende forfaitaire de 135 €. Le doublement des sanctions par la loi 2023-973 du 23 octobre 2023 relative à l'industrie verte (article L.541-46) est conservé de la v0.6 et `À VÉRIFIER` sur Légifrance avant toute citation externe.

Angle Vignite. Le gisement rhodanien est juridiquement verrouillé : chaque tonne enfumée est à la fois un gisement perdu pour la thermo-compression et une émission de CO2e (équivalent CO2) sans valeur. La collecte et la valorisation sur site offrent la seule voie conforme. Détections Firms (Fire Information for Resource Management System) du 17/10/2026 : 11 points chauds en Camargue voisine.

Sources croisées : Légifrance (article L.541-21-1), portail national de l'information sur l'habitat (article R.541-78), fiche Telepac 2026 — consultées le 31/10/2026.

## Fiche ch-leman — Suisse (canton de Vaud)

Statut : interdiction de principe, l'incinération des déchets est admise uniquement dans des installations. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur Fedlex).

Cadre fédéral. L'article 26a de l'ordonnance sur la protection de l'air (OPair, recueil systématique RS 814.318.142.1) admet l'incinération des déchets uniquement dans des installations relevant du chiffre 7 de l'annexe 2, à l'exclusion des déchets visés au chiffre 11. L'article 30c de la loi sur la protection de l'environnement (LPE) encadre l'incinération en plein air.

Cadre cantonal. L'instruction conjointe du Service des forêts, de la faune et de la nature (SFFN) et du Service de l'environnement et de l'énergie (SEVEN) du 20 novembre 2006 fonde la pratique des dérogations communales pour les rémanents forestiers : des exceptions demeurent possibles mais étroites et motivées au cas par cas, avec priorité à la valorisation matière.

Sanctions. Régime pénal de la loi sur la protection de l'environnement (LPE). Les modalités exactes d'amende pour le brûlage agricole en zone ouverte restent `À VÉRIFIER` auprès de l'autorité cantonale.

Angle Vignite. L'ordonnance sur la protection de l'air (OPair) exige une installation : c'est précisément ce qu'est une unité Nomad. Le bassin lémanique est la juridiction où la conformité de Vignite est la plus littéralement alignée sur le texte. Détections Firms du 17/10/2026 : aucun point chaud significatif au nord du Léman.

Sources croisées : Fedlex (article 26a), JuriUp, canton de Vaud — consultés le 31/10/2026.

## Fiche it-puglia — Italie (région Pouilles)

Statut : encadré, avec verrou météo régional et régime spécifique pour les chaumes. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur Normattiva).

Cadre national. Le décret législatif 152/2006 (code de l'environnement italien) est la référence. L'article 182, alinéa 6-bis, introduit en 2022, autorise le ramassage et le brûlage sur place des broussailles sèches, des tontes et des tailles, en tas d'un volume maximal de 3 m³ par hectare et par jour, en dehors des périodes de haut risque d'incendie déclarées par la région, et en vue du réusage comme fertilisant ou amendement. L'article 185 exclut du régime des déchets les matières dont l'usage agricole est démontré. La loi 353/2000 constitue le socle pénal national.

Cadre régional. La loi régionale (LR) 38/2016 régit les incendies de forêt et d'interface. La délibération de la junte régionale (DGR) 1149 du 28 juin 2018 encadre le brûlage des chaumes et des pailles : il n'est autorisé que dans le cadre de la pratique du ringrano (régénération des pailles) avec mise en culture de secondes récoltes sur surfaces irrigables, après communication préalable par formulaire certifié au maire et au Département régional de l'agriculture. En dehors de ce cadre, le brûlage des chaumes est toujours interdit.

Sanctions. Régime de la loi 353/2000 en cas d'incendie, complété par les sanctions régionales de la loi régionale (LR) 38/2016. Montants exacts `À VÉRIFIER` selon la qualification.

Angle Vignite. Même le régime dit permissif exige une preuve de réusage agricole. Vignite inverse la logique : au lieu de prouver le brûlage utile, l'agriculteur vend la paille et gagne sans feu. Détections Firms du 17/10/2026 : 4 points chauds autour de Tarente et de Foggia.

Sources croisées : Normattiva (article 182, alinéa 6-bis), Bulletin officiel de la région Poulies (loi régionale (LR) 38/2016), Bussola normativa (délibération de la junte régionale (DGR) 1149/2018), informations quotidiennes du Centre fonctionnel décentralisé — consultées le 31/10/2026.

## Fiche es-extremadura — Espagne (Estrémadure)

Statut : interdiction générale, avec exceptions encadrées et verrou saisonnier. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur le Boletín Oficial del Estado et le Diario Oficial de Extremadura).

Cadre national. La Ley 7/2022 du 8 avril sur les déchets et les sols contaminés dispose à son article 27.3 qu'en règle générale, la combustion de résidus végétaux issus du milieu agricole ou forestier n'est pas permise. Le texte ménage des exceptions liées à la directive (Union européenne) 2016/2284 (annexe III, partie 2, lettre C, considérant 22). La note interprétative du ministère de la Transition écologique (MITECO) du 26 janvier 2023 précise la notion de residuo vegetal de origen agrario.

Cadre régional. La Résolution du 30 décembre 2022 de la direction générale des situations d'urgence détaille les instructions d'application de l'article 27.3 sur le territoire régional. L'Orden du 26 mai 2026 (Diario Oficial de Extremadura n° 100 du 27 mai 2026) établit l'époque de danger élevé du 1er juin 2026 au 15 octobre 2026 (plan de lutte contre les incendies de forêt d'Estrémadure, Infoex). L'Orden du 9 octobre 2026 (Diario Oficial de Extremadura du 15 octobre 2026) établit l'époque de danger faible en vigueur à la date de vérification.

Sanctions. Régime d'infractions de la Ley 7/2022 pour la partie déchets, et des órdenes saisonnières pour l'usage du feu en zone forestière. Montants `À VÉRIFIER` selon la qualification avant tout engagement.

Angle Vignite. L'Estrémadure combine une interdiction nationale de principe, une instruction régionale détaillée et un verrou saisonnier dur : c'est le cas d'école du marché adressable — de grandes surfaces de cultures permanentes et d'oliveraies dont les résidus ne peuvent plus être brûlés, sans filière de substitution structurée. Détections Firms du 17/10/2026 : 2 points chauds.

Sources croisées : Boletín Oficial del Estado (Ley 7/2022), conseil de l'agriculture de la Junte d'Estrémadure, ministère de la Transition écologique (MITECO), Résolution du 30/12/2022, Diario Oficial de Extremadura (órdenes des 26/05/2026 et 09/10/2026), portail Infoex — consultés le 31/10/2026.

## Fiche ar-cuyo — Argentine (province de Mendoza)

Statut : autorisation obligatoire à trois niveaux, fédéral, provincial et communal. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur Infoleg).

Cadre fédéral. La Ley 26.562 (lue avec la Ley 26.815, voir la découverte centrale) fixe les présupposés minimaux de protection environnementale pour le contrôle des activités de brûlage : définition de la quema, interdiction sans autorisation, conditions et informations exigées, sanctions supplétives, aucune exemption des normes forestières. La Ley 26.815 institue le Système fédéral de gestion du feu, le Service national de gestion du feu et le Fonds national de gestion du feu en fiducie, l'autorité d'application étant le ministère de la Sécurité de la Nation (Decreto 73/2026).

Cadre provincial. La Ley 6.099 de Mendoza interdit l'usage du feu en zones urbaines et rurales, sous réserve des autorisations du régime. La Résolution 1946/23 de la direction des ressources naturelles renouvelables (DRNR) du 20 septembre 2023 établit la procédure d'autorisation des brûlages prescrits de pâturages en zones de secano. Le Plan provincial de gestion du feu a annoncé le 14 janvier 2026 des amendes saisonnières pouvant atteindre 70 millions de pesos argentins (140 000 unités fiscales (UF) à 500 pesos argentins chacune, actualisant la valeur de 58 millions citée par la v0.6), recouvrées par l'administration tributaire de Mendoza (ATM), avec surveillance satellitaire et application Satellites on Fire.

Sanctions. Voir ci-dessus — `DONNÉES RÉELLES` (annonce officielle du 14/01/2026, presse concordante multiple). Le périmètre exact des unités fiscales (UF) pour la conversion des amendes saison 2027 reste `À VÉRIFIER`.

Angle Vignite. Cuyo vit sous une triple contrainte avec une surveillance satellitaire active et des amendes 2026 en forte hausse. Le marché de proximité est double : les viticulteurs et producteurs qui ne peuvent plus brûler leurs sarments et résidus, et les gestionnaires de pâturages qui doivent aujourd'hui brûler à titre prescrit — la thermo-compression compacte et valorise sans feu. Détections Firms du 17/10/2026 : aucune détection signalée sur la zone du hub au relevé du jour.

Sources croisées : Infoleg (Ley 26.562 et Ley 26.815), Boletín Oficial argentin (Decreto 73/2026), portail Argentina.gob.ar, Système argentin d'information juridique (SAIJ), ArgentinaForestal (annonce du 14/01/2026), Agrositio (Ley 6.099), Ecofield (Résolution 1946/23) — consultés le 31/10/2026.

## Fiche ar-misiones — Argentine (province de Misiones)

Statut : interdiction générale en milieu rural, avec exceptions agricoles soumises à plan approuvé — régime le plus restrictif des sept juridictions. Ce statut comble le point `À VÉRIFIER` de la v0.6. Éléments `DONNÉES RÉELLES` (vérifiés le 31/10/2026 sur le Digesto de Misiones).

Cadre provincial. La Ley XVI n° 65 (ancienne Ley 3.751 de l'an 2000) institue le Plan provincial de gestion du feu, place l'autorité d'application auprès du ministère de l'Écologie, crée la Red de Alerta y Emergencia Provincial (RAEP, réseau d'alerte et d'urgence provincial) et le fonds provincial de gestion du feu (FEPPCIFR). La Résolution 293/2020 du 20 août 2020 du ministère de l'Écologie et des ressources naturelles renouvelables interdit toute quema en milieu rural sur l'ensemble du territoire de la province ainsi que tout usage du feu en milieu rural, à une exception près : la quema ouverte contrôlée de matériel végétal résiduel issu des récoltes, de la préparation du sol et du renouvellement des pâturages, aux conditions fixées par la résolution, avec renvoi exprès à l'article 140 de la Ley 26.815.

Procédure. Le formulaire officiel de demande et de plan de brûlage contrôlé (édition du ministère de l'Écologie de juillet 2026) exige une déclaration sur l'honneur de connaissance de la Ley 26.562, de la Ley 26.815, de la Ley XVI n° 65 et de la Résolution 293/2020, et rappelle que le plan soumis ne vaut pas autorisation tant qu'il n'est pas approuvé par l'autorité provinciale. La procédure est une exception encadrée, non un droit.

Sanctions. Régime provincial du plan de gestion du feu, complété par les sanctions supplétives de l'article 7 de la Ley 26.562. Montants exacts `À VÉRIFIER` par voie locale.

Angle Vignite. Misiones concentre la culture sur brûlis traditionnelle : la zone la plus sensible et le marché le plus net — l'interdiction existe, il ne manque que la filière de substitution. Détections Firms du 17/10/2026 : 1 point chaud.

Sources croisées : Digesto de Misiones (Ley XVI n° 65), ministère de l'Écologie de Misiones (formulaire de juillet 2026), texte officiel de la Résolution 293/2020, portail du Plan provincial de gestion du feu, base FAOLEX de l'Organisation des Nations unies pour l'alimentation et l'agriculture (FAO) — consultés le 31/10/2026.

## Fiche ma-atlas — Maroc (région de l'Atlas)

Statut : aucune norme nationale dédiée au brûlage agricole identifiée à la date de vérification, cadres généraux de la qualité de l'air et de la gestion des déchets. Ce statut précise le point `À VÉRIFIER` de la v0.6. Éléments `DONNÉES RÉELLES` sur les textes cités, constat d'absence `À VÉRIFIER`.

Cadre national, air. La Loi n° 13-03 relative à la lutte contre la pollution de l'air (dahir n° 1-03-61 du 12 mai 2003, Bulletin officiel marocain n° 5118 du 19 juin 2003) constitue le cadre général des émissions atmosphériques. Le décret n° 2-09-286 du 8 décembre 2009 fixe les normes de qualité de l'air, modifié par le décret n° 2-23-244 du 7 mars 2024. Aucun de ces textes ne comporte de disposition dédiée au brûlage des résidus agricoles d'après les consultations du 31/10/2026.

Cadre national, déchets. La Loi n° 28-00 relative à la gestion des déchets (dahir n° 1-06-153 du 22 novembre 2006, Bulletin officiel marocain n° 5480 du 7 décembre 2006) consacre son Titre III aux déchets agricoles : article 24 dépôt dans les lieux d'élimination désignés par le plan directeur régional, article 25 réception contre redevance par le service communal, article 10 couverture des déchets agricoles par les plans directeurs régionaux. La voie légale marocaine pour les résidus agricoles est donc le dépôt et la collecte organisés, non le brûlage, sans que celui-ci soit nommément interdit par un texte national identifié.

Constat et réserve. Le constat d'absence de norme nationale dédiée reste `À VÉRIFIER` : des arrêtés du gouverneur, des règlements régionaux ou des règles de gestion forestière (domaines relevant du Haut-Commissariat aux eaux et forêts) peuvent encadrer le feu en pratique. Ce point doit être confirmé par un conseil local avant tout engagement opérationnel de la filiale Al-Atlas.

Angle Vignite. Le vide relatif du droit marocain est un piège et une opportunité. Un piège, car l'absence d'interdiction explicite n'autorise rien : un brûlage de grande ampleur resterait exposé au regard de la Loi 13-03 et à un risque réputationnel fort pour un partenaire institutionnel. Une opportunité, car Vignite peut apporter la conformité par anticipation et se positionner en standard de la filière avant même que la norme n'existe — jamais couvrir un brûlage, toujours valoriser le procédé sans feu à l'air libre. Détections Firms du 17/10/2026 : 2 points chauds sur la zone.

Sources croisées : ministère de la Transition énergétique et du Développement durable marocain (Loi 13-03), JuriMaroc (décret 2-09-286), Secrétariat général du gouvernement marocain (texte consolidé de la Loi 28-00 au 30 juillet 2025), Bulletin officiel marocain, base de l'Unité d'évaluation environnementale du Programme des Nations unies pour l'environnement (UNEP) — consultés le 31/10/2026.

## Lecture stratégique transversale

Premier constat : la voie du feu se referme partout, par des chemins différents. La France et la Suisse énoncent une interdiction de principe avec dérogation d'exception. L'Espagne énonce une interdiction générale par la Ley 7/2022 avec verrou saisonnier régional. L'Italie encadre strictement par des volumes et un verrou météo régional. L'Argentine impose l'autorisation à trois niveaux, et Misiones va jusqu'à l'interdiction générale en milieu rural avec exceptions approuvées plan par plan. Le Maroc n'a pas encore écrit sa norme dédiée. Aucune des sept juridictions n'offre aujourd'hui un droit au brûlage simple, et la trajectoire de chacune va vers plus de contrainte, pas moins.

Deuxième constat : l'argument de conformité est un argument commercial de premier rang. Dans les sept juridictions, le discours de Vignite n'est pas de demander une faveur, il est d'apporter la solution que la norme exige ou anticipera. La conformité transforme l'agriculteur de contrevenant potentiel en partenaire régulier, sans changement de sa productivité.

Troisième constat : l'argument techfin carbone complète l'argument réglementaire. Chaque tonne de biomasse enfumée est un double gâchis, un gisement perdu pour la thermo-compression et une émission de CO2e (équivalent CO2) sans contrepartie de crédit carbone. La réglementation ferme la voie de l'émission, le techfin ouvre la voie de la rémunération de la non-émission.

Quatrième constat : les détections Firms (Fire Information for Resource Management System) du 17/10/2026 confirment que la pratique du brûlage reste réelle dans cinq des sept zones (11 points en Camargue voisine du hub fr-rhone, 4 dans les Pouilles, 2 en Estrémadure, 1 à Misiones, 2 dans l'Atlas, aucun sur le bassin lémanique, aucune signalée sur la zone ar-cuyo au relevé du jour). L'écart entre la norme écrite et la pratique observée mesure le marché adressable de substitution : chaque point chaud est un gisement juridiquement perdu que Vignite peut reconvertir en contrat.

Cinquième constat : le cas marocain appelle une doctrine de communication dédiée. Vendre la conformité là où la norme manque exige de ne jamais donner l'impression de couvrir un brûlage, mais au contraire de valoriser l'apport d'un procédé sans feu à l'air libre au regard de la Loi 13-03 sur la pollution de l'air. Le positionnement Fahm et Fahima de la filiale Al-Atlas s'inscrit dans ce cadre de communication prudente.

## Registre des vérifications

| Élément | Date de vérification | Sources croisées | Étiquette |
| --- | --- | --- | --- |
| France, article L.541-21-1 II du code de l'environnement | 31/10/2026 | Légifrance, doctrine administrative | DONNÉES RÉELLES |
| France, condition BCAE 3 de la politique agricole commune (PAC) | 31/10/2026 | Fiche Telepac 2026 | DONNÉES RÉELLES |
| France, article R.541-78 du code de l'environnement | 31/10/2026 | Portail national de l'information sur l'habitat | DONNÉES RÉELLES |
| France, loi 2023-973 industrie verte | 17/10/2026 (v0.6) | Doctrine associative, non re-vérifiée sur Légifrance | À VÉRIFIER |
| Suisse, ordonnance sur la protection de l'air (OPair) article 26a | 31/10/2026 | Fedlex, JuriUp | DONNÉES RÉELLES |
| Suisse, canton de Vaud, dérogations déchets verts | 31/10/2026 | Canton de Vaud, instruction SFFN et SEVEN du 20/11/2006 | DONNÉES RÉELLES |
| Italie, décret législatif 152/2006, article 182, alinéa 6-bis | 31/10/2026 | Normattiva, doctrine à jour d'octobre 2026 | DONNÉES RÉELLES |
| Pouilles, loi régionale (LR) 38/2016 et délibération de la junte régionale (DGR) 1149/2018 | 31/10/2026 | Bulletin officiel des Pouilles, Bussola normativa | DONNÉES RÉELLES |
| Espagne, Ley 7/2022 article 27.3 | 31/10/2026 | Boletín Oficial del Estado (BOE), Junte d'Estrémadure, ministère de la Transition écologique (MITECO) | DONNÉES RÉELLES |
| Estrémadure, órdenes saisonnières 2026 | 31/10/2026 | Diario Oficial de Extremadura (DOE) n° 100 du 27/05/2026 et édition du 15/10/2026, portail Infoex | DONNÉES RÉELLES |
| Argentine, Ley 26.562 | 31/10/2026 | Infoleg, Système argentin d'information juridique (SAIJ) | DONNÉES RÉELLES |
| Argentine, Ley 26.815 modifiée par la Ley 27.591 | 31/10/2026 | Infoleg, Boletín Oficial argentin, portail Argentina.gob.ar | DONNÉES RÉELLES |
| Argentine, autorité d'application de la Ley 26.815 | 31/10/2026 | Decreto 73/2026, Boletín Oficial du 30/01/2026 | DONNÉES RÉELLES |
| Mendoza, Ley 6.099 et Résolution 1946/23 de la direction des ressources naturelles renouvelables (DRNR) | 31/10/2026 | Presse agricole spécialisée, portails provinciaux | DONNÉES RÉELLES |
| Mendoza, amendes saison 2026 du plan provincial de gestion du feu | 31/10/2026 | Annonce du 14/01/2026, presse concordante multiple | DONNÉES RÉELLES |
| Misiones, Ley XVI n° 65 | 31/10/2026 | Digesto de Misiones, base FAOLEX de l'Organisation des Nations unies pour l'alimentation et l'agriculture (FAO) | DONNÉES RÉELLES |
| Misiones, Résolution 293/2020 | 31/10/2026 | Texte officiel, formulaire ministériel de juillet 2026 | DONNÉES RÉELLES |
| Maroc, Loi 13-03 et décret 2-09-286 | 31/10/2026 | Ministère de la Transition énergétique et du Développement durable, JuriMaroc | DONNÉES RÉELLES |
| Maroc, Loi 28-00, articles 10, 24 et 25 | 31/10/2026 | Secrétariat général du gouvernement, texte consolidé au 30/07/2025 | DONNÉES RÉELLES |
| Maroc, absence de norme nationale dédiée au brûlage agricole | 31/10/2026 | Consultations multiples sans résultat, arrêtés locaux non consultés | À VÉRIFIER |
| Détections Firms (Fire Information for Resource Management System) | Relevé du 17/10/2026 | Registre de développement World Twin | DONNÉES RÉELLES datées |

## Étape suivante

Les points `À VÉRIFIER` ouverts (doublement des sanctions France, modalités d'amende vaudoises, montants des sanctions italiennes, espagnoles et misioneñas, périmètre des unités fiscales de Mendoza, arrêtés locaux marocains) sont suivis par la veille réglementaire et seront comblés au fil des sources. Les juridictions des atlas v1.0 à v1.3 hors P2 (Brésil, Inde, Chine, Turquie, Iran, Russie, etc.) restent des synthèses à cinq postes `À VÉRIFIER` et pourront recevoir la même discipline de re-vérification sourcée sur demande. Registre de travail, pas une consultation juridique : valider par un conseil local avant tout engagement.
