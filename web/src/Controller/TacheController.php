<?php

namespace App\Controller;

use App\Entity\Projet;
use App\Entity\Tache;
use App\Form\TacheType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

/**
 * Ajout, modification et suppression des tâches d'un projet.
 * Après chaque action, on revient sur la page du projet, où le calcul est relancé.
 */
class TacheController extends AbstractController
{
    /** Ajout d'une tâche au projet. */
    #[Route('/projet/{id}/tache/nouvelle', name: 'tache_nouvelle', methods: ['GET', 'POST'])]
    public function nouvelle(Projet $projet, Request $request, EntityManagerInterface $em): Response
    {
        $tache = new Tache();
        $projet->ajouterTache($tache);

        $form = $this->createForm(TacheType::class, $tache, ['projet' => $projet]);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->persist($tache);
            $em->flush();
            $this->addFlash('succes', 'Tâche ajoutée.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('tache/formulaire.html.twig', [
            'form' => $form,
            'projet' => $projet,
            'titre' => 'Nouvelle tâche',
        ]);
    }

    /** Modification d'une tâche (nom, durée, précédentes). */
    #[Route('/tache/{id}/modifier', name: 'tache_modifier', methods: ['GET', 'POST'])]
    public function modifier(Tache $tache, Request $request, EntityManagerInterface $em): Response
    {
        $projet = $tache->getProjet();
        $form = $this->createForm(TacheType::class, $tache, ['projet' => $projet]);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->flush();
            $this->addFlash('succes', 'Tâche modifiée.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('tache/formulaire.html.twig', [
            'form' => $form,
            'projet' => $projet,
            'titre' => 'Modifier la tâche',
        ]);
    }

    /**
     * Suppression d'une tâche.
     * Elle est aussi retirée des précédentes des autres tâches (table de liaison en cascade),
     * et les contraintes qui la mentionnent sont supprimées.
     */
    #[Route('/tache/{id}/supprimer', name: 'tache_supprimer', methods: ['POST'])]
    public function supprimer(Tache $tache, Request $request, EntityManagerInterface $em): Response
    {
        $projet = $tache->getProjet();

        if ($this->isCsrfTokenValid('supprimer_tache_'.$tache->getId(), $request->getPayload()->getString('_token'))) {
            // On la retire d'abord des précédentes des autres tâches, côté objets PHP
            foreach ($projet->getTaches() as $autre) {
                $autre->retirerPrecedente($tache);
            }
            $projet->retirerTache($tache);
            $em->flush();
            $this->addFlash('succes', 'Tâche supprimée.');
        }

        return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
    }
}
