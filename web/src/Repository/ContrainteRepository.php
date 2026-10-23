<?php

namespace App\Repository;

use App\Entity\Contrainte;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * Accès en base aux entités Contrainte.
 * Les requêtes personnalisées (recherches, tris…) seront ajoutées ici.
 *
 * @extends ServiceEntityRepository<Contrainte>
 */
class ContrainteRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Contrainte::class);
    }
}
