<?php

namespace App\Controller;

use App\Entity\Projet;
use App\Form\ProjetType;
use App\Repository\ProjetRepository;
use App\Service\CalculOrdonnancement;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

/**
 * Pages des projets : liste, création, détail (tâches + résultats), modification, suppression.
 */
class ProjetController extends AbstractController
{
    /** Page d'accueil : liste de tous les projets. */
    #[Route('/', name: 'projet_liste', methods: ['GET'])]
    public function liste(ProjetRepository $projets): Response
    {
        return $this->render('projet/liste.html.twig', [
            'projets' => $projets->findBy([], ['dateCreation' => 'DESC']),
        ]);
    }

    /** Création d'un nouveau projet (vide). */
    #[Route('/projet/nouveau', name: 'projet_nouveau', methods: ['GET', 'POST'])]
    public function nouveau(Request $request, EntityManagerInterface $em): Response
    {
        $projet = new Projet();
        $form = $this->createForm(ProjetType::class, $projet);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->persist($projet);
            $em->flush();
            $this->addFlash('succes', 'Projet créé. Ajoutez maintenant ses tâches.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('projet/formulaire.html.twig', [
            'form' => $form,
            'titre' => 'Nouveau projet',
        ]);
    }

    /**
     * Détail d'un projet : tâches, contraintes et résultats du calcul.
     * Le calcul est relancé à chaque affichage, donc toute modification est prise en compte.
     */
    #[Route('/projet/{id}', name: 'projet_detail', methods: ['GET'], requirements: ['id' => '\d+'])]
    public function detail(Projet $projet, CalculOrdonnancement $calcul): Response
    {
        return $this->render('projet/detail.html.twig', [
            'projet' => $projet,
            'resultat' => $calcul->calculer($projet),
        ]);
    }

    /** Modification du nom / de la description. */
    #[Route('/projet/{id}/modifier', name: 'projet_modifier', methods: ['GET', 'POST'])]
    public function modifier(Projet $projet, Request $request, EntityManagerInterface $em): Response
    {
        $form = $this->createForm(ProjetType::class, $projet);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->flush();
            $this->addFlash('succes', 'Projet modifié.');

            return $this->redirectToRoute('projet_detail', ['id' => $projet->getId()]);
        }

        return $this->render('projet/formulaire.html.twig', [
            'form' => $form,
            'titre' => 'Modifier le projet',
        ]);
    }

    /** Suppression (en POST, protégée par un jeton CSRF). Les tâches et contraintes partent avec. */
    #[Route('/projet/{id}/supprimer', name: 'projet_supprimer', methods: ['POST'])]
    public function supprimer(Projet $projet, Request $request, EntityManagerInterface $em): Response
    {
        if ($this->isCsrfTokenValid('supprimer_projet_'.$projet->getId(), $request->getPayload()->getString('_token'))) {
            $em->remove($projet);
            $em->flush();
            $this->addFlash('succes', 'Projet supprimé.');
        }

        return $this->redirectToRoute('projet_liste');
    }

    // TODO : dupliquer un projet
    // TODO : importer un projet depuis un CSV (format de Graphe/P1.csv)
    // TODO : exporter un projet en CSV
}
