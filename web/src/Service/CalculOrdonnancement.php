<?php

namespace App\Service;

use App\Entity\Contrainte;
use App\Entity\Projet;
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Exception\ProcessTimedOutException;
use Symfony\Component\Process\Process;

/**
 * Pont entre Symfony et les calculs Python (pas d'API HTTP).
 *
 * Fonctionnement :
 *  1. on transforme le Projet en JSON ;
 *  2. on lance `python calcul.py` en lui envoyant ce JSON sur l'entrée standard ;
 *  3. le script répond un JSON sur la sortie standard, qu'on décode et renvoie.
 *
 * Format envoyé à Python :
 *  {
 *    "nom": "Construction maison",
 *    "taches": [ {"id": 1, "description": "Murs", "duree": 7, "precedentes": []}, ... ],
 *    "contraintes": [ {"type": "date_fixe", "tacheA": 2, "tacheB": null, "valeur": 3}, ... ]
 *  }
 *
 * Format renvoyé par calcul.py (même structure que le resultat.json de index.py) :
 *  {
 *    "realisable": true,
 *    "duree_projet": 22,
 *    "taches": {
 *      "1": {"description": "Murs", "duree": 7, "precedentes": [],
 *            "date_au_plus_tot": 0, "date_au_plus_tard": 0, "marge": 0, "critique": true},
 *      ...
 *    },
 *    "erreur": null
 *  }
 *
 * Ce service le traduit en un format court utilisé par les templates :
 *  ['realisable', 'duree', 'taches' => [idEnBase => ['tot', 'tard', 'marge', 'critique']], 'erreur']
 */
class CalculOrdonnancement
{
    /** Temps maximum laissé au script Python, en secondes. */
    private const DELAI_MAX = 30;

    public function __construct(
        // Exécutable Python, configuré dans .env (PYTHON_BIN)
        #[Autowire('%env(PYTHON_BIN)%')]
        private readonly string $python,
        // Dossier du projet Symfony (web/) : le script est un niveau au-dessus
        #[Autowire('%kernel.project_dir%')]
        private readonly string $dossierProjet,
    ) {
    }

    /**
     * Lance le calcul pour un projet.
     *
     * Ne lève jamais d'exception : en cas de problème, le tableau renvoyé
     * contient "realisable" => false et un message dans "erreur".
     * Les résultats par tâche sont indexés par l'id EN BASE de la tâche,
     * pour être faciles à utiliser dans les templates.
     *
     * @return array{realisable: bool, duree: ?int, taches: array<int, array<string, mixed>>, erreur: ?string}
     */
    public function calculer(Projet $projet): array
    {
        if ($projet->getTaches()->isEmpty()) {
            return $this->echec('Le projet ne contient aucune tâche.');
        }

        $script = $this->dossierProjet.'/../calcul.py';
        if (!is_file($script)) {
            return $this->echec('Le script de calcul Python (calcul.py) est introuvable.');
        }

        // Correspondance numéro Python (1..n) <-> id en base
        [$donnees, $idsBase] = $this->versJson($projet);

        $process = new Process([$this->python, $script]);
        $process->setInput(json_encode($donnees, JSON_THROW_ON_ERROR | JSON_INVALID_UTF8_SUBSTITUTE));
        $process->setTimeout(self::DELAI_MAX);
        // Force Python à lire et écrire en UTF-8 (sinon les accents posent problème sous Windows)
        $process->setEnv(['PYTHONIOENCODING' => 'utf-8', 'PYTHONUTF8' => '1']);

        try {
            $process->mustRun();
        } catch (ProcessTimedOutException) {
            return $this->echec('Le calcul a pris trop de temps.');
        } catch (ProcessFailedException) {
            // Le script a planté : on affiche ce qu'il a écrit sur la sortie d'erreur
            return $this->echec('Erreur du script Python : '.trim($process->getErrorOutput()));
        }

        $resultat = json_decode($process->getOutput(), true);
        if (!is_array($resultat)) {
            return $this->echec('Réponse illisible du script Python.');
        }

        // "taches" est un objet indexé par numéro Python ("1", "2"…) :
        // on ré-indexe par id en base et on raccourcit les noms des champs
        $parTache = [];
        foreach ($resultat['taches'] ?? [] as $numero => $ligne) {
            $idBase = $idsBase[(int) $numero] ?? null;
            if (null !== $idBase) {
                $parTache[$idBase] = [
                    'tot' => $ligne['date_au_plus_tot'] ?? null,
                    'tard' => $ligne['date_au_plus_tard'] ?? null,
                    'marge' => $ligne['marge'] ?? null,
                    'critique' => (bool) ($ligne['critique'] ?? false),
                ];
            }
        }

        return [
            'realisable' => (bool) ($resultat['realisable'] ?? false),
            'duree' => $resultat['duree_projet'] ?? null,
            'taches' => $parTache,
            'erreur' => $resultat['erreur'] ?? null,
        ];
    }

    /**
     * Construit le JSON envoyé à Python.
     * Les tâches sont renumérotées 1..n (le cours et le code Python l'exigent).
     *
     * @return array{0: array<string, mixed>, 1: array<int, int>} [données, numéro Python => id en base]
     */
    private function versJson(Projet $projet): array
    {
        $numeros = [];   // id en base => numéro Python
        $idsBase = [];   // numéro Python => id en base
        $numero = 1;
        foreach ($projet->getTaches() as $tache) {
            $numeros[$tache->getId()] = $numero;
            $idsBase[$numero] = $tache->getId();
            ++$numero;
        }

        $taches = [];
        foreach ($projet->getTaches() as $tache) {
            $precedentes = [];
            foreach ($tache->getPrecedentes() as $precedente) {
                // On ignore une précédente qui appartiendrait à un autre projet
                if (isset($numeros[$precedente->getId()])) {
                    $precedentes[] = $numeros[$precedente->getId()];
                }
            }
            sort($precedentes);

            $taches[] = [
                'id' => $numeros[$tache->getId()],
                'description' => $tache->getDescription(),
                'duree' => $tache->getDuree(),
                'precedentes' => $precedentes,
            ];
        }

        $contraintes = array_map(fn (Contrainte $c) => [
            'type' => $c->getType(),
            'tacheA' => $numeros[$c->getTacheA()?->getId()] ?? null,
            'tacheB' => $c->getTacheB() ? ($numeros[$c->getTacheB()->getId()] ?? null) : null,
            'valeur' => $c->getValeur(),
        ], $projet->getContraintes()->toArray());

        return [
            ['nom' => $projet->getNom(), 'taches' => $taches, 'contraintes' => array_values($contraintes)],
            $idsBase,
        ];
    }

    /** Résultat standard en cas d'échec. */
    private function echec(string $message): array
    {
        return ['realisable' => false, 'duree' => null, 'taches' => [], 'erreur' => $message];
    }
}
