<?php

namespace App\Entity;

use App\Repository\ProjetRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * Un projet d'ordonnancement (ex. "Construction maison" = P1).
 * Il regroupe une liste de tâches et, éventuellement, des contraintes supplémentaires.
 */
#[ORM\Entity(repositoryClass: ProjetRepository::class)]
class Projet
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    /** Nom affiché du projet. */
    #[ORM\Column(length: 255)]
    #[Assert\NotBlank(message: 'Le nom du projet est obligatoire.')]
    private ?string $nom = null;

    /** Description libre, facultative. */
    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $description = null;

    #[ORM\Column]
    private ?\DateTimeImmutable $dateCreation = null;

    /**
     * Tâches du projet.
     * orphanRemoval : une tâche retirée du projet est supprimée de la base.
     *
     * @var Collection<int, Tache>
     */
    #[ORM\OneToMany(targetEntity: Tache::class, mappedBy: 'projet', cascade: ['persist', 'remove'], orphanRemoval: true)]
    #[ORM\OrderBy(['id' => 'ASC'])]
    private Collection $taches;

    /**
     * Contraintes supplémentaires (date fixe, chevauchement…), utilisées à partir du projet P2.
     *
     * @var Collection<int, Contrainte>
     */
    #[ORM\OneToMany(targetEntity: Contrainte::class, mappedBy: 'projet', cascade: ['persist', 'remove'], orphanRemoval: true)]
    private Collection $contraintes;

    public function __construct()
    {
        $this->taches = new ArrayCollection();
        $this->contraintes = new ArrayCollection();
        $this->dateCreation = new \DateTimeImmutable();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getNom(): ?string
    {
        return $this->nom;
    }

    public function setNom(string $nom): static
    {
        $this->nom = $nom;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): static
    {
        $this->description = $description;

        return $this;
    }

    public function getDateCreation(): ?\DateTimeImmutable
    {
        return $this->dateCreation;
    }

    /**
     * @return Collection<int, Tache>
     */
    public function getTaches(): Collection
    {
        return $this->taches;
    }

    public function ajouterTache(Tache $tache): static
    {
        if (!$this->taches->contains($tache)) {
            $this->taches->add($tache);
            $tache->setProjet($this);
        }

        return $this;
    }

    public function retirerTache(Tache $tache): static
    {
        $this->taches->removeElement($tache);

        return $this;
    }

    /**
     * @return Collection<int, Contrainte>
     */
    public function getContraintes(): Collection
    {
        return $this->contraintes;
    }

    public function ajouterContrainte(Contrainte $contrainte): static
    {
        if (!$this->contraintes->contains($contrainte)) {
            $this->contraintes->add($contrainte);
            $contrainte->setProjet($this);
        }

        return $this;
    }

    public function retirerContrainte(Contrainte $contrainte): static
    {
        $this->contraintes->removeElement($contrainte);

        return $this;
    }
}
