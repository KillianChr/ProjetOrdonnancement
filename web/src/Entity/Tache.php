<?php

namespace App\Entity;

use App\Repository\TacheRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * Une tâche d'un projet (ex. "Murs", durée 7).
 *
 * Attention : l'id en base n'est PAS le numéro de la tâche dans le projet.
 * Le numéro 1..n attendu par le Python est recalculé au moment du calcul
 * (voir App\Service\CalculOrdonnancement), ce qui évite de renuméroter la base
 * à chaque suppression.
 */
#[ORM\Entity(repositoryClass: TacheRepository::class)]
class Tache
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'taches')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Projet $projet = null;

    /** Nom de la tâche. */
    #[ORM\Column(length: 255)]
    #[Assert\NotBlank(message: 'La description est obligatoire.')]
    private ?string $description = null;

    /** Durée de la tâche (en unités de temps, entier strictement positif). */
    #[ORM\Column]
    #[Assert\NotNull]
    #[Assert\Positive(message: 'La durée doit être un entier strictement positif.')]
    private ?int $duree = null;

    /**
     * Tâches qui doivent être terminées avant de pouvoir commencer celle-ci.
     * Relation de la table Tache vers elle-même (table de liaison "tache_precedente").
     *
     * @var Collection<int, Tache>
     */
    #[ORM\ManyToMany(targetEntity: self::class)]
    #[ORM\JoinTable(name: 'tache_precedente')]
    #[ORM\JoinColumn(name: 'tache_id', onDelete: 'CASCADE')]
    #[ORM\InverseJoinColumn(name: 'precedente_id', onDelete: 'CASCADE')]
    private Collection $precedentes;

    public function __construct()
    {
        $this->precedentes = new ArrayCollection();
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

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(string $description): static
    {
        $this->description = $description;

        return $this;
    }

    public function getDuree(): ?int
    {
        return $this->duree;
    }

    public function setDuree(int $duree): static
    {
        $this->duree = $duree;

        return $this;
    }

    /**
     * @return Collection<int, Tache>
     */
    public function getPrecedentes(): Collection
    {
        return $this->precedentes;
    }

    public function ajouterPrecedente(Tache $tache): static
    {
        if (!$this->precedentes->contains($tache)) {
            $this->precedentes->add($tache);
        }

        return $this;
    }

    public function retirerPrecedente(Tache $tache): static
    {
        $this->precedentes->removeElement($tache);

        return $this;
    }

    /** Numéro de la tâche dans son projet (1, 2, 3…). */
    public function getNumero(): int
    {
        return (int) $this->projet?->getTaches()->indexOf($this) + 1;
    }

    /** Référence affichée partout sur le site (T01, T02…). */
    public function getReference(): string
    {
        return sprintf('T%02d', $this->getNumero());
    }

    /** Libellé des listes de choix (« T04 · Plomberie »). */
    public function getEtiquette(): string
    {
        return $this->getReference().' · '.$this->description;
    }

    /** Utilisé par les listes déroulantes / cases à cocher des formulaires. */
    public function __toString(): string
    {
        return (string) $this->description;
    }
}
