// @ts-nocheck
const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'An Open Educational Resource for Advanced Robotics',
  favicon: 'img/favicon.ico',

  url: process.env.DEPLOY_ENV === 'VERCEL'
       ? 'https://physical-ai-humanoid-book.vercel.app'
       : 'https://Aqsaarshi.github.io',
  baseUrl: process.env.DEPLOY_ENV === 'VERCEL' || process.env.NODE_ENV === 'development'
           ? '/'
           : '/physical-ai-humanoid-book/',

  organizationName: 'Aqsaarshi',
  projectName: 'physical-ai-humanoid-book',
  trailingSlash: false,

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: { defaultLocale: 'en', locales: ['en'] },

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/Aqsaarshi/physical-ai-humanoid-book/tree/main/',
        },
        blog: false,
        theme: { customCss: require.resolve('./src/css/custom.css') },
      },
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'robotics-textbook',
        path: 'specs/002-physical-ai-robotics-textbook',
        routeBasePath: 'physical-ai-robotics-textbook',
        sidebarPath: require.resolve('./specs/002-physical-ai-robotics-textbook/sidebar.js'),
        editUrl: 'https://github.com/Aqsaarshi/physical-ai-humanoid-book/tree/main/',
      },
    ],
  ],

  customFields: {
    backendUrl: process.env.BACKEND_URL || 'http://127.0.0.1:8000',
  },

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics Textbook',
      logo: { alt: 'logo', src: 'img/logo.jpg' },
      items: [
        { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Textbook' },
        { to: '/chatbot', label: 'chatbot', position: 'left' },
        { href: 'https://github.com/Aqsaarshi/physical-ai-humanoid-book', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Textbook', to: 'docs/01-introduction' }] },
        {
          title: 'Community',
          items: [
            { label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/docusaurus' },
            { label: 'Discord', href: 'https://discordapp.com/invite/docusaurus' },
            { label: 'Twitter', href: 'https://twitter.com/docusaurus' },
          ],
        },
        { title: 'More', items: [{ label: 'GitHub', href: 'https://github.com/Aqsaarshi/physical-ai-humanoid-book' }] },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook.`,
    },
    prism: { theme: lightCodeTheme, darkTheme: darkCodeTheme },
  },
};

module.exports = config;
