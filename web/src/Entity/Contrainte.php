<?php

namespace App\Entity;

use App\Repository\ContrainteRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * Contrainte supplémentaire sur un projet (partie P2 du cours).
 *
 * Remplace les contraintes aujourd'hui écrites en dur dans contraintes.py :
 *  - DATE_FIXE          : la tâche A commence exactement à la date "valeur"          (ex. S2 = 3)
 *  - DEBUT_APRES_DEBUT  : la tâche B commence après le début de A, + "valeur"         (ex. S5 >= S3 + 0)
 *  - CHEVAUCHEMENT      : les tâches A et B se chevauchent d'au moins 1 unité de temps
 */
#[ORM\Entity(repositoryClass: ContrainteRepository::class)]
class Contrainte
{
    public const DATE_FIXE = 'date_fixe';
    public const DEBUT_APRES_DEBUT = 'debut_apres_debut';
    public const CHEVAUCHEMENT = 'chevauchement';

    /** Libellés affichés dans les formulaires. */
    public const TYPES = [
        'Date de début fixe' => self::DATE_FIXE,
        'Commence après le début d\'une autre tâche' => self::DEBUT_APRES_DEBUT,
        'Chevauchement entre deux tâches' => self::CHEVAUCHEMENT,
    ];

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'contraintes')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Projet $projet = null;

    /** Une des constantes DATE_FIXE, DEBUT_APRES_DEBUT ou CHEVAUCHEMENT. */
    #[ORM\Column(length: 30)]
    #[Assert\Choice(choices: self::TYPES, message: 'Type de contrainte inconnu.')]
    private ?string $type = null;

    /** Première tâche concernée (toujours renseignée). */
    #[ORM\ManyToOne]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Tache $tacheA = null;

    /** Seconde tâche (vide pour DATE_FIXE). */
    #[ORM\ManyToOne]
    #[ORM\JoinColumn(nullable: true, onDelete: 'CASCADE')]
    private ?Tache $tacheB = null;

    /** Valeur numérique : la date pour DATE_FIXE, le délai pour DEBUT_APRES_DEBUT. */
    #[ORM\Column(nullable: true)]
    private ?int $valeur = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getProjet(): ?Projet
    {
        return $this->projet;
    }

    public function setProjet(?Projet $projet): static
    {
        $this->projet = $projet;

        return $this;
    }

    public function getType(): ?string
    {
        return $this->type;
    }

    public function setType(string $type): static
    {
        $this->type = $type;

        return $this;
    }

    /** Libellé lisible du type, pour l'affichage. */
    public function getLibelleType(): string
    {
        return array_search($this->type, self::TYPES, true) ?: (string) $this->type;
    }

    public function getTacheA(): ?Tache
    {
        return $this->tacheA;
    }

    public function setTacheA(?Tache $tacheA): static
    {
        $this->tacheA = $tacheA;

        return $this;
    }

    public function getTacheB(): ?Tache
    {
        return $this->tacheB;
    }

    public function setTacheB(?Tache $tacheB): static
    {
        $this->tacheB = $tacheB;

        return $this;
    }

    public function getValeur(): ?int
    {
        return $this->valeur;
    }

    public function setValeur(?int $valeur): static
    {
        $this->valeur = $valeur;

        return $this;
    }
}
