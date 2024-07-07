from dataclasses import dataclass


@dataclass
class Latin(object):
    """
    The Latin class initializes a dictionary named verbum that maps French phrases to their Latin translations. This
    dictionary is used to store and retrieve Latin translations for specific French terms.
    """

    def __init__(self) -> None:
        """
        Initialize the Latin class with a dictionary of Latin phrases and their translations.
        """
        self.verbum: dict[str, str] = {
                                        # M&M's to M&M's
                                        'besoin aide': 'auxilium postulo',
                                        # MM to Collector
                                        'focalisation sur ces ressources': 'focus in his opibus : ',
                                        'point de dépot': 'collectio rerum : ',
                                       'inventaire des explorateur': 'quid habes ut nobis offerat',
                                        'demande de ressources': 'vade ad me aliquid : ',
                                        'Vous ne pouvez pas passer maître': 'Non Potes dominum facti',

                                        # MM to Incant
                                        'deplace-toi vers : ': 'movere ad : ',
                                       'ressources placés pour l\'incantation': 'facultates positas carmina',

                                        # Incant to MM
                                        'incantation raté': 'defecit carmen',
                                        'incantation réussie': 'felix carmen', # Incant to PNJ

                                        # Coll to MM
                                        'ressources déposées : ': 'opes deposita : ',
                                        # TODO - parse l'inventaire
                                        'Je suis positionné pour le dépot': 'situm intrare',
                                       'Je suis sortie du dépot': 'sum extra domum',
                                        'Les ressources de mon inventaire sont : ': 'opes in meo inventario sunt : ',

                                        'Les ressources de mon inventaire sont : ': 'opes in meo inventario sunt : ',

                                        # All to push or firstborn
                                        'confirmation id': 'sum socius senatus',

                                        # COOCK to push
                                        'voici votre repas': 'hic est prandium tuum',

                                        # MM to push
                                        'deplace-toi vers : ': 'movere ad',
                                        'changement de rôle': 'factus es : ',

                                        # North_guard to ALL
                                        'voici le nord': 'est dominus aquilonis',
                                        # North guard to M&M's or progenitor
                                        'je ai plus de force': 'Ego plus viribus',

                                        # Coll to Coll
                                        'Qui est collecteur ?': 'Quot publicani ibi sunt?',
                                        'Je suis collecteur': 'Ego sum publicani ibi',

                                        # Push to Push
                                        'Qui est un pusher': 'Quis est puer interfector?',
                                        'Je suis un pusher': 'Ego sum puer inteffector',

                                        # First Born to MM
                                        'Je me vais me transormer en : ': 'Ego me transform : ',
                                        'Qui es-tu': 'Quis es',

                                        # MM to First Born
                                        'Je suis ton maître': 'Ego sum dominus tuus',

                                        # Incantator to Collecteur
                                        'évo de niveau': 'nobilis incantatio',

                                        'Collector': 'Collector',
                                        'Pusher': 'Pusher',
                                        'Incantator': 'Incantator',
                                        'Progenitor': 'Progenitor',
                                        'Mastermind': 'Mastermind',
                                        'North guard': 'North guard',
                                        'Pnj': 'Pnj',

                                        #PNJ to Incant
                                        'J\'ai bougé': 'motus sum',

                                        # Elder to all
                                        'Voici l\'histoire de l\'Empire ACCMST': 'haec est historia imperii ACCMST',

                                        # M&M's to Pusher
                                        'formation tortue': 'satus testudo : ',

                                        # Pusher to M&M's
                                        # 'je vais mourir': 'recessi ab exercitu',
                                        'je suis démis de la 0 légion': 'Dimissus a Legione Honoris',
                                        'je suis démis de la 1ère légion': 'Dimissus a legione prima',
                                        'je suis démis de la 2ème légion': 'Dimissus a legione secunda',
                                        'je suis démis de la 3ème légion': 'Dimissus a legione tertia',
                                        'remplace le pousseur : ': 'occupat exercitum : ',

                                        'Où vais-je': 'Quo ego vado',
                                        'point de ralliment': 'collectio militum : ',


                                       'etat ressources': 'ut inventarium rerum',

                                        'assignation rôles': 'assignationem partium : ',
                                        'nouvelle tâche': 'habes novum negotium : ',

                                        'demande de nourriture': 'cibo opus est',

                                        'changement de rôle': 'factus es : ',
                                        'reconfiguration des rôles': 'omnis fit : ',

                                        'presence ennemis': 'inimicos recta praemisit',

                                        'temps restant incantation': 'quantum temporis reliquum est carminibus',


                                        'confirmation action': 'hic servio tibi domino',

                                        'plan de bataille': 'pugnae consilia',
                                        'strat ressources': 'omnis venite ut',

                                        'divertis-moi (peroquet)': 'oblectas',
                                        'pousse les autres': 'officium tuum est ad ventilabis inimicos',

                                        'qui est le mastermind ?': 'quis est dominus mentis',
                                        'c\'est moi': 'ego sum',

                                        # Numbers
                                        'zero': 'nulla',
                                        'un': 'unum',
                                        'deux': 'duo',
                                        'trois': 'tres',
                                        'quatre': 'quattuor',
                                        'cinq': 'quinque',
                                        'six': 'sex',
                                        'sept': 'septem',
                                        'huit': 'octo',
                                        'neuf': 'novem',

                                        # Elements
                                        'linemate': 'linemate',
                                        'deraumere': 'deraumere',
                                        'sibur': 'sibur',
                                        'mendiane': 'mendiane',
                                        'phiras': 'phiras',
                                        'thystame': 'thystame',
                                        'food': 'cibus',
                                       }
