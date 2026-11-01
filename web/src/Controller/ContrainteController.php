<?php

namespace App\Controller;

use App\Entity\Contrainte;
use App\Entity\Projet;
use App\Form\ContrainteType;
use App\Service\CalculOrdonnancement;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

/**
 * Ajout, modification et suppression des contraintes supplémentaires d'un projet (partie P2).
 */
class ContrainteController extends AbstractController
{
    #[Route('/projet/{id}/contrainte/nouvelle', name: 'contrainte_nouvelle', methods: ['GET', 'POST'])]
    public function nouvelle(Projet $projet, Request $request, EntityManagerInterface $em, CalculOrdonnancement $calcul): Response
    {
        // Valeurs de départ : le panneau « Lecture » montre tout de suite un exemple
        $taches = $projet->getTaches();
        $contrainte = (new Contrainte())
            ->setType(Contrainte::PRECEDENCE)
            ->setTacheA($taches->first() ?: null)
            ->setTacheB($taches->get(1));
        $projet->ajouterContrainte($contrainte);

        $form = $this->createForm(ContrainteType::class, $contrainte, ['projet' => $projet]);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->persist($contrainte);
            $em->flush();
            $this->addFlash('succes', 'Contrainte ajoutée.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('contrainte/formulaire.html.twig', [
            'form' => $form,
            'projet' => $projet,
            'titre' => 'Nouvelle contrainte',
            'resultat' => $calcul->calculer($projet),
        ]);
    }

    #[Route('/contrainte/{id}/modifier', name: 'contrainte_modifier', methods: ['GET', 'POST'])]
    public function modifier(Contrainte $contrainte, Request $request, EntityManagerInterface $em, CalculOrdonnancement $calcul): Response
    {
        $projet = $contrainte->getProjet();
        $form = $this->createForm(ContrainteType::class, $contrainte, ['projet' => $projet]);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->flush();
            $this->addFlash('succes', 'Contrainte modifiée.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('contrainte/formulaire.html.twig', [
            'form' => $form,
            'projet' => $projet,
            'titre' => 'Modifier la contrainte',
            'resultat' => $calcul->calculer($projet),
        ]);
    }

    #[Route('/contrainte/{id}/supprimer', name: 'contrainte_supprimer', methods: ['POST'])]
    public function supprimer(Contrainte $contrainte, Request $request, EntityManagerInterface $em): Response
    {
        $projet = $contrainte->getProjet();

        if ($this->isCsrfTokenValid('supprimer_contrainte_'.$contrainte->getId(), $request->getPayload()->getString('_token'))) {
            $projet->retirerContrainte($contrainte);
            $em->flush();
            $this->addFlash('succes', 'Contrainte supprimée.');
        }

        return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
    }
}
