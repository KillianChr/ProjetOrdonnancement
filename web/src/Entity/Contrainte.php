<?php

namespace App\Entity;

use App\Repository\ContrainteRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\Context\ExecutionContextInterface;

/**
 * Contrainte supplémentaire sur un projet, en plus des précédences (cours p.20 à 36).
 * Utilisable sur n'importe quel projet. Les types portent le nom des fonctions de contraintes.py
 * (debut_max_apres_fin est traduit par calcul.py).
 *
 *  - DATE_FIXE            : A commence exactement à la date "valeur"              (ex. P2 : S2 = 3)
 *  - DATE_MIN             : A ne commence pas avant la date "valeur"
 *  - DATE_MAX             : A commence au plus tard à la date "valeur"
 *  - APRES_DEBUT          : B commence au moins "valeur" après le début de A      (ex. P2 : S5 >= S3)
 *  - PRECEDENCE           : B commence après la fin de A
 *  - DEBUT_MAX_APRES_FIN  : B commence au plus "valeur" après la fin de A         (ex. cours p.20)
 *  - CHEVAUCHEMENT        : A et B se chevauchent d'au moins 1 unité de temps     (ex. P2 : 3 et 4)
 */
#[ORM\Entity(repositoryClass: ContrainteRepository::class)]
class Contrainte
{
    public const DATE_FIXE = 'date_fixe';
    public const DATE_MIN = 'date_min';
    public const DATE_MAX = 'date_max';
    public const APRES_DEBUT = 'apres_debut';
    public const PRECEDENCE = 'precedence';
    public const DEBUT_MAX_APRES_FIN = 'debut_max_apres_fin';
    public const CHEVAUCHEMENT = 'chevauchement';

    /** Libellés affichés dans les formulaires. */
    public const TYPES = [
        'A commence exactement à la date X' => self::DATE_FIXE,
        'A ne commence pas avant la date X' => self::DATE_MIN,
        'A commence au plus tard à la date X' => self::DATE_MAX,
        'B commence au moins X après le début de A' => self::APRES_DEBUT,
        'B commence après la fin de A' => self::PRECEDENCE,
        'B commence au plus X après la fin de A' => self::DEBUT_MAX_APRES_FIN,
        'A et B se chevauchent (au moins 1 unité)' => self::CHEVAUCHEMENT,
    ];

    /** Types qui portent sur deux tâches (A et B). */
    public const TYPES_A_DEUX_TACHES = [
        self::APRES_DEBUT, self::PRECEDENCE, self::DEBUT_MAX_APRES_FIN, self::CHEVAUCHEMENT,
    ];

    /** Types qui portent sur une date : la valeur X est obligatoire. */
    public const TYPES_A_DATE = [self::DATE_FIXE, self::DATE_MIN, self::DATE_MAX];

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'contraintes')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Projet $projet = null;

    /** Une des constantes de type ci-dessus (voir TYPES). */
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

    /** Valeur X : une date (types à date) ou un délai (types à deux tâches, 0 si vide). */
    #[ORM\Column(nullable: true)]
    private ?int $valeur = null;

    /**
     * Vérifie que les bons champs sont remplis selon le type choisi
     * (appelé automatiquement par le validateur de Symfony).
     */
    #[Assert\Callback]
    public function verifierChamps(ExecutionContextInterface $context): void
    {
        if (in_array($this->type, self::TYPES_A_DEUX_TACHES, true)) {
            if (null === $this->tacheB) {
                $context->buildViolation('Ce type de contrainte porte sur deux tâches : choisissez la tâche B.')
                    ->atPath('tacheB')->addViolation();
            } elseif ($this->tacheB === $this->tacheA) {
                $context->buildViolation('Les tâches A et B doivent être différentes.')
                    ->atPath('tacheB')->addViolation();
            }
        }

        if (in_array($this->type, self::TYPES_A_DATE, true) && null === $this->valeur) {
            $context->buildViolation('Indiquez la date X.')->atPath('valeur')->addViolation();
        }

        if (null !== $this->valeur && $this->valeur < 0) {
            $context->buildViolation('La valeur X doit être positive ou nulle.')->atPath('valeur')->addViolation();
        }
    }

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
