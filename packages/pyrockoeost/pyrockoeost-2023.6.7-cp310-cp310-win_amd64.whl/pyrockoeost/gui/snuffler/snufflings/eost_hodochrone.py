import numpy as num
import os
from PyQt5.QtWidgets import QMessageBox
from os import listdir
from os.path import isfile, join
import time
import sys
import re
from collections import OrderedDict

from pyrockoeost.gui.qt_compat import qw

from pyrockoeost import moment_tensor, model
from pyrockoeost.snuffling import Snuffling, Param, Choice, EventMarker, MyFrame, Text
from pyrockoeost import gf
from pyrockoeost.marker import PhaseMarker

# Couleur des phases ajoutées par le calculateur d'hodochrones
# 0: rouge - 1: vert - 2: bleu - 3: jaune - 4: violet - 5: marron
NORMAL_KIND = 0
FIXED_PHASE_KIND = 2
HODOCHRONE_PHASE_KIND = 3

PLUGIN_NAME = "EOST - Hodochrones"

class EOST_hodochrone(Snuffling):

    def setup(self):
        '''Customization of the snuffling.'''

        self.set_name(PLUGIN_NAME)

        self.add_parameter(
            Text('Hodochrones', 'hodochrone_results', '''
            <html><p><strong>Station : </strong> - \t <strong>Type : </strong> - </p>
            <p><strong>Date Séisme :</strong> - </p>
            <p><strong>Distance :</strong> - &deg; / - km</p></html>'''))

        self.add_parameter(
            Choice('Phase 1 :', 'phase_first', 'Pointez 2 phases minimum',
                   ['Pointez 2 phases minimum']))

        self.add_parameter(
            Choice('Phase 2 :', 'phase_second', 'Pointez 2 phases minimum',
                   ['Pointez 2 phases minimum']))

        self.add_parameter(
            Choice('Profondeur :', 'depth', '15',
                   ['15',
                    '50',
                    '100',
                    '200',
                    '400']))

        self.add_trigger('Ouvrir des fichiers', self.waveform_browser)
        self.add_trigger('Dessiner les Hodochrones', self.hodochrone_calculator)
        self.add_trigger('Supprimer les Hodochrones', self.hodochrone_remover)
        self.add_trigger('Sauvegarder les phases', self.save_phases_as_text)

        self.useless_buttons_already_removed = False
        self.tinc = None
        self.seism_date = None
        self.seism_distance = None
        self.file_type = " Aucun Fichier "
        self.station = " Aucun Fichier "

        self.marker_choices = []

        self.hodochrone_memory = {}

    def call(self):
        '''
        Routine d'initialisation et de mise à jour du module.
        Différents éléments graphiques se placent en écoute d'autres éléments de l'application: ajout/modification de
        marqueurs, changement de profil de profondeur, ...

        Cette routine est exécutée une fois l'interface graphique lancée.
        '''

        if not self.useless_buttons_already_removed:
            self.useless_buttons_already_removed = True
            self.remove_useless_buttons()

        # A chaque modification des phases de la vue principale (ajout, edition, suppression, ...),
        # on met à jour les choix de phases disponibles pour le calcul d'hodochrones
        viewer = self.get_viewer()
        viewer.begin_markers_add.connect(self.handle_changed_markers)
        viewer.end_markers_add.connect(self.handle_changed_markers)
        viewer.begin_markers_remove.connect(self.handle_changed_markers)
        viewer.end_markers_remove.connect(self.handle_changed_markers)
        viewer.marker_selection_changed.connect(self.handle_changed_markers)

        # A chaque changement de valeur des listes déroulantes, on surligne les phases sélectionnées
        control_first = self._param_controls.get('phase_first')
        control_first.choosen.connect(self.handle_changed_choice)
        control_second = self._param_controls.get('phase_second')
        control_second.choosen.connect(self.handle_changed_choice)

        # A chaque changement de valeur de la liste déroulante de profondeur, on charge les hodochrones en mémoire
        control_second = self._param_controls.get('depth')
        control_second.choosen.connect(self.load_hodochrone_files)

        # Initialisation
        self.load_hodochrone_files()
        self.update_seism_text()

    def remove_useless_buttons(self):
        """
        Permet de supprimer les boutons intégrés par défaut par SNUFFLER (Help, Clear, Run) qui ne servent à rien pour ce
        module.
        """
        button = self._panel_parent.get_panel_parent_widget().findChildren(qw.QPushButton)
        button += self._panel_parent.get_panel_parent_widget().findChildren(qw.QCheckBox)

        for b in button:
            if (
                    PLUGIN_NAME in b.parent().objectName() and
                    ("Help" in b.text() or
                     "Clear" in b.text() or
                     "Run" in b.text() or
                     "Auto-Run" in b.text()
                    )
                ):

                b.setVisible(False)

    def load_hodochrone_files(self):
        """
        Chargement des fichiers d'hodochrones depuis le PATH indiqué dans le fichier de configuration:
         ~/.pyrockoeost/snuffler.pf
        :return:
        """
        depth = self.get_parameter_value('depth')
        hodochrone_folder_path = self.get_viewer().get_path_hodochrones() +str(depth) +"KM/"

        self.hodochrone_memory["P-Pdif"] = {}
        self.hodochrone_memory["PP"] = {}
        self.hodochrone_memory["S-SKKS"] = {}
        self.hodochrone_memory["SS"] = {}
        self.hodochrone_memory["PKP"] = {}
        self.hodochrone_memory["SKS"] = {}
        self.hodochrone_memory["SP"] = {}
        self.hodochrone_memory["RAYL"] = {}
        self.hodochrone_memory["LOVE"] = {}

        # self.hodochrone_memory["P"] = {}
        # self.hodochrone_memory["S"] = {}
        # self.hodochrone_memory["R"] = {}
        # self.hodochrone_memory["Q"] = {}

        for key in self.hodochrone_memory:
            with open(str(hodochrone_folder_path) +str(depth) + "km" +str(key) +str(".dat")) as f:
                lines = f.readlines()

                dict_phase = OrderedDict()
                for l in lines:
                    dict_phase[float(l[0:5])] = float(l[6:14])

                self.hodochrone_memory[key] = dict_phase

    def hodochrone_calculator(self):
        """
        Process complet du calcul des hodochrones:
            - suppression des anciennes phases tracées
            - récupération des valeurs indiquées par l'utilisateur dans les menus déroulants
            - vérification de cohérence
            - lancement de la recherche d'une hodochrone existante
            - dessin des hodochrones
        :return:
        """
        markers = self.get_markers()
        phase_first = self.get_parameter_value("phase_first")
        phase_second = self.get_parameter_value("phase_second")

        phases_in_right_order = ["P-Pdif", "PKP", "PP", "SKS", "S-SKKS", "SP", "SS", "LOVE", "RAYL"]
        # phases_in_right_order = ["P", "S", "R", "Q"]

        if len(self.marker_choices) > 1:
            self.hodochrone_remover() # Eviter d'avoir plusieurs hodochrones superposé

            for m in markers:
                m_time = m.get_tmin()
                m_time_str = str(time.strftime("%d/%m/%Y - %H:%M:%S", time.gmtime(m_time)))
                m_label = m.get_label()

                # Suppression des anciennes phases d'hodochrones
                if m.kind == HODOCHRONE_PHASE_KIND:
                    self.get_viewer().remove_marker(m)

                elif str(m_label) in str(phase_first) and str(m_time_str) in str(phase_first):
                    marker_phase_first = m
                    marker_phase_first_time = m_time
                    marker_phase_first_label = m_label

                elif str(m_label) in str(phase_second) and str(m_time_str) in str(phase_second):
                    marker_phase_second = m
                    marker_phase_second_time = m_time
                    marker_phase_second_label = m_label

            # Si les deux phases de références pointes sur la même phase, ca ne pourra pas marcher !
            if str(phase_second) == str(phase_first):
                self.show_message("ERREUR ", "Tu as sélectionné deux fois la même phase !")

            # Test de cohérence de l'ordre des phases pointées: une P ne peut pas être avant une RAYL
            elif (
                (phases_in_right_order.index(marker_phase_first_label) < phases_in_right_order.index(marker_phase_second_label) and
                (marker_phase_first_time > marker_phase_second_time))
                or
                (phases_in_right_order.index(marker_phase_first_label) > phases_in_right_order.index(marker_phase_second_label) and
                (marker_phase_first_time < marker_phase_second_time))
            ):
                self.show_message("Situation impossible, revoir le pointé ", "ordre des phases incohérent")

            else:
                # Recherche d'une distance épicentral à partir des hodochrones
                self.seism_distance, self.seism_date = self.search_for_epicentral_details(marker_phase_first, marker_phase_second)

                # Si on a bien trouvé une distance épicentrale, on traces les autres phases qui en découlent
                # On calcule la date d'origine du séisme
                # On autorise l'utilisateur à sauvegarder ce pointé
                # On met à jour le texte affiché
                if self.seism_distance is not None:
                    self.draw_hodochrone_phases(marker_phase_first, marker_phase_second, self.seism_distance)
                    self.get_open_file_type()
                    self.update_seism_text()
        else : self.show_message("ERREUR ", "Tu n'as pas défini au moins deux phases !")

    def get_open_file_type(self):
        """
        A chaque calcul d'hodocrhone et sauvegarde de pointé, on vérifie le type du fichier utilisé pour l'afficher
        sur l'interface ou l'écrire dans le fichier de pointé.
        Les types de fichiers pris en charge sont: LH, BH et miniseed.
        :return:
        """
        open_files = self.get_viewer().get_pile().open_files
        open_files = open_files[sorted(open_files.keys())[-1]]

        for o in open_files:
            open_file_path = o.abspath
            break

        pattern_lh = re.compile(".*LHE.*$") # Vérifier le motif (Contient LHE ?)
        pattern_bh = re.compile(".*BHE.*$")
        pattern_seed = re.compile(".*seed$")

        if pattern_lh.match(str(open_file_path)):
            self.file_type = "LH (1Hz)"
        elif pattern_bh.match(str(open_file_path)):
            self.file_type = "BH (10Hz)"
        elif pattern_seed.match(str(open_file_path)):
            self.file_type = "Miniseed"

    def search_for_epicentral_details(self, marker_phase_first, marker_phase_second):
        '''
        Dans les fichiers d'hodochrones, on boucle pour trouver une distance épicentrale qui correspondrait au delta T
        pointé par l'utilisateur entre 2 phases.

        :param marker_phase_first:
        :param marker_phase_second:
        :return: (epicentral_distance, epicentral_date) si une distance épicentrale a été trouvée dans les hodochrones
         ou (None, None) si rien n'a été trouvé.
        '''
        delta_t = abs(marker_phase_first.get_tmin() - marker_phase_second.get_tmin())
        delta_t_found_in_hodochrone = False

        for epicentral_distance in num.arange(0,180,0.1):
            try:
                t1 = self.hodochrone_memory[marker_phase_first.get_label()][epicentral_distance]
                t2 = self.hodochrone_memory[marker_phase_second.get_label()][epicentral_distance]
            except KeyError:
                continue

            # On accepte une approximation, voir avec Armelle si 5 secondes sont ok
            if abs(round(abs(t2 - t1),2) - round(delta_t,2))  <= 5:
                delta_t_found_in_hodochrone = True
                epicentral_date = marker_phase_first.get_tmin() - t1
                break

        if delta_t_found_in_hodochrone:
            return epicentral_distance,epicentral_date
        else:
            self.show_message("Situation impossible, revoir le pointé",
                              "le temps entre les phases ne correspond pas à une situation possibles")
            return  None, None

    def draw_hodochrone_phases(self, marker_phase_first, marker_phase_second, epicentral_distance):
        """
        Dessin des phases calculées par hodochrone en JAUNE: elles ne seront pas prise en compte lors de la sauvegarde
        du pointé, n'apparaitront pas dans les menus déroulants et pourront être facilement supprimées.

        :param marker_phase_first:
        :param marker_phase_second:
        :param epicentral_distance:
        :return:
        """
        for key in self.hodochrone_memory:
            if key in marker_phase_first.get_label() or key in marker_phase_second.get_label():
                continue
            try:
                t_new_phase = self.hodochrone_memory[key][epicentral_distance]
            except KeyError:
                continue

            t_ref_phase = self.hodochrone_memory[marker_phase_first.get_label()][epicentral_distance]
            delta_t_new_phase = t_ref_phase - t_new_phase
            absolute_t_new_phase = marker_phase_first.get_tmin() - delta_t_new_phase

            new_phase = PhaseMarker(nslc_ids=marker_phase_first.get_nslc_ids(), tmin=absolute_t_new_phase,
                                    tmax= absolute_t_new_phase, kind=HODOCHRONE_PHASE_KIND, phasename=key)

            self.get_viewer().add_marker(new_phase)

    def hodochrone_remover(self):
        """
        Fonction de suppression des phases ajoutées par le calcul des hodochrones: elles sont tracées en JAUNE
        :return:
        """
        # Test reset Distance / Date lors de la suppression de l'hodochrone
        self.seism_date = None
        self.seism_distance = None
        self.update_seism_text()


        markers = self.get_markers()
        markers_toRemove = []

        for m in markers:
            if m.kind == HODOCHRONE_PHASE_KIND:
                markers_toRemove += [m]

        for m in markers_toRemove:
            self.get_viewer().remove_marker(m)

    def save_phases_as_text(self):
        """
        Fonction de sauvegarde des détails d'un pointé. Tous les pointés d'une même journée sont inscrits dans un unique
        fichier: c'est la date du séisme qui est prise en compte.

        :return:
        """
        path_save_depu = self.get_viewer().get_path_save_depu()
        # station = self.get_viewer().get_station_name() if not None else " - "
        date = str(time.strftime("%Y/%m/%d   %H:%M:%S", time.gmtime(self.seism_date))) if not None else " - "
        distance_deg = self.seism_distance if not None else " - "
        distance_km = self.convert_degree_to_km(self.seism_distance) if (self.seism_distance is not None) else " - "
        markers = self.get_markers()

        try:
            self.get_open_file_type()
        except Exception :
            self.show_message("ERREUR ", "Aucun fichier ouvert / pas encore affiché")
            return None


        if len(markers) < 1:
            self.show_message("ERREUR ", "Aucune phase défini")
            return None
        elif len(markers) == 1 or self.seism_date == None:
            # On utilise la date du seul marqueur à disposition
            seism_date_for_filename = str(time.strftime("%Y-%m-%d", time.gmtime(markers[0].get_tmin())))
        else:
            # On utilise la date d'origine du séisme pour le nom du fichier
            seism_date_for_filename = str(time.strftime("%Y-%m-%d", time.gmtime(self.seism_date)))

        filename = str(self.station) + ".L-" + seism_date_for_filename + "-depu"
        file_path = str(path_save_depu) + str(filename)

        # Vérifier si le fichier existe déjà
        if os.path.isfile(file_path):
            # Le fichier existe déjà, demander à l'utilisateur ce qu'il souhaite faire
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle('Confirmation')
            msg_box.setText('Le fichier existe déjà. Que voulez-vous faire ?\n(Remplacer ou ajouter à la suite)')
            add_button = msg_box.addButton('Ajouter', QMessageBox.YesRole)
            replace_button = msg_box.addButton('Remplacer', QMessageBox.NoRole)
            cancel_button = msg_box.addButton('Annuler', QMessageBox.RejectRole)
            msg_box.setDefaultButton(cancel_button)

            msg_box.exec()

            if msg_box.clickedButton() == replace_button:
                # Supprimer le fichier existant
                os.remove(file_path)
            elif msg_box.clickedButton() == cancel_button:
                # Annuler l'opération
                return None

        # On écrit dans le fichier
        # On change la couleur des phases pointées en VIOLET
        # On nettoie les vieilles phases
        with open(file_path, "a") as f:
            for m in markers:
                if m.kind != HODOCHRONE_PHASE_KIND:
                    m_time = m.get_tmin()
                    m_time_str = str(time.strftime("%Y-%m-%d   %H:%M:%S.00", time.gmtime(m_time)))
                    m_label = m.get_label()
                    f.write(str(m_label) + "\t\t" + str(m_time_str) +"\n")

            f.write("\nStation " + str(self.station) + " - Type "+ str(self.file_type) +"\n")
            f.write("Distance epicentrale: " +str(distance_deg) + " deg / "+ str(distance_km) +" km\n")

            if self.seism_date != None:
                seism_date_for_record = str(time.strftime("%Y/%m/%d   %H:%M:%S.00", time.gmtime(self.seism_date)))
            else:
                seism_date_for_record = str(time.strftime("%Y-%m-%d   %H:%M:%S.00", time.gmtime(markers[0].get_tmin())))

            f.write("Date du seisme: " +str(seism_date_for_record)+"\n")
            f.write("\n################################\n\n")

            self.hodochrone_remover()
            self.handle_changed_markers()

        # Et on affiche une petite fenêtre, pour remplir l'utilisateur de bonheur !!!
        self.show_message("Pointé sauvegardé", file_path)


    def update_seism_text(self):
        """
        Fonction de mise à jour du texte affiché sur l'interface pour l'utilisateur.
        :return:
        """

        # station = self.get_viewer().get_station_name() if not None else " - "
        # print(self.seism_date)
        if self.seism_date != None:
            date = str(time.strftime("%d/%m/%Y   %H:%M:%S", time.gmtime(self.seism_date)))
        else : date = " Hodochrone en attente "

        if self.seism_distance != None :
            distance_deg = self.seism_distance
            distance_km = self.convert_degree_to_km(self.seism_distance)
        else : 
            distance_deg = " Hodochrone en attente "
            distance_km = ""

        label = self._panel_parent.get_panel_parent_widget().findChildren(qw.QLabel)
        for l in label:
            if (
                    ("Station" in l.text() and "Date" in l.text() and "Distance" in l.text())
            ):
                if self.seism_distance != None :
                    l.setText('''
                    <html><p><strong>Station : </strong>''' + str(self.station) + '''\t<strong>Type : </strong> '''
                            + str(self.file_type) +'''</p>
                    <p><strong>Date Séisme :</strong> ''' + str(date) +''' </p>
                    <p><strong>Distance :</strong> ''' +str(distance_deg)+'''&deg; / '''+ \
                    str(distance_km) +''' km</p></html>''')
                else :
                    l.setText('''
                    <html><p><strong>Station : </strong>''' + str(self.station) + '''\t<strong>Type : </strong> '''
                            + str(self.file_type) +'''</p>
                    <p><strong>Date Séisme :</strong> ''' + str(date) +''' </p>
                    <p><strong>Distance :</strong> ''' +str(distance_deg)+'''</p></html>''')

    def handle_changed_markers(self):
        """
        A chaque changement de marqueur (création, déplacement, suppression, ...) cette fonction est appellée
        Elle met à jour les listes déroulantes pour le choix des phases à utiliser pour un calcul d'hodochrones.

        Dans le cas où il n'existe que moins de 2 phases, on affiche un texte spécifique.
        :return:
        """
        markers = self.get_markers()
        self.marker_choices = []
        # print(len(markers))
        # print(marker_choices)
        # print(len(marker_choices))

        for m in markers:
            if type(m) is PhaseMarker \
                    and m.kind != HODOCHRONE_PHASE_KIND:
                marker_time = m.get_tmin()
                marker_time_str = str(time.strftime("%d/%m/%Y - %H:%M:%S", time.gmtime(marker_time)))
                self.marker_choices += [str(m.get_label()) +' - ' +str(marker_time_str)]
        # print(self.marker_choices)

        # Le calcul d'hodochrones n'est possible qu'à partir du moment où il y a 2 phases pointés
        if len(self.marker_choices) >= 2:
            # tri de la liste en fonction des heures de chaque phase
            self.marker_choices.sort(key = lambda x: time.strptime(" ".join(x.rsplit(' - ')[1:]), "%d/%m/%Y %H:%M:%S"))

            try:
                self.set_parameter_choices("phase_first", self.marker_choices)
            except IndexError:
                self.set_parameter("phase_first", self.marker_choices[0])

            try:
                self.set_parameter_choices("phase_second", self.marker_choices)
            except IndexError:
                self.set_parameter("phase_second", self.marker_choices[0])

        else:
            zeroPhaseTab = ['Pointez 2 phases minimum']

            self.set_parameter_choices("phase_first", zeroPhaseTab)
            self.set_parameter("phase_first",zeroPhaseTab[0])

            self.set_parameter_choices("phase_second", zeroPhaseTab)
            self.set_parameter("phase_second",zeroPhaseTab[0])

            for m in markers:
                m.set_kind(NORMAL_KIND)

        # Dans le cas où il n'y a que 2 phases de pointées, on les considère directement comme celles qui permettront
        # le calcul des hodochrones
        if len(self.marker_choices) == 2:
            self.set_parameter("phase_first", self.marker_choices[0])
            self.set_parameter("phase_second", self.marker_choices[1])
            self.handle_changed_choice()

    def handle_changed_choice(self):
        """
        A chaque changement de choix de l'utilisateur dans les listes déroulantes, cette fonction est exécutée.

        Elle gère les couleurs des marqueurs: bleu quand ils sont choisis comme références d'hodochrones, rouge autrement
        :return:
        """
        markers = self.get_markers()
        phase_first = self.get_parameter_value("phase_first")
        phase_second = self.get_parameter_value("phase_second")

        if len(markers) >= 2:
            for m in markers:
                m_time = m.get_tmin()
                m_time_str = str(time.strftime("%d/%m/%Y - %H:%M:%S", time.gmtime(m_time)))
                m_label = m.get_label()

                if m.kind is FIXED_PHASE_KIND:
                    m.set_kind(NORMAL_KIND)

                if str(m_label) in str(phase_first) and str(m_time_str) in str(phase_first):
                    m.set_kind(FIXED_PHASE_KIND)

                if str(m_label) in str(phase_second) and str(m_time_str) in str(phase_second):
                    m.set_kind(FIXED_PHASE_KIND)

    def convert_degree_to_km(self,deg):
        """
        Conversion degrée vers des km
        :param deg:
        :return:
        """
        earth_radius=6378.1370
        km = deg*(2*num.pi*earth_radius)/360
        return round(km)

    def waveform_browser(self):
        """
        fonction appellée par le bouton "open files", elle ouvre une nouvelle fenêtre de navigation de fichiers pour
        permettre à l'utilisateur les fichiers à charger.
        :return:
        """
        path_donnees_quant = self.get_viewer().get_path_donnees_quant()
        fb = FileBrowser(path_donnees_quant)
        waveform_files = fb.waveform_files
        if waveform_files:
            self.file_type = waveform_files["type"]
            self.station = waveform_files["station"]

            # On met à jour le Texte
            self.update_seism_text()

            for f in waveform_files["files"]:
                self.get_viewer().load(f)

class FileBrowser(qw.QWidget):

    def __init__(self, rootFolder):
        super().__init__()
        self.title = 'Open a seismo file'
        self.left = 250
        self.top = 250
        self.width = 640
        self.height = 480
        self.rootFolder = rootFolder

        self.waveform_files = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        waveform_files = self.waveforme_loader()
        self.waveform_files = waveform_files

    def waveforme_loader(self):
        """
        Gestion de la fenêtre de navigation pour l'utilisateur.
        :return:
        """
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        fileNames = qw.QFileDialog.getOpenFileNames(self,"Waveform loader", self.rootFolder,"LHE files (*LHE*);;"+ "BHE files (*BHE*);; Miniseed Files (*seed);; All Files (*)", options=options)

        if fileNames and len(fileNames[0]) > 0:
            waveform_files = {}

            # Station :
            pattern_AIS = re.compile(".*AIS.*$")
            pattern_PAF = re.compile(".*PAF.*$")
            pattern_ECH = re.compile(".*ECH.*$")
            pattern_CRZF = re.compile(".*CRZF.*$")
            pattern_DRV = re.compile(".*DRV.*$")
            pattern_CCD = re.compile(".*CCD.*$")

            # Type :
            pattern_lh = re.compile(".*LHE.*$")
            pattern_bh = re.compile(".*BHE.*$")
            pattern_seed = re.compile(".*seed$") # Pas encore utiliser
            
            # Dans certaines versions de QT, qw.QFileDialog.getOpenFileNames renvoie un tuple de tableaux ...
            try:
                pattern_lh.match(fileNames[0])
            except TypeError:
                fileNames = fileNames[0]

            # Station :
            if pattern_AIS.match(fileNames[0]):
                waveform_files["station"] = "AIS"
            elif pattern_PAF.match(fileNames[0]):
                waveform_files["station"] = "PAF"
            elif pattern_ECH.match(fileNames[0]):
                waveform_files["station"] = "ECH"
            elif pattern_CRZF.match(fileNames[0]):
                waveform_files["station"] = "CRZF"
            elif pattern_DRV.match(fileNames[0]):
                waveform_files["station"] = "DRV"
            elif pattern_CCD.match(fileNames[0]):
                waveform_files["station"] = "CCD"
            else:
                waveform_files["station"] = "Erreur"

            # Type :
            if pattern_lh.match(fileNames[0]):
                waveform_files["type"] = "LH"
                waveform_files["files"] = fileNames
                fileName = qw.QFileDialog.getOpenFileName(self,"Waveform loader - LHN", self.rootFolder,"LHN files (*LHN*)",
                                                             options=options)
                waveform_files["files"] += [fileName]
                fileName = qw.QFileDialog.getOpenFileName(self,"Waveform loader - LHZ", self.rootFolder,"LHZ files (*LHZ*)",
                                                             options=options)
                waveform_files["files"] += [fileName]

            elif pattern_bh.match(fileNames[0]):
                waveform_files["type"] = "BH"
                waveform_files["files"] = fileNames
                fileName = qw.QFileDialog.getOpenFileName(self,"Waveform loader - BHN", self.rootFolder,"BHN files (*BHN*)",
                                                             options=options)
                waveform_files["files"] += [fileName]
                fileName = qw.QFileDialog.getOpenFileName(self,"Waveform loader - BHZ", self.rootFolder,"BHZ files (*BHZ*)",
                                                             options=options)
                waveform_files["files"] += [fileName]

            return waveform_files

        return None


def __snufflings__():
    '''Returns a list of snufflings to be exported by this module.'''

    return [ EOST_hodochrone() ]

