import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import numpy as np
from Deselection import Deselection

deselection = Deselection()

class Affichage:
    def __init__(self):
        pass
    '''
    Affiche les détails des documents sélectionnés dans la zone de texte.

    Paramètres : 
        - corpus : L'objet corpus contenant les documents.
        - zone_texte : Le widget de zone de texte dans lequel afficher les détails.
        - numDoc : Le numéro du document à afficher. Attribut de la classe Document.
        - vars_afficher : Un dictionnaire de variables associées aux boutons "Afficher" pour chaque document.

    Algorithme :
        Récupère le document associé au numDoc dans l'objet corpus.
        Active la modification de la zone de texte.
        Efface le contenu précédent de la zone de texte.
        Récupère les documents sélectionnés en fonction des variables associées aux boutons "Afficher".
        Affiche les détails des documents sélectionnés : le titre, l'auteur, la date, l'URL et le contenu du document.
    '''
    def afficher_details_selectionnes(self, corpus, zone_texte, numDoc, vars_afficher):
        document = next(doc for doc in corpus.id2doc.values() if doc.numDoc == numDoc)

        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END)

        # Récupére les documents sélectionnés
        documents_selectionnes = [doc for doc, var in zip(corpus.id2doc.values(), vars_afficher.values()) if var.get()]

        # Affiche les détails des documents sélectionnés
        for document in documents_selectionnes:
            zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
            zone_texte.insert(tk.END, f"Auteur du document : {document.auteur}\n")
            zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
            zone_texte.insert(tk.END, f"Lien du document : {document.url}\n")
            zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
            zone_texte.insert(tk.END, "=" * 150 + "\n")

        # Désactive la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)
        
    '''Affichage du Corpus dans son intégralité

    Paramètres : 
        - corpus : l'objet corpus contenant les documents.
        - zone_texte : le widget de zone de texte dans lequel afficher les détails.
        - checkbutton : checkbutton associé au type de source.
        - vars_afficher : un dictionnaire de variables associées aux boutons "Afficher" pour chaque document.
        - vars_comparer: Dictionnaire de variables associées aux boutons “Comparer” pour chaque document.
        
    Algorithme :
        Efface le contenu précédent du widget de texte et désélectionne le check boutons du type de source s'il est activé.
        Utilise une boucle pour parcourir tous les documents dans le corpus.
        Créer des boutons "Afficher" et "Comparer" pour chaque document, associant les fonctions afficher_details_selectionnes et comparer_documents.
        Affiche pour chaque document son titre et ses auteurs.
        Ajoute les boutons créés à la zone de texte.
        Ajoute des lignes de séparation pour une meilleure lisibilité.
        Met à jour les dictionnaires vars_afficher et vars_comparer avec les nouvelles variables associées aux boutons pour chaque document.
        Si on clique sur "Afficher", cela va faire appel à afficher_details_selectionnes.
        Si on clique sur "Comparer" de deux documents, cela va faire appel à comparer_documents.
        Désactive la modification de la zone de texte.
'''

    def afficher_corpus(self, corpus, zone_texte, checkbutton, vars_afficher, vars_comparer):
        # Effacer le contenu précédent du widget de texte
        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END) 
        
        #Deselectionne le check du type si active
        checkbutton.deselect()

        #Initialisation
        boutons_par_document = {}

        # Afficher l'ensemble du corpus    
        for document in corpus.id2doc.values():
            zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
            zone_texte.insert(tk.END, f"Auteurs du document : {document.auteur}\n")

            var_afficher = tk.IntVar()
            bouton_check = tk.Checkbutton(
                zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
                command=lambda doc=document, var=var_afficher: self.afficher_details_selectionnes(corpus, zone_texte, doc.numDoc, vars_afficher))
            bouton_check.document = document
            zone_texte.window_create(tk.END, window=bouton_check)
            zone_texte.insert(tk.END, "\n")

            var_comparer = tk.IntVar()
            bouton_comparer_doc = tk.Checkbutton(
                    zone_texte,
                    text="Comparer", variable=var_comparer, font=("Helvetica", 10),
                    command=lambda doc=document: self.comparer_documents(corpus, zone_texte, vars_afficher, vars_comparer, doc.numDoc))

            bouton_comparer_doc.document = document
            zone_texte.window_create(tk.END, window=bouton_comparer_doc)
            zone_texte.insert(tk.END, "\n")

            boutons_par_document[document] = (var_afficher, var_comparer)

        #Mise à jour
        vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
        vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
        vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
        vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})


        # Activer la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)

    '''
    Visualise la distribution TFxIDF pour un mot donné dans le corpus.
    
    Paramètres : 
        - mot : Mot pour lequel visualiser la distribution TFxIDF.
        - vocabulaire : Liste triée des mots du vocabulaire du corpus.
        - mat_TFxIDF : Matrice TFxIDF du corpus.  

    Algorithme :
        Trouve l'indice du mot dans le vocabulaire.
        Initialise une figure pour les graphiques.
        Créer un histogramme pour le mot en utilisant la distribution TFxIDF  du corpus.
        Affiche le titre, les labels des axes, et ajuste la mise en page.
        Affiche le graphique.
    '''
    def visualiser_distribution(self, mot, vocabulaire, mat_TFxIDF):
        # Trouve l'indice du mot dans le vocabulaire
        mot_index = vocabulaire.index(mot)

        # Initialise la figure pour les graphiques
        plt.figure(figsize=(12, 6))

        tfidf_corpus = mat_TFxIDF[:, mot_index].tolist()

        # Crée un histogramme pour le mot
        plt.hist(np.array(tfidf_corpus), bins=30, edgecolor='black')
        plt.title(f'Distribution TFxIDF pour le mot "{mot}"')
        plt.xlabel('Valeurs TFxIDF')
        plt.ylabel('Fréquence')

        plt.tight_layout()
        plt.show()
   
    '''
    Comparer deux documents sélectionnés dans le corpus en utilisant la similarité cosinus et affiche les détails de la comparaison.
   
    Paramètres : 
        - corpus: L'objet corpus contenant les documents.
        - zone_texte: La zone de texte où afficher les résultats.
        - vars_afficher : un dictionnaire de variables associées aux boutons "Afficher" pour chaque document.
        - vars_comparer: Dictionnaire de variables associées aux boutons “Comparer” pour chaque document.
        - numDoc: L'identifiant unique du document sur lequel l'utilisateur a cliqué pour lancer la comparaison.
    
    Algorithme :
        Récupère les documents sélectionnés en utilisant les identifiants uniques.
        Initialise les variables pour les deux documents à comparer.
        Utilise la méthode creer_vocabulaire de la classe Corpus pour obtenir le vocabulaire du corpus.
        Transforme les documents en vecteurs sur le vocabulaire précédemment construit à l'aide de la similarité cosinus
        Calcule la similarité entre les deux documents.
        Récupère les indices des mots communs et les mots communs eux-mêmes.
        Calcule le pourcentage de présence des mots communs dans chaque document.
        Affiche la similarité et les informations détaillées pour chaque document.
        Réinitialise tous les boutons de comparaison dans les variables associées.
        Affiche un message d'erreur si le nombre de documents sélectionnés n'est pas exactement deux.
        Désactive la modification de la zone de texte.           
    '''
    def comparer_documents(self, corpus, zone_texte, vars_afficher, vars_comparer, numDoc):
        # Récupére les documents sélectionnés en utilisant l'identifiant unique
        numeros_selectionnes = [doc for doc, var in vars_comparer.items() if var.get()]
        
        # Permet d'éditer la zone de texte
        zone_texte.config(state=tk.NORMAL)  

        # Débogage
        print("Documents sélectionnés pour comparaison :", numeros_selectionnes)
        print("longueur :" ,len(numeros_selectionnes))
        print("longeur check ", len(vars_comparer))

        if len(numeros_selectionnes) == 2:
            num_doc1 = numeros_selectionnes[0]
            num_doc2 = numeros_selectionnes[1]

            # Récupére les documents correspondants aux numéros
            document1 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc1)
            document2 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc2)

            # Utilise la méthode creer_vocabulaire de la classe Corpus pour obtenir le vocabulaire
            _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

            # Transforme les documents en vecteurs sur le vocabulaire précédemment construit
            vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)
            document1_vecteur = vectorizer.transform([document1.texte])
            document2_vecteur = vectorizer.transform([document2.texte])

            # Calcule la similarité entre les deux documents
            similarite = cosine_similarity(document1_vecteur, document2_vecteur).flatten()[0]

            # Récupére les indices des mots communs
            mots_communs_indices = list(set(document1_vecteur.indices) & set(document2_vecteur.indices))

            # Récupére les mots communs
            mots_communs = [vocabulaire_corpus[indice] for indice in mots_communs_indices]

            # Calcule le nombre total de mots dans chaque document
            total_mots_document1 = len(document1.texte.split())
            total_mots_document2 = len(document2.texte.split())

            # Affichage
            zone_texte.config(state=tk.NORMAL)
            zone_texte.delete(1.0, tk.END)
            zone_texte.insert(tk.END, f"Comparaison entre {document1.titre} et {document2.titre}\n\n")
            zone_texte.insert(tk.END, f"Similarité : {similarite}\n\n")

            zone_texte.insert(tk.END, f"Informations pour le premier document : \n\n")
            zone_texte.insert(tk.END, f"Titre : {document1.titre}\n")
            zone_texte.insert(tk.END, f"Auteurs : {document1.auteur}\n")
            zone_texte.insert(tk.END, f"Date du document : {document1.date}\n")
            zone_texte.insert(tk.END, f"URL : {document1.url}\n")
            zone_texte.insert(tk.END, f"Contenu :\n{document1.texte}\n\n")

            zone_texte.insert(tk.END, f"Informations pour le second document :\n\n")
            zone_texte.insert(tk.END, f"Titre : {document2.titre}\n")
            zone_texte.insert(tk.END, f"Auteurs : {document2.auteur}\n")
            zone_texte.insert(tk.END, f"Date du document : {document2.date}\n")
            zone_texte.insert(tk.END, f"URL : {document2.url}\n")
            zone_texte.insert(tk.END, f"Contenu :\n{document2.texte}\n\n")
            
            if not mots_communs:
                zone_texte.insert(tk.END, "Aucun mot commun trouvé.\n")
            else:
                # Affiche les mots communs dans la zone de texte
                zone_texte.insert(tk.END, "Pourcentage de présence des mots communs :\n\n")
                for mot in mots_communs:
                    pour_document1 = document1.texte.lower().count(mot.lower())/total_mots_document1*100
                    pour_document2 = document2.texte.lower().count(mot.lower())/total_mots_document2*100
                    zone_texte.insert(tk.END, f"- Mot : {mot}\n")
                    zone_texte.insert(tk.END, f"{document1.titre} : {pour_document1:.2f} %\n")
                    zone_texte.insert(tk.END, f"{document2.titre} : {pour_document2:.2f} %\n\n")
            
            # Réinitialise la comparaison
            deselection.clear_tous_les_boutons(vars_afficher, vars_comparer)
            vars_comparer = {}
            
            zone_texte.config(state=tk.DISABLED)

        elif len(numeros_selectionnes) < 2:
            messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
        else:
            messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")
        
        # Désactive la possibilité d'éditer la zone de texte
        zone_texte.config(state=tk.DISABLED)