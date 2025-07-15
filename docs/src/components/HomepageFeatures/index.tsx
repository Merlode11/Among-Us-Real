import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  img: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Accessibilité universelle',
    img: require('@site/static/img/accessibilite.png').default,
    description: (
      <>
        Jouez à Among Us Real partout : en présentiel, sur SMS, WhatsApp, Discord, Instagram ou Web. Aucun matériel spécifique n'est requis, juste un téléphone mobile !
      </>
    ),
  },
  {
    title: 'Gestion automatisée du jeu',
    img: require('@site/static/img/industry-automation.png').default,
    description: (
      <>
        Attribution automatique des rôles, gestion des tâches, des votes, des réunions et notifications personnalisées selon le mode de jeu. L'organisateur peut tout piloter facilement.
      </>
    ),
  },
  {
    title: 'Open source et personnalisable',
    img: require('@site/static/img/open-source-programming.png').default,
    description: (
      <>
        Le projet est entièrement open source : chacun peut contribuer, adapter les règles, ajouter des fonctionnalités ou améliorer la documentation.
      </>
    ),
  },
  {
    title: 'Sécurité et respect de la vie privée',
    img: require('@site/static/img/data-protection.png').default,
    description: (
      <>
        Les données personnelles (numéros, identifiants) ne sont utilisées que pour le bon déroulement du jeu et ne sont jamais partagées.
      </>
    ),
  },
  {
    title: 'Gestion de crise (SOS)',
    img: require('@site/static/img/emergency.png').default,
    description: (
      <>
        Une commande spéciale permet de suspendre la partie et d'alerter l'organisateur en cas de problème ou d'urgence, pour une expérience sereine et maîtrisée.
      </>
    ),
  },
  {
    title: 'Documentation complète',
    img: require('@site/static/img/documentation.png').default,
    description: (
      <>
        Retrouvez toutes les règles, commandes, modes de jeu et guides pour organiser ou rejoindre une partie facilement.
      </>
    ),
  },
];

function Feature({title, img, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={img} className={styles.featureSvg} role="img"  alt={title}/>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
