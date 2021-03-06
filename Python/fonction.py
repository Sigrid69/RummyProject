import random
from variable import jeu, plateau, plateau2, plateau3, plateau4, defausse

def envoyer(connexion, data):
    data=data.encode("utf8");
    connexion.send(data);
    return "";

def recevoir(connexion):
    reponse=connexion.recv(1024);
    reponse=reponse.decode("utf8");
    return reponse;
    
def demandeutilisateur(connexion, data):
    data+=("zz");
    envoyer(connexion,data);
    reponse=recevoir(connexion);
    return reponse,"";

def memoire(tab):
    tabmem=[];
    for i in range(0,len(tab)):
        tabmem.append(tab[i]);
    return tabmem;

def Switchplateau2(place, nouvelleplace):
    carte=plateau2[place];
    plateau2.remove(carte);
    if(nouvelleplace=="fin"):
        plateau2.append(carte);
    else:
        plateau2.insert(nouvelleplace,carte);

def newpioche():
    if(len(jeu)==0):
        mel(defausse);
        for i in range(0, len(defausse)):
            jeu.append(defausse[i]);
            defausse.remove(defausse[i]);
    
def Winner(player):
    if(len(player.tab)==0):
        return 1;
    else :
        return 0;

def switch(joueur,nbjoueur):
    return (joueur + 1)%nbjoueur;

def pointfindepartie(joueur):
    points=0;
    if(joueur.demarrer==0):
        points=100;
    else:
        for i in range(0, len(joueur.tab)):
            if(joueur.tab[i].couleur=="joker"):
                points+=20;
            else:
                if(joueur.tab[i].nombre>=10):
                    points+=10;
                elif(joueur.tab[i].nombre==1):
                    points+=11;
                else:
                    points+=joueur.tab[i].nombre;
    return points; 
         
def printTab(Tab, connexion, data=""):
    for i in range(0, len(Tab), 1):
        if(Tab[i].couleur !="joker"):
               data+=("\t\t");
               data+=str(i+1);
               data+=(" : ");
               data+=Tab[i].nom;
               data+=(" de ");
               data+=Tab[i].couleur;
               data+=("\n");
        else:
               data+=("\t\t");
               data+=str(i+1);
               data+=(" : joker\n");
    envoyer(connexion, data);
    return "";

def printPlateau(Tab, connexion, data=""):
    data+=("\nLe plateau:\n");
    a=len(Tab);
    if(a!=0):
        for i in range(0,len(Tab),1):
            data+=("\tCoup num??ro :");
            data+=str(i+1);
            data+=("\n");
            data=printTab(Tab[i].tab, connexion, data);
    else:
        data+=("\nAucun coup n'a ??t?? jou?? pour l'instant.\n");
    data+=("--------------------------------\n");
    envoyer(connexion, data);
    return "";
           
def Tabremove(Tab):
    a=len(Tab);
    for i in range(0,a):
        Tab.remove(Tab[-1]);
        
def mel(Tab):
	c=len(Tab);
	for i in range(0, c):
	    a=random.randint(0,c-1);
	    b=Tab[a];
	    Tab[a]=Tab[i];
	    Tab[i]=b;

def rangement(Tab):
    a=len(Tab);
    if(a>1):
        i=1;
        while(i!=a):
            numeroprecedent=(Tab[i-1].numero)%54;
            numero=(Tab[i].numero)%54;
            if(numeroprecedent>numero):
                b=Tab[i];
                Tab[i]=Tab[i-1];
                Tab[i-1]=b;
                i=0;
            i+=1;

def menuprincipal(limite, connexion):
    choix="";
    ETAT=0;
    while(ETAT==0):
        data=("\nBienvenue, vous vous appr??tez ?? jouer au Rami \n");
        data+=("Voulez-vous consultez les r??gles ou commencer ?? jouer? \n");
        data+=("Tapez r pour consulter les r??gles, l pour choisir la limite de points ?? d??passer pour poser une premi??re fois et j pour jouer: \n");
        choix, data = demandeutilisateur(connexion, data)
        if(choix=="r"):
            data+=("R??gles du Rami\n");
            data+=(">Chaque joueur poss??de 14 cartes pour commencer\n");
            data+=(">A chaque d??but de tour, le joueur pioche une carte\n");
            data+=(">Il est aussi possible de prendre la derni??re carte de la d??fausse\n");
            data+=(">Il peut ensuite jouer ou non un coup\n");
            data+=(">Coups possibles:\n");
            data+=("\t-Cartes de m??me nombre mais de couleurs diff??rentes, pas de doubles autoris??s\n");
            data+=("\t-Cartes de m??me couleur qui se suivent\n");
            data+=("\t-Il est possible de jouer un As au dessus d'un Roi ou en dessous d'un 2\n");
            
            data+=(">Ce qui n'est pas autoris??:\n");
            data+=("\t-Jouer un Roi en dessous d'un As pos?? en dessous d'un 2 ou inversement\n");
        
            data+=(">Chaque coup doit ??tre au minimum d'une longueur de 3 cartes\n");
            data+=(">Il faut d??fausser une carte ?? la fin de chaque tour si vous ne pouvez pas vous avez perdu\n");
            data+=(">Il est possible de prendre une carte pos??e sur le 'plateau' si on la joue dans le m??me tour\n");
            data+=(">De mani??re analogue, il est possible de remplacer un joker jou?? avec une carte valable si on l'utilise dans le m??me tour\n");
        
            data+=(">Chaque carte vaut un certain nombre de points:\n");
            data+=("\t-Cartes de 2 ?? 10: valent le nombre de points marqu??s sur la carte\n");
            data+=("\t-Valets, Reines, Rois: valent 10\n");
            data+=("\t-Jokers: 20 points dans la main en fin de partie, 0 si jou?? en d??but\n");
            data+=("\t-As: prend 11 dans votre main ou si il est jou?? apr??s un Roi, prend 1 si jou?? en dessous d'un 2\n");
            data+=("\t-Si on ne joue pas de la manche, on gagne 100 points quoi qu'il nous reste en main\n");
            data+=("\t-Si un joueur pose toute sa main en une fois, les points gagn??s par les perdants doublent\n");
            
            data+=(">La premi??re fois qu'un joueur joue, le total de points jou??s doit exc??der 30 ou 51, sinon, les coups ne seront pas accept??s\n");
            data+=(">Le premier joueur ?? ne plus avoir de cartes en main gagne\n");
            data+=(">Le reste des joueurs gagnent des points en fonction des cartes qu'ils ont en main et une nouvelle manche d??bute\n");
            data+=(">Cependant si le vainqueur de la manche a gagn?? en posant pour la premi??re fois les points des autres joueurs sont doubl??s\n");
            data+=(">le but du jeu est de poss??der le moins de points apr??s toutes les manches\n");
            data+=("Appuyez sur entrer pour continuer\n");
            reponse, data = demandeutilisateur(connexion, data)
        if(choix=="l"):
            data+=("La limite actuelle est de : ");
            data+=str(limite);
            data+=(". Voulez vous actualiser la limite? (oui, autre)\n");
            actualiser, data =demandeutilisateur(connexion, data)
            if(actualiser=="oui"):
                data+=("Choisissez 30 ou 51 pour la valeur de la limite ?? d??passer pour jouer une premi??re fois:\n");
                limite, data = demandeutilisateur(connexion, data)
                if(limite=="30"):
                    limite=30;
                    envoyer(connexion,("Nouvelle limite: 30"));
                elif(limite=="51"):
                    limite=51;
                    envoyer(connexion,("Nouvelle limite: 51"));
                else:
                    envoyer(connexion,("Votre limite est ??rron??e; nouvelle limite : 30\n"));
                    limite=30;
        if(choix=="j"):
            ETAT=1;
    return limite;