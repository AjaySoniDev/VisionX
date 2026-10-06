import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir:'tests/browser', timeout:45000, fullyParallel:false, workers:1,
  use:{baseURL:'http://127.0.0.1:4174', headless:true, launchOptions:process.env.VISIONX_BROWSER_EXECUTABLE ? {executablePath:process.env.VISIONX_BROWSER_EXECUTABLE,args:['--no-sandbox']} : {}},
  reporter:[['list'],['json',{outputFile:'validation/browser-tests.json'}]],
  webServer:{command:'node scripts/serve.mjs',url:'http://127.0.0.1:4174',reuseExistingServer:true,timeout:15000},
});
