import { Controller } from '@hotwired/stimulus';

/*
 * Formulaire de contrainte :
 *  - n'affiche que les champs utiles au type choisi ;
 *  - remplit le panneau « Lecture » : formule, phrase, schéma, arcs et effet sur le planning.
 * Aucun calcul d'ordonnancement ici : la vérification ne fait que comparer la contrainte
 * aux dates au plus tôt déjà calculées par le Python.
 * Sans JavaScript, tous les champs restent visibles et le panneau reste caché.
 */
const SIGMA = 'σ';
const CREME = '#F3F2EE';
const SIGNAL = '#C026D3';

// Doit rester synchronisé avec Contrainte::TYPES_A_DEUX_TACHES (PHP)
const DEUX_TACHES = ['apres_debut', 'precedence', 'debut_max_apres_fin', 'chevauchement'];
const SANS_VALEUR = ['precedence', 'chevauchement'];
const TYPES_A_DATE = ['date_fixe', 'date_min', 'date_max'];

const indice = (n) => String(n).split('').map((c) => '₀₁₂₃₄₅₆₇₈₉'[Number(c)]).join('');
const barre = (lettre, tache, debut, couleur, extra = {}) => ({ lettre, nom: tache.nom, debut, duree: tache.duree, couleur, ...extra });

export default class extends Controller {
    static targets = ['type', 'tacheA', 'tacheB', 'valeur', 'groupeB', 'groupeValeur',
        'lecture', 'code', 'formule', 'phrase', 'schema', 'arcs', 'effet'];

    static values = { taches: Object, duree: Number };

    connect() {
        this.lectureTarget.hidden = false;
        this.mettreAJour();
    }

    tache(cible) {
        return this.tachesValue[`t${cible.value}`] ?? null;
    }

    mettreAJour() {
        const type = this.typeTargets.find((t) => t.checked)?.value;
        if (!type) return;

        // Champs utiles au type
        const aDeuxTaches = DEUX_TACHES.includes(type);
        const sansValeur = SANS_VALEUR.includes(type);
        this.groupeBTarget.hidden = !aDeuxTaches;
        this.groupeValeurTarget.hidden = sansValeur;
        // Un champ désactivé n'est pas envoyé : le serveur enregistre « vide » pour les champs inutiles
        this.tacheBTarget.disabled = !aDeuxTaches;
        this.valeurTarget.disabled = sansValeur;
        const libelle = this.groupeValeurTarget.querySelector('label');
        if (libelle) libelle.textContent = TYPES_A_DATE.includes(type) ? 'Date X' : 'Délai X';

        const a = this.tache(this.tacheATarget);
        const b = this.tache(this.tacheBTarget);
        const x = sansValeur ? 0 : Number(this.valeurTarget.value || 0);

        this.codeTarget.textContent = type;

        if (!a || (aDeuxTaches && !b)) {
            this.formuleTarget.textContent = '';
            this.phraseTarget.textContent = 'Choisissez les tâches concernées.';
            this.schemaTarget.replaceChildren();
            this.arcsTarget.replaceChildren();
            this.effetTarget.textContent = '';
            return;
        }

        const lecture = this.lire(type, a, b, x);
        this.formuleTarget.textContent = lecture.formule;
        this.formuleTarget.classList.toggle('lecture-formule-longue', lecture.formule.length > 22);
        this.phraseTarget.textContent = lecture.phrase;
        this.dessinerSchema(lecture);
        this.arcsTarget.replaceChildren(...lecture.arcs.map((arc) => {
            const element = document.createElement('span');
            element.textContent = arc;
            return element;
        }));
        this.afficherEffet(lecture.respectee, aDeuxTaches && this.tacheATarget.value === this.tacheBTarget.value);
    }

    // Formule, phrase, arcs, schéma et respect actuel de la contrainte, pour chaque type
    lire(type, a, b, x) {
        const A = a.numero;
        const B = b?.numero;
        const sA = `S${indice(A)}`;
        const sB = B ? `S${indice(B)}` : '';
        const connu = (...v) => v.every((d) => d !== null && d !== undefined);

        switch (type) {
            case 'date_fixe':
                return {
                    formule: `${sA} = ${x}`, phrase: `${a.nom} commence exactement à la date ${x}.`,
                    arcs: [`(${SIGMA} → ${A}, ${x})`, `(${A} → ${SIGMA}, ${-x})`],
                    respectee: connu(a.tot) ? a.tot === x : null,
                    barres: [barre('A', a, x, CREME)], cote: { debut: 0, fin: x, texte: `X = ${x}` }, reperes: [x], etendue: x + a.duree + 2,
                };
            case 'date_min':
                return {
                    formule: `${sA} ≥ ${x}`, phrase: `${a.nom} ne commence pas avant la date ${x}.`,
                    arcs: [`(${SIGMA} → ${A}, ${x})`],
                    respectee: connu(a.tot) ? a.tot >= x : null,
                    barres: [barre('A', a, x, CREME, { zone: [0, x] })], cote: { debut: 0, fin: x, texte: `X = ${x}` }, reperes: [x], etendue: x + a.duree + 2,
                };
            case 'date_max':
                return {
                    formule: `${sA} ≤ ${x}`, phrase: `${a.nom} commence au plus tard à la date ${x}.`,
                    arcs: [`(${A} → ${SIGMA}, ${-x})`],
                    respectee: connu(a.tot) ? a.tot <= x : null,
                    barres: [barre('A', a, x, CREME, { fenetre: [0, x + a.duree] })], cote: { debut: 0, fin: x, texte: `≤ ${x}` }, reperes: [x], etendue: x + a.duree + 2,
                };
            case 'apres_debut':
                return {
                    formule: `${sB} ≥ ${sA} + ${x}`, phrase: `${b.nom} commence au moins ${x} après le début de ${a.nom}.`,
                    arcs: [`(${A} → ${B}, ${x})`],
                    respectee: connu(a.tot, b.tot) ? b.tot >= a.tot + x : null,
                    barres: [barre('A', a, 0, CREME), barre('B', b, x, SIGNAL)], cote: { debut: 0, fin: x, texte: `X = ${x}` }, reperes: [0, x], etendue: Math.max(a.duree, x + b.duree) + 2,
                };
            case 'precedence':
                return {
                    formule: `${sB} ≥ ${sA} + ${a.duree}`, phrase: `${b.nom} commence après la fin de ${a.nom}.`,
                    arcs: [`(${A} → ${B}, ${a.duree})`],
                    respectee: connu(a.tot, b.tot) ? b.tot >= a.tot + a.duree : null,
                    barres: [barre('A', a, 0, CREME), barre('B', b, a.duree, SIGNAL)], cote: null, reperes: [a.duree], etendue: a.duree + b.duree + 2,
                };
            case 'debut_max_apres_fin':
                return {
                    formule: `${sB} ≤ ${sA} + ${a.duree} + ${x}`, phrase: `${b.nom} commence au plus ${x} après la fin de ${a.nom}.`,
                    arcs: [`(${B} → ${A}, ${-(a.duree + x)})`],
                    respectee: connu(a.tot, b.tot) ? b.tot <= a.tot + a.duree + x : null,
                    barres: [barre('A', a, 0, CREME), barre('B', b, a.duree + x, SIGNAL, { fenetre: [0, a.duree + x + b.duree] })],
                    cote: { debut: a.duree, fin: a.duree + x, texte: `≤ ${x}` }, reperes: [a.duree, a.duree + x], etendue: a.duree + x + b.duree + 2,
                };
            default:
                return {
                    formule: `${sA} + ${a.duree} ≥ ${sB} + 1  et  ${sB} + ${b.duree} ≥ ${sA} + 1`,
                    phrase: `${a.nom} et ${b.nom} se déroulent en même temps pendant au moins une unité.`,
                    arcs: [`(${B} → ${A}, ${1 - a.duree})`, `(${A} → ${B}, ${1 - b.duree})`],
                    respectee: connu(a.tot, b.tot) ? a.tot + a.duree >= b.tot + 1 && b.tot + b.duree >= a.tot + 1 : null,
                    barres: [barre('A', a, 0, CREME), barre('B', b, a.duree - 1, SIGNAL, { chevauchement: [a.duree - 1, 1] })],
                    cote: { debut: a.duree - 1, fin: a.duree, texte: '1 u en commun' }, reperes: [a.duree - 1, a.duree], etendue: a.duree - 1 + b.duree + 2,
                };
        }
    }

    // Schéma à l'échelle : une ligne par tâche, plus les repères et la cote
    dessinerSchema({ barres, cote, reperes, etendue }) {
        const pourcent = (v) => `${(v / etendue) * 100}%`;
        const bloc = (classe, style = {}, texte = null) => {
            const element = document.createElement('span');
            element.className = classe;
            Object.assign(element.style, style);
            if (texte !== null) element.textContent = texte;
            return element;
        };

        const lignes = barres.map((b) => {
            const ligne = bloc('schema-ligne');
            const nom = bloc('schema-nom');
            nom.append(bloc(`schema-lettre schema-lettre-${b.lettre}`, {}, b.lettre), b.nom);
            const piste = bloc('schema-piste');
            if (b.zone) piste.append(bloc('schema-zone', { left: pourcent(b.zone[0]), width: pourcent(b.zone[1] - b.zone[0]) }));
            if (b.fenetre) piste.append(bloc('schema-fenetre', { left: pourcent(b.fenetre[0]), width: pourcent(b.fenetre[1] - b.fenetre[0]) }));
            piste.append(bloc('schema-barre', { left: pourcent(b.debut), width: pourcent(b.duree), background: b.couleur }));
            if (b.chevauchement) piste.append(bloc('schema-chevauchement', { left: pourcent(b.chevauchement[0]), width: pourcent(b.chevauchement[1]) }));
            ligne.append(nom, piste);
            return ligne;
        });

        const bas = bloc('schema-ligne');
        const mesure = bloc('schema-mesure');
        reperes.forEach((r) => mesure.append(bloc('schema-repere', { left: pourcent(r) })));
        if (cote) {
            mesure.append(
                bloc('schema-cote', { left: pourcent(cote.debut), width: pourcent(cote.fin - cote.debut) }),
                bloc('schema-cote-butee', { left: pourcent(cote.debut) }),
                bloc('schema-cote-butee', { left: pourcent(cote.fin) }),
                bloc('schema-cote-texte', { left: pourcent((cote.debut + cote.fin) / 2) }, cote.texte),
            );
        }
        bas.append(bloc('schema-nom'), mesure);

        this.schemaTarget.replaceChildren(...lignes, bas);
    }

    afficherEffet(respectee, memeTache) {
        let message;
        if (memeTache) {
            message = 'Choisissez deux tâches différentes.';
        } else if (respectee === null) {
            message = 'Le planning actuel n’est pas calculé : l’effet sera visible après l’enregistrement.';
        } else if (respectee) {
            message = `Déjà respectée par le planning actuel : aucune date ne change, la durée reste de ${this.dureeValue}.`;
        } else {
            message = 'Non respectée par le planning actuel : les dates seront recalculées à l’enregistrement, et la durée du projet peut augmenter.';
        }
        this.effetTarget.textContent = message;
        this.effetTarget.classList.toggle('lecture-effet-alerte', memeTache || respectee === false);
    }
}
