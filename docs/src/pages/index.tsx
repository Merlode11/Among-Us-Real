import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import {useRef} from 'react';
// @ts-ignore
import AmongUsSound from '@site/static/among-us-sound.mp3';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const audioRef = useRef<HTMLAudioElement>(null);
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <audio ref={audioRef} src={AmongUsSound} preload="auto" />
      <div className="container">
        <Heading as="h1" className="hero__title">
          <AmongUsClickable audioRef={audioRef}>{siteConfig.title}</AmongUsClickable>
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/accueil">
            Découvrir le projet
          </Link>
        </div>
      </div>
    </header>
  );
}

function playAmongUsSound(audioRef: React.RefObject<HTMLAudioElement>) {
  if (audioRef.current) {
    audioRef.current.currentTime = 0;
    audioRef.current.play();
  }
}

function AmongUsClickable({children, audioRef}: {children: ReactNode, audioRef: React.RefObject<HTMLAudioElement>}) {
  return (
    <span
      style={{cursor: 'pointer'}}
      onClick={() => playAmongUsSound(audioRef)}
      title="Jouer le son Among Us"
    >
      {children}
    </span>
  );
}

function ProjectIntro() {
  const audioRef = useRef<HTMLAudioElement>(null);
  return (
    <section className={styles.introSection}>
      <audio ref={audioRef} src={AmongUsSound} preload="auto" />
      <div className="container">
        <Heading as="h2">
          Qu'est-ce que <AmongUsClickable audioRef={audioRef}>Among Us Real</AmongUsClickable> ?
        </Heading>
        <p>
          <AmongUsClickable audioRef={audioRef}>Among Us Real</AmongUsClickable> est une adaptation communautaire et open source du célèbre jeu <AmongUsClickable audioRef={audioRef}>Among Us</AmongUsClickable>, conçue pour être jouée en présentiel ou à distance, sur SMS, WhatsApp, Discord, Instagram, Web, et plus encore. Le projet permet d'organiser des parties dans la vraie vie, en s'appuyant sur des outils numériques pour gérer les rôles, les tâches, les votes et la communication entre joueurs.
        </p>
        <ul>
          <li>Accessible à tous, même sans ordinateur ou console</li>
          <li>Plusieurs modes de jeu : SMS, WhatsApp, Discord, Instagram, Web</li>
          <li>Gestion automatisée des rôles, tâches, votes et réunions</li>
          <li>Open source : chacun peut contribuer et améliorer le projet</li>
        </ul>
        <p>
          <Link to="/docs/accueil">En savoir plus sur l'histoire et les fonctionnalités</Link>
        </p>
      </div>
    </section>
  );
}

function ModesSection() {
  return (
    <section className={styles.modesSection}>
      <div className="container">
        <Heading as="h2">Modes de fonctionnement</Heading>
        <div className="row">
          <div className="col col--6">
            <h3>Mode SMS</h3>
            <p>Jouez via de simples messages texte, idéal pour les groupes sans accès à Internet ou applications modernes.</p>
          </div>
          <div className="col col--6">
            <h3>Mode WhatsApp</h3>
            <p>Utilisez les groupes et messages privés WhatsApp pour une expérience interactive et rapide.</p>
          </div>
        </div>
        <div className="row">
          <div className="col col--6">
            <h3>Mode Discord</h3>
            <p>Intégrez un bot Discord pour gérer les parties, les rôles et les commandes dans des salons dédiés.</p>
          </div>
          <div className="col col--6">
            <h3>Mode Instagram</h3>
            <p>Jouez via messages privés Instagram, pour toucher un public plus large et connecté.</p>
          </div>
        </div>
        <div className="row">
          <div className="col col--12">
            <h3>Mode Web</h3>
            <p>Une interface web pour centraliser la gestion des parties et offrir une expérience moderne.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout
      title="Among Us Real – Accueil"
      description="Adaptation open source du jeu Among Us pour jouer partout, avec n'importe quel moyen de communication !">
      <HomepageHeader />
      <main style={{padding: '20px 0'}}>
        <ProjectIntro />
        <HomepageFeatures />
        <ModesSection />
      </main>
    </Layout>
  );
}
