<?php

namespace App\Form;

use App\Entity\Projet;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Formulaire de création / modification d'un projet (nom + description).
 * Les tâches et contraintes sont gérées sur leurs propres formulaires.
 */
class ProjetType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('nom', TextType::class, [
                'label' => 'Nom du projet',
                'attr' => ['placeholder' => 'Ex. Construction maison'],
            ])
            ->add('description', TextareaType::class, [
                'label' => 'Description',
                'required' => false,
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(['data_class' => Projet::class]);
    }
}
