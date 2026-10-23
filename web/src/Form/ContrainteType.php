<?php

namespace App\Form;

use App\Entity\Contrainte;
use App\Entity\Projet;
use App\Entity\Tache;
use App\Repository\TacheRepository;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Formulaire d'une contrainte supplémentaire (partie P2).
 *
 * Champs utilisés selon le type (vérifiés par Contrainte::verifierChamps()) :
 *  - types à date (fixe, min, max) : tâche A + valeur X (la date)
 *  - types à deux tâches           : tâche A + tâche B (+ valeur X = délai, 0 si vide)
 *
 * TODO : masquer/afficher les champs selon le type choisi (petit contrôleur Stimulus).
 */
class ContrainteType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        /** @var Projet $projet */
        $projet = $options['projet'];

        // Seules les tâches du projet sont proposées
        $tachesDuProjet = fn (TacheRepository $repo) => $repo->createQueryBuilder('t')
            ->where('t.projet = :projet')
            ->setParameter('projet', $projet)
            ->orderBy('t.id', 'ASC');

        $builder
            ->add('type', ChoiceType::class, [
                'label' => 'Type de contrainte',
                'choices' => Contrainte::TYPES,
            ])
            ->add('tacheA', EntityType::class, [
                'label' => 'Tâche A',
                'class' => Tache::class,
                'query_builder' => $tachesDuProjet,
            ])
            ->add('tacheB', EntityType::class, [
                'label' => 'Tâche B',
                'class' => Tache::class,
                'query_builder' => $tachesDuProjet,
                'required' => false,
                'placeholder' => '— aucune —',
            ])
            ->add('valeur', IntegerType::class, [
                'label' => 'Valeur X (date ou délai)',
                'required' => false,
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(['data_class' => Contrainte::class]);
        $resolver->setRequired('projet');
        $resolver->setAllowedTypes('projet', Projet::class);
    }
}
