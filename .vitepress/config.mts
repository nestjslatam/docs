import { defineConfig } from 'vitepress';

export default defineConfig({
  lang: 'es-ES',
  title: 'NestJS Latam',
  description:
    'Domain-Driven Design, event sourcing y herramientas para NestJS. Documentación en español.',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  head: [
    ['meta', { name: 'theme-color', content: '#1e73be' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:locale', content: 'es_ES' }],
    ['meta', { property: 'og:site_name', content: 'NestJS Latam' }],
    ['link', { rel: 'icon', href: '/favicon.svg', type: 'image/svg+xml' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'NestJS Latam',

    nav: [
      { text: 'Guía', link: '/guia/', activeMatch: '/guia/' },
      { text: 'CLI', link: '/cli/', activeMatch: '/cli/' },
      { text: 'Value Objects', link: '/valueobjects/', activeMatch: '/valueobjects/' },
      { text: 'Event Sourcing', link: '/event-sourcing/', activeMatch: '/event-sourcing/' },
      { text: 'Artículos', link: '/articulos/', activeMatch: '/articulos/' },
      {
        text: 'Paquetes',
        items: [
          { text: 'ddd-lib', link: 'https://www.npmjs.com/package/@nestjslatam/ddd-lib' },
          { text: 'ddd-cli', link: 'https://www.npmjs.com/package/@nestjslatam/ddd-cli' },
          { text: 'ddd-valueobjects', link: 'https://www.npmjs.com/package/@nestjslatam/ddd-valueobjects' },
          { text: 'ddd-es-lib', link: 'https://www.npmjs.com/package/@nestjslatam/ddd-es-lib' },
          { text: '—' , link: '/' },
          { text: 'Comunidad', link: 'https://nestjslatam.dev' },
        ],
      },
    ],

    sidebar: {
      '/guia/': [
        {
          text: 'Empezar',
          collapsed: false,
          items: [
            { text: 'Qué es esto', link: '/guia/' },
            { text: 'Instalación', link: '/guia/instalacion' },
            { text: 'Tu primer agregado', link: '/guia/primer-agregado' },
          ],
        },
        {
          text: 'El dominio',
          collapsed: false,
          items: [
            { text: 'Agregados', link: '/guia/agregados' },
            { text: 'Value objects', link: '/guia/value-objects' },
            { text: 'Reglas rotas', link: '/guia/reglas-rotas' },
            { text: 'Eventos de dominio', link: '/guia/eventos' },
          ],
        },
        {
          text: 'La aplicación',
          collapsed: false,
          items: [
            { text: 'Comandos y consultas', link: '/guia/cqrs' },
            { text: 'Mapear errores a HTTP', link: '/guia/errores-http' },
          ],
        },
        {
          text: 'Referencia',
          collapsed: true,
          items: [{ text: 'API', link: '/guia/api' }],
        },
      ],
      '/cli/': [
        {
          text: 'ddd-cli',
          items: [
            { text: 'Introducción', link: '/cli/' },
            { text: 'Guía completa', link: '/cli/guia' },
            { text: 'Servidor MCP', link: '/cli/mcp' },
          ],
        },
      ],
      '/valueobjects/': [
        { text: 'ddd-valueobjects', items: [{ text: 'Catálogo', link: '/valueobjects/' }] },
      ],
      '/event-sourcing/': [
        { text: 'ddd-es-lib', items: [{ text: 'Introducción', link: '/event-sourcing/' }] },
      ],
      '/articulos/': [
        { text: 'Artículos', items: [{ text: 'Todos', link: '/articulos/' }] },
      ],
    },

    socialLinks: [{ icon: 'github', link: 'https://github.com/nestjslatam' }],

    search: { provider: 'local' },

    editLink: {
      pattern: 'https://github.com/nestjslatam/docs/edit/main/:path',
      text: 'Editar esta página en GitHub',
    },

    outline: { level: [2, 3], label: 'En esta página' },

    docFooter: { prev: 'Anterior', next: 'Siguiente' },
    darkModeSwitchLabel: 'Tema',
    returnToTopLabel: 'Volver arriba',
    langMenuLabel: 'Idioma',
    lastUpdatedText: 'Actualizado',

    footer: {
      message:
        'Publicado con licencia MIT. Hecho en Perú 🇵🇪 · Impulsado por <a href="https://beyondnet.info/">BeyondNetCode</a>',
      copyright: '© 2026 NestJS Latam',
    },
  },
});
