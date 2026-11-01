import { Controller } from '@hotwired/stimulus';

/*
 * Compteur : boutons − et + autour d'un champ numérique.
 * Déclenche l'événement « input » pour que les autres contrôleurs voient le changement.
 */
export default class extends Controller {
    get champ() {
        return this.element.querySelector('input');
    }

    plus() {
        this.modifier(1);
    }

    moins() {
        this.modifier(-1);
    }

    modifier(ecart) {
        const minimum = Number(this.champ.min || 0);
        this.champ.value = Math.max(minimum, Number(this.champ.value || 0) + ecart);
        this.champ.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
