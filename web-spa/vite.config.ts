import { vitePlugin as remix } from "@remix-run/dev";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  base: process.env.ENV === 'prod' ? '/public/' : '/',
  server: {
    host: '0.0.0.0'
  },
  envPrefix: "WEB_",
  plugins: [
    remix({
      ssr: false,
    }),
    tsconfigPaths(),
  ],
});
