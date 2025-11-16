import adapter from '@sveltejs/adapter-static';

const dev = process.env.NODE_ENV === 'development';

export default {
  kit: {
    adapter: adapter({
      pages: 'docs',
      assets: 'docs',
      fallback: undefined,
      precompress: false,
      strict: true
    }),
    paths: {
      base: dev ? '' : '/shrine'
    },
    prerender: {
      handleHttpError: ({ path, referrer, message }) => {
        // Allow 404 errors for static assets (with or without base path)
        if (path.startsWith('/images/') || path.startsWith('/icons/') || 
            path.startsWith('/shrine/images/') || path.startsWith('/shrine/icons/')) {
          console.warn(`[Warning] Missing static asset: ${path} (referenced from ${referrer})`);
          return;
        }
        // Otherwise, throw the error
        throw new Error(message);
      }
    }
  }
};

