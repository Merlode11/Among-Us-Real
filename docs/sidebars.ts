import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
    docs: [
        'accueil',
        {
            type: 'category',
            label: 'Joueur',
            items: [
                'joueur/partie',
                'joueur/roles-joueur',
                {
                    type: 'category',
                    label: 'Commandes',
                    link: {
                        type: 'doc',
                        id: 'joueur/commandes/index',
                    },
                    items: [
                        'joueur/commandes/aide',
                        'joueur/commandes/tache',
                        'joueur/commandes/info',
                        'joueur/commandes/morts',
                        'joueur/commandes/mort',
                        'joueur/commandes/fait',
                        'joueur/commandes/sos',
                        'joueur/commandes/tuer',
                        'joueur/commandes/vote',
                    ],
                },
                'joueur/sms-partie',
                'joueur/discord-partie',
                'joueur/whatsapp-partie',
                'joueur/instagram-partie',
            ],
        },
        {
            type: 'category',
            label: 'Gestionnaire du jeu',
            items: [
                'gestionnaire/installation',
                {
                    type: 'category',
                    label: "Configuration d'une partie",
                    link: { type: 'doc', id: 'gestionnaire/configuration/index' },
                    items: [
                        'gestionnaire/configuration/ajout-joueurs',
                        'gestionnaire/configuration/parametres',
                        'gestionnaire/configuration/taches',
                    ],
                },
                'gestionnaire/discord',
                'gestionnaire/sms',
                'gestionnaire/whatsapp',
                'gestionnaire/web',
                'gestionnaire/instagram',
            ],
        },
    ],
};

export default sidebars;
