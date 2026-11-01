<?php

namespace App\Form;

use App\Entity\Projet;
use App\Entity\Tache;
use App\Repository\TacheRepository;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Formulaire d'une tâche.
 *
 * Les précédentes sont proposées sous forme de cases à cocher, limitées
 * aux autres tâches du même projet : impossible de saisir une tâche
 * inexistante, ni de rendre une tâche précédente d'elle-même.
 */
class TacheType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        /** @var Projet $projet */
        $projet = $options['projet'];
        /** @var Tache|null $tache */
        $tache = $builder->getData();

        $builder
            ->add('description', TextType::class, [
                'label' => 'Nom de la tâche',
                'attr' => ['placeholder' => 'Ex. Murs'],
            ])
            ->add('duree', IntegerType::class, [
                'label' => 'Durée',
                'attr' => ['min' => 1],
            ])
            ->add('precedentes', EntityType::class, [
                'label' => 'Tâches à terminer avant',
                'class' => Tache::class,
                'choice_label' => 'etiquette',
                'multiple' => true,
                'expanded' => true,   // cases à cocher
                'required' => false,
                // by_reference reste à true (défaut) : Symfony modifie directement la collection
                // renvoyée par getPrecedentes(), sans chercher de méthodes addXxx()/removeXxx()
                'query_builder' => function (TacheRepository $repo) use ($projet, $tache) {
                    $qb = $repo->createQueryBuilder('t')
                        ->where('t.projet = :projet')
                        ->setParameter('projet', $projet)
                        ->orderBy('t.id', 'ASC');

                    // En modification : on retire la tâche elle-même de la liste
                    if ($tache?->getId()) {
                        $qb->andWhere('t.id != :id')->setParameter('id', $tache->getId());
                    }

                    return $qb;
                },
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(['data_class' => Tache::class]);
        // Le projet est obligatoire pour filtrer la liste des précédentes
        $resolver->setRequired('projet');
        $resolver->setAllowedTypes('projet', Projet::class);
    }
}
