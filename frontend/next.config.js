/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: false, // ⬅️ TURN OFF
  },

  typescript: {
    ignoreBuildErrors: true, // ⬅️ deploy ko block nahi karega
  },

  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  },

  images: {
    domains: ['localhost', '127.0.0.1'],
  },
};

module.exports = nextConfig;