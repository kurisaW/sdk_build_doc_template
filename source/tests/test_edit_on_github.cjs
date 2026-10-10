const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(
  path.join(__dirname, '../_static/edit_on_github.js'),
  'utf8',
);

function render(pathname) {
  const metas = [];
  const breadcrumbs = {
    children: [],
    appendChild(child) {
      this.children.push(child);
    },
    querySelector() {
      return null;
    },
  };
  const document = {
    readyState: 'complete',
    documentElement: {
      getAttribute(name) {
        return name === 'lang' ? 'zh-CN' : null;
      },
    },
    head: {
      appendChild(node) {
        metas.push(node);
      },
    },
    getElementsByTagName(name) {
      return name === 'meta' ? metas : [];
    },
    querySelector(selector) {
      if (selector === '.wy-breadcrumbs') return breadcrumbs;
      return null;
    },
    createElement(tagName) {
      return {
        tagName: tagName.toUpperCase(),
        attributes: {},
        children: [],
        setAttribute(name, value) {
          this.attributes[name] = String(value);
        },
        getAttribute(name) {
          return this.attributes[name] || null;
        },
        appendChild(child) {
          this.children.push(child);
        },
      };
    },
  };
  const context = {
    document,
    location: { pathname, protocol: 'https:' },
    window: {
      location: { pathname },
      SPHINX_EDIT_BASE_URL: 'https://github.com/acme/sdk-docs/edit/',
      versionInfo: {
        branch: 'main',
        url_path: 'lts',
        projectsDir: 'projects',
        copyFiles: ['README_zh.md', 'README.md'],
      },
    },
    console,
  };
  vm.runInNewContext(script, context);
  const item = breadcrumbs.children.find((child) => child.children?.length);
  return item?.children.find((child) => child.tagName === 'A')?.href || '';
}

assert.equal(
  render('/docs/lts/overview/README_zh.html'),
  'https://github.com/acme/sdk-docs/edit/main/projects/overview/README_zh.md',
);
assert.equal(
  render('/docs/lts/overview/setup_zh.html'),
  'https://github.com/acme/sdk-docs/edit/main/projects/overview/setup_zh.md',
);
assert.equal(render('/docs/lts/overview/index.html'), '');
console.log('Edit-on-GitHub mapping passed');
