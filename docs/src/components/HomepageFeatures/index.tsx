import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Accessibilité universelle',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Jouez à Among Us Real partout : en présentiel ou à distance, sur SMS, WhatsApp, Discord, Instagram ou Web. Aucun matériel spécifique n'est requis, juste un moyen de communication !
      </>
    ),
  },
  {
    title: 'Gestion automatisée du jeu',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Attribution automatique des rôles, gestion des tâches, des votes, des réunions et notifications personnalisées selon le mode de jeu. L'organisateur peut tout piloter facilement.
      </>
    ),
  },
  {
    title: 'Open source et personnalisable',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Le projet est entièrement open source : chacun peut contribuer, adapter les règles, ajouter des fonctionnalités ou améliorer la documentation.
      </>
    ),
  },
  {
    title: 'Sécurité et respect de la vie privée',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Les données personnelles (numéros, identifiants) ne sont utilisées que pour le bon déroulement du jeu et ne sont jamais partagées.
      </>
    ),
  },
  {
    title: 'Gestion de crise (SOS)',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Une commande spéciale permet de suspendre la partie et d'alerter l'organisateur en cas de problème ou d'urgence, pour une expérience sereine et maîtrisée.
      </>
    ),
  },
  {
    title: 'Documentation complète',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Retrouvez toutes les règles, commandes, modes de jeu et guides pour organiser ou rejoindre une partie facilement.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
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
