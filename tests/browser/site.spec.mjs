import { test,expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';

const routes=['/','/architecture.html','/research.html','/evidence.html','/reproduce.html','/business.html','/references.html','/source.html','/404.html'];
for (const width of [320,390,768,1440]) {
  for (const route of routes) {
    test(`${width}px ${route}: content, images, console and overflow`,async ({page}) => {
      await page.setViewportSize({width,height:900});
      const errors=[];
      page.on('pageerror',e => errors.push(e.message));
      page.on('console',m => { if (m.type() === 'error') errors.push(m.text()); });
      const response=await page.goto(route);
      expect(response.status()).toBe(200);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('main')).toBeVisible();
      for (const image of await page.locator('img').all()) {
        await image.scrollIntoViewIfNeeded();
        await expect.poll(() => image.evaluate(i => i.complete && i.naturalWidth > 0)).toBe(true);
      }
      await page.locator('footer').scrollIntoViewIfNeeded();
      const imageFailures=await page.locator('img').evaluateAll(images => images.filter(i => !i.complete || !i.naturalWidth).map(i => i.src));
      expect(imageFailures).toEqual([]);
      expect(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)).toBe(false);
      expect(errors).toEqual([]);
      if (route === '/' || route === '/evidence.html') {
        fs.mkdirSync('validation/screenshots',{recursive:true});
        if (width === 390 || width === 1440) await page.screenshot({path:`validation/screenshots/${route === '/' ? 'home' : 'evidence'}-${width}.png`,fullPage:true});
      }
    });
  }
}
for (const route of routes) {
  test(`${route}: accessibility scan`,async ({page}) => {
    await page.setViewportSize({width:1280,height:900});
    await page.goto(route);
    const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
    expect(results.violations.map(v => ({id:v.id,impact:v.impact,nodes:v.nodes.length}))).toEqual([]);
  });
}
test('Mobile navigation supports keyboard opening, escape and page selection',async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto('/');
  const menu=page.getByRole('button',{name:'Menu'});
  await menu.focus(); await page.keyboard.press('Enter');
  await expect(menu).toHaveAttribute('aria-expanded','true');
  const navigation=page.getByRole('navigation',{name:'Primary navigation'});
  await navigation.getByRole('link',{name:'Research',exact:true}).focus();
  await page.keyboard.press('Escape');
  await expect(menu).toHaveAttribute('aria-expanded','false');
  await menu.click();
  await navigation.getByRole('link',{name:'Evidence',exact:true}).click();
  await expect(page).toHaveURL(/evidence\.html$/);
});
test('Static navigation and evidence remain available without JavaScript',async ({browser}) => {
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const page=await context.newPage(); await page.goto('http://127.0.0.1:4174/');
  await expect(page.getByRole('navigation',{name:'Primary navigation'})).toBeVisible();
  await page.getByRole('navigation',{name:'Primary navigation'}).getByRole('link',{name:'Evidence',exact:true}).click();
  await expect(page.locator('table')).toHaveCount(3);
  await context.close();
});
test('Missing routes return the designed 404 with deployment headers',async ({request}) => {
  const response=await request.get('/unavailable-route');
  expect(response.status()).toBe(404);
  expect(await response.text()).toContain('This page could not be found');
  expect(response.headers()['x-content-type-options']).toBe('nosniff');
  expect(response.headers()['content-security-policy']).toContain("script-src 'self'");
});
