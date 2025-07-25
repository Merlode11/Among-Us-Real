import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
    title: 'Among Us Real',
    tagline: 'Jouez avec vos amis à un Among Us dans la vie réelle avec ce logiciel !',
    favicon: 'img/amongus.ico',

    // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
    future: {
        v4: true, // Improve compatibility with the upcoming Docusaurus v4
    },

    // Set the production url of your site here
    url: 'https://merlode11.github.io',
    // Set the /<baseUrl>/ pathname under which your site is served
    // For GitHub pages deployment, it is often '/<projectName>/'
    baseUrl: '/Among-Us-Real/',

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.
    organizationName: 'Merlode11', // Usually your GitHub org/username.
    projectName: 'Among-Us-Real', // Usually your repo name.
    deploymentBranch: 'gh-pages', // Branche de déploiement

    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',

    // Even if you don't use internationalization, you can use this field to set
    // useful metadata like html lang. For example, if your site is Chinese, you
    // may want to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: 'fr',
        locales: ['fr'],
    },

    presets: [
        [
            'classic',
            {
                docs: {
                    sidebarPath: './sidebars.ts',
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        'https://github.com/Merlode11/Among-Us-Real/blob/master/docs/',
                },
                blog: {
                    blogTitle: 'Blog',
                    blogDescription: "Le blog d'Among Us Real",
                    blogSidebarTitle: 'Tous les articles',
                    blogSidebarCount: 'ALL',
                    showReadingTime: true,
                    feedOptions: {
                        type: ['rss', 'atom'],
                        xslt: true,
                    },
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        'https://github.com/Merlode11/Among-Us-Real/blob/master/docs/',
                    // Useful options to enforce blogging best practices
                    onInlineTags: 'warn',
                    onInlineAuthors: 'warn',
                    onUntruncatedBlogPosts: 'warn',

                },
                theme: {
                    customCss: './src/css/custom.css',
                },
            } satisfies Preset.Options,
        ],
    ],

    themeConfig: {
        // Replace with your project's social card
        image: 'img/among-us-youtube-banner.jpg',
        colorMode: {
            defaultMode: 'dark',
            disableSwitch: false,
            respectPrefersColorScheme: true,
        },
        navbar: {
            title: 'Among Us Real',
            logo: {
                alt: 'Among us',
                src: 'img/amongus.ico',
            },
            items: [
                {
                    type: 'docSidebar',
                    sidebarId: 'docs',
                    position: 'left',
                    label: 'Docs',
                },
                {to: '/blog', label: 'Blog', position: 'left'},
                {
                    href: 'https://github.com/Merlode11/Among-US-Real',
                    label: 'GitHub',
                    position: 'right',
                },
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Docs',
                    items: [
                        {
                            label: 'Documentation',
                            to: '/docs/accueil',
                        },
                    ],
                },
                {
                    title: 'Communauté',
                    items: [
                        {
                            label: 'Instagram',
                            href: 'https://www.instagram.com/among.us.real/',
                        },
                        {
                            // Say that the discord server is not available yet in a popup
                            html: `<span class="footer__link-item" onclick='alert("Le serveur Discord est pas encore disponible.")'>Discord</span>`,
                        },
                    ],
                },
                {
                    title: 'Plus',
                    items: [
                        {
                            label: 'Blog',
                            to: '/blog',
                        },
                        {
                            label: 'GitHub',
                            href: 'https://github.com/Merlode11/Among-US-Real',
                        },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} Among Us Real par Merlode. Built with Docusaurus.`,
        },
        prism: {
            theme: prismThemes.github,
            darkTheme: prismThemes.dracula,
        },
    } satisfies Preset.ThemeConfig,
};

export default config;
